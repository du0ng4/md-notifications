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
    logger.info("Starting Mangadex-Notifications")

    session = mangadex.login()
    manga_list = mangadex.get_manga_list(session, get_latests=True)

    logger.info("Successfully started Mangadex-Notifications")

    while True:
        if mangadex.session_expired(session):
            session = mangadex.refresh_session(session)

        manga_list = mangadex.update_manga_list(session, manga_list)
        for manga in manga_list:
            latest = mangadex.get_latest_chapter(manga["id"])
            if float(latest["chapter"]) > float(manga["latest_chapter"]["chapter"]):
                logger.info(f"New chapter of {manga['title']} released")
                webhook.send_webhook(manga, latest)
                manga["latest_chapter"] = latest

        time.sleep(settings.REFRESH_RATE)


if __name__ == "__main__":
    main()
