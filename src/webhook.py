import os
import requests
import json
from datetime import datetime
import pytz
import logging

from src import settings

logger = logging.getLogger(__name__)

WEBHOOK_URL = settings.DISCORD_WEBHOOK_URL


def send_webhook(manga, chapter):
    logger.debug(f"send_webhook({manga}, {chapter})")

    if settings.STYLE == "compact":
        message = generate_compact(manga, chapter)
    else:
        message = generate_full(manga, chapter)

    requests.post(WEBHOOK_URL, data=message, headers={'Content-Type': 'application/json'})


def generate_full(manga, chapter):
    logger.debug("generate_full")

    message = {
        "username": settings.SENDER_USERNAME,
        "avatar_url": settings.AVATAR_URL,
        "embeds": [
            {
                "author": {
                    "name": "MangaDex",
                    "icon_url": "https://avatars.githubusercontent.com/u/100574686?s=200&v=4"
                },
                "title": None,
                "url": chapter["external_url"] or f"https://mangadex.org/chapter/{chapter['id']}",
                "description": f"Group: {chapter['group']}\nUploader: {chapter['uploader']}",
                "color": "4104968",
                "fields": [
                    {
                        "name": "**Genres**",
                        "value": ", ".join(manga["genres"]),
                    },
                    {
                        "name": "**Demographic**",
                        "value": manga["demographic"],
                        "inline": True
                    },
                    {
                        "name": "**Content Rating**",
                        "value": manga["content_rating"],
                        "inline": True
                    },
                    {
                        "name": "**Pages**",
                        "value": chapter["pages"],
                        "inline": True
                    },
                ],
                "image": {
                    "url": f"https://uploads.mangadex.org/covers/{manga['id']}/{manga['cover_art']}"
                },
                "timestamp": datetime.now(pytz.UTC).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            }
        ]
    }

    title = f"{manga['title']}\n"
    title += f"Vol. {chapter['volume']} " if chapter["volume"] else ""
    title += f"Ch. {chapter['chapter']}"
    title += f": {chapter['title']}" if chapter["title"] else ""
    message["embeds"][0]["title"] = title

    links = ""
    if manga['links']['mal']:
        links += f"[MAL](https://myanimelist.net/manga/{manga['links']['mal']})"
    if manga['links']['al']:
        links += f"{' / ' if links else ''}[AL](https://anilist.co/manga/{manga['links']['al']})"
    message["embeds"][0]["fields"].append({"name": "**Links**", "value": links})

    message_json = json.dumps(message)

    return message_json


def generate_compact(manga, chapter):
    logger.debug("generate_compact")

    message = {
        "username": settings.SENDER_USERNAME,
        "avatar_url": settings.AVATAR_URL,
        "embeds": [
            {
                "author": {
                    "name": "MangaDex",
                    "icon_url": "https://avatars.githubusercontent.com/u/100574686?s=200&v=4"
                },
                "title": None,
                "url": chapter["external_url"] or f"https://mangadex.org/chapter/{chapter['id']}",
                "description": f"**Group**: {chapter['group']}   **Uploader**: {chapter['uploader']}",
                "color": "4104968",
                "thumbnail": {
                    "url": f"https://uploads.mangadex.org/covers/{manga['id']}/{manga['cover_art']}"
                },
                "timestamp": datetime.now(pytz.UTC).strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            }
        ]
    }

    title = f"{manga['title']} - "
    title += f"Vol. {chapter['volume']} " if chapter["volume"] else ""
    title += f"Ch. {chapter['chapter']}"
    title += f": {chapter['title']}" if chapter["title"] else ""
    message["embeds"][0]["title"] = title

    message_json = json.dumps(message)

    return message_json
