import os
import time
import logging

from src import settings
from src import mangadex
from src import webhook

logger = logging.getLogger(__name__)

logging.basicConfig(
    format='%(asctime)s %(name)-1s %(levelname)-1s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    encoding='utf-8', level=logging.INFO,
)


def main():
    logger.info("Starting MangaDex-Notifications")

    if settings.GET_PRIVATE_LIST:
        session = mangadex.login()
        manga_list = mangadex.get_manga_list(session, get_latests=True)
    elif settings.PUBLIC_MANGA_LIST:
        session = None
        manga_list = mangadex.get_manga_list(settings.PUBLIC_MANGA_LIST, get_info=True, get_latests=True)
    else:
        raise Exception("No manga list source")

    logger.info("Successfully started MangaDex-Notifications")

    while True:
        if settings.GET_PRIVATE_LIST:
            if mangadex.session_expired(session):
                session = mangadex.refresh_session(session)

        input = session or settings.PUBLIC_MANGA_LIST
        manga_list = mangadex.update_manga_list(input, manga_list)
        for manga in manga_list:
            latest = mangadex.get_latest_chapter(manga["id"])
            if float(latest["chapter"]) > float(manga["latest_chapter"]["chapter"]):
                logger.info(f"New chapter of {manga['title']} released")
                webhook.send_webhook(manga, latest)
                manga["latest_chapter"] = latest

        time.sleep(settings.REFRESH_RATE)


if __name__ == "__main__":
    main()
