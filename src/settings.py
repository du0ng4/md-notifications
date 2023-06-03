import os
import logging

logger = logging.getLogger(__name__)

PUBLIC_MANGA_LIST = os.getenv("PUBLIC_MANGA_LIST")
MANGADEX_USERNAME = os.getenv("MANGADEX_USERNAME")
MANGADEX_PASSWORD = os.getenv("MANGADEX_PASSWORD")

GET_PRIVATE_LIST = True if MANGADEX_USERNAME and MANGADEX_PASSWORD else False

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
AVATAR_URL = os.getenv("AVATAR_URL") or "https://avatars.githubusercontent.com/u/100574686?s=200&v=4"
WEBHOOK_USERNAME = os.getenv("WEBHOOK_USERNAME") or "MD-Notification"

REFRESH_RATE = 20
