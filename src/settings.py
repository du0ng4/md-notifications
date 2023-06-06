import os
import logging

import utils

logger = logging.getLogger(__name__)

PUBLIC_MANGA_LIST = utils.get_value_from_file("/etc/secret/mdlist") or os.getenv("PUBLIC_MANGA_LIST")
MANGADEX_USERNAME = utils.get_value_from_file("/etc/secret/mangadex_username") or os.getenv("MANGADEX_USERNAME")
MANGADEX_PASSWORD = utils.get_value_from_file("/etc/secret/mangadex_username") or os.getenv("MANGADEX_PASSWORD")
DISCORD_WEBHOOK_URL = utils.get_value_from_file("/etc/secret/discord_webhook_url") or os.getenv("DISCORD_WEBHOOK_URL")

GET_PRIVATE_LIST = True if MANGADEX_USERNAME and MANGADEX_PASSWORD else False

STYLE = utils.get_value_from_file("/etc/config/style") or os.getenv("STYLE") or "full"
AVATAR_URL = utils.get_value_from_file("/etc/config/avatar_url") or os.getenv("AVATAR_URL") or "https://avatars.githubusercontent.com/u/100574686?s=200&v=4"
SENDER_USERNAME = utils.get_value_from_file("/etc/config/sender_username") or os.getenv("WEBHOOK_USERNAME") or "MD-Notifications"

REFRESH_RATE = 20
