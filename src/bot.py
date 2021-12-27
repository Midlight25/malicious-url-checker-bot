# -*- coding: utf-8 -*-

"""Event based programming for the bot"""

# System Libraries
import logging
import re
from urllib.parse import quote

# Third-Party Modules
import discord
import requests

# My Modules
import info


class DiscordBot(discord.Client):
    """Discord Bot that scans messages for URLs and then evaluates if they
        are trustworthy"""

    # Regular Expression for finding links
    URL_RE: str = r'(?:http(?:s)?:\/\/)?.(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b(?:[-a-zA-Z0-9@:%_\+.~#?&//=]*)'

    # Standard logger that all classes report to.
    LOGGER = logging.getLogger('discord').getChild('bot')

    API_URL: str = r"https://ipqualityscore.com/api/json/url/"

    def __init__(self, api_key: str):
        super().__init__()
        self.url: str = DiscordBot.API_URL + api_key

    async def on_ready(self):
        DiscordBot.LOGGER.info("Discord Bot is ready to go.")

    async def on_message(self, message):
        if message.author == self.user:
            return

        # Scan message and check for links in message
        matches = re.findall(DiscordBot.URL_RE, message.content)

        # Iterate through links found in message
        for match in matches:
            self.check_url_status(match)

    async def on_error(self, event, *args, **kwargs):

        if event == "on_message":
            DiscordBot.LOGGER.error(
                f"Unhandled Message: \"{args[0].content}\" {args[0]}")
        else:
            raise

    def check_url_status(self, url: str):
        """API Request to Safe Browsing API for trustworthiness"""

        # Change url to url encoded string
        encoded_url: str = quote(url, safe='')

        # Build API call URL
        request_url = f"{self.url}/{encoded_url}"

        print(request_url)
        response = requests.get(request_url)

        print(response.status_code)
        print(response.content)

        response_data = response.json
        print(response_data)
