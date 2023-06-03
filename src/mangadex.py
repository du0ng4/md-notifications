import json
import requests
from datetime import datetime
import time
import logging

from src import settings

logger = logging.getLogger(__name__)

BASE_URL = "https://api.mangadex.org"


def login():
    logger.debug("login()")

    credentials = {
        "username": settings.MANGADEX_USERNAME,
        "password": settings.MANGADEX_PASSWORD,
    }

    r = requests.post(
        f"{BASE_URL}/auth/login",
        json=credentials,
    )
    if r.status_code != 200:
        raise Exception(f"Could not authenticate with Mangadex API {r.json()}")

    session = {
        "session_token": r.json()["token"]["session"],
        "expires": datetime.now().timestamp() + 60 * 10,
        "refresh_token": r.json()["token"]["refresh"]
    }

    return session


def refresh_session(session):
    logger.debug(f"refresh_session({session})")

    r = requests.post(
        f"{BASE_URL}/auth/refresh",
        json={"token": session["refresh_token"]},
    )
    if r.status_code != 200:
        raise Exception(f"Could not refresh with Mangadex API {r.json()}")

    session = {
        "session_token": r.json()["token"]["session"],
        "expires": datetime.now().timestamp() + 60 * 10,
        "refresh_token": session["refresh_token"]
    }

    return session


def session_expired(session):
    if datetime.now().timestamp() > session["expires"]:
        return True

    return False


def get_manga_list(session, get_latests=False):
    logger.debug(f"get_manga_list({session}, {get_latests})")

    while True:
        try:
            r = requests.get(
                f"{BASE_URL}/user/follows/manga",
                headers={"Authorization": f"Bearer {session['session_token']}"},
                params={
                    "limit": 100,
                    "includes[]": ["cover_art"]
                }
            )
            if r.status_code != 200:
                logger.error(r.text)
                raise Exception

            break
        except Exception as e:
            logger.error(e)
            time.sleep(10)

    manga_list = []
    for manga in r.json()["data"]:
        manga_list.append({
            "id": manga["id"],
            "title": manga["attributes"]["title"].get("en") or manga["attributes"]["title"].get("ja-ro"),
            "description": manga["attributes"]["description"]["en"],
            "status": manga["attributes"]["status"],
            "demographic": manga["attributes"]["publicationDemographic"],
            "content_rating": manga["attributes"]["contentRating"],
            "genres": [obj["attributes"]["name"]["en"] for obj in manga["attributes"]["tags"] if obj["attributes"]["group"] == "genre"],
            "cover_art": next(obj["attributes"]["fileName"] for obj in manga["relationships"] if obj["type"] == "cover_art"),
            "links": {"mal": manga["attributes"]['links'].get("mal"), "al": manga["attributes"]['links'].get("mal")}
        })

    if get_latests:
        for manga in manga_list:
            manga["latest_chapter"] = get_latest_chapter(manga["id"])
    
    return manga_list
    

def get_latest_chapter(id):
    logger.debug(f"get_latest_chapter({id})")

    while True:
        try:
            r = requests.get(
                f"{BASE_URL}/manga/{id}/feed",
                params={
                    "limit": 1,
                    "translatedLanguage[]": ["en"],
                    "order[chapter]": "desc",
                    "includes[]": ["scanlation_group", "user"]
                }
            )
            if r.status_code != 200:
                logger.error(r.text)
                raise Exception

            break
        except Exception as e:
            logger.error(e)
            time.sleep(10)

    data = r.json()["data"][0]
    chapter = {
        "id": data["id"],
        "volume": data["attributes"]["volume"],
        "chapter": data["attributes"]["chapter"],
        "title": data["attributes"]["title"],
        "external_url": data["attributes"]["externalUrl"],
        "pages": data["attributes"]["pages"],
        "group": next((obj["attributes"]["name"] for obj in data["relationships"] if obj["type"] == "scanlation_group"), "No Group"),
        "uploader": next((obj["attributes"]["username"] for obj in data["relationships"] if obj["type"] == "user"))
    }
    return chapter


def update_manga_list(session, manga_list):
    logger.debug(f"update_manga_list({session}, {manga_list})")

    current_following = get_manga_list(session)

    for a in current_following: 
        if not any(a['id'] == b['id'] for b in manga_list):
            logger.info(f"Added {a['title']} to manga list")
            a['latest_chapter'] = get_latest_chapter(a['id'])
            manga_list.append(a)

    for b in manga_list[:]:
        if not any(b['id'] == a['id'] for a in current_following):
            logger.info(f"Removed {b['title']} from manga list")
            manga_list.remove(b)

    return manga_list
