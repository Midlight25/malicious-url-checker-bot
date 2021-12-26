# -*- coding: utf-8 -*-

"""Event based programming for the bot"""

# System Libraries
import json
import logging
import re

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

    API_URL: str = r"https://safebrowsing.googleapis.com/v4/threatMatches:find"

    def __init__(self, api_key: str):
        super().__init__()
        self.url = f'{DiscordBot.API_URL}?key={api_key}'

    async def on_ready(self):
        DiscordBot.LOGGER.info("Discord Bot is ready to go.")

    async def on_message(self, message):
        if message.author == self.user:
            return

        # Scan message and check for links in message
        matches = re.findall(DiscordBot.URL_RE, message.content)

        # Iterate through links found in message
        for match in matches:
            print(self.check_url_status(match))

    async def on_error(self, event, *args, **kwargs):

        if event == "on_message":
            DiscordBot.LOGGER.error(
                f"Unhandled Message: \"{args[0].content}\" {args[0]}")
        else:
            raise

    def check_url_status(self, url: str):
        """API Request to Safe Browsing API for trustworthiness"""

        request_body = {
            "client": {
                "clientId": info.name,
                "clientVersion": info.version
            },
            "threatInfo": {
                "threatTypes": ["THREAT_TYPE_UNSPECIFIED"],
                "platformTypes": ["PLATFORM_TYPE_UNSPECIFIED"],
                "threatEntryTypes": ["THREAT_ENTRY_TYPE_UNSPECIFIED"],
                "threatEntries": [
                    {"url": url}
                ]
            }
        }

        response = requests.post(
            self.url, json=request_body)

        # response_data = json.loads(response.json())

        # print(response_data)

        return response
