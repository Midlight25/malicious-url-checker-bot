# bot.py
# -*- coding: utf-8 -*-

"""Bot logic as class"""

# System Libraries
import logging
import re

# Third-Party Modules
from discord.ext import commands
from discord import Intents, Activity, ActivityType, Embed
import requests
from pysafebrowsing import SafeBrowsing

# My Modules
import info


class URLBot(commands.Bot):
    """Discord Bot that scans messages for URLs and then evaluates if they
        are trustworthy"""

    # Regular Expression for finding links
    URL_RE: str = r'(?:http(?:s)?:\/\/)?.(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]' + \
        r'{2,256}\.[a-z]{2,6}\b(?:[-a-zA-Z0-9@:%_\+.~#?&//=]*)'

    # Standard logger that all instances report to. 'discord:bot"
    LOGGER = logging.getLogger('discord').getChild('bot')

    API_URL: str = r"https://safebrowsing.googleapis.com/v4/threatMatches:find"

    def __init__(self, command_prefix, api_key: str):
        """Configure the bot by passing the configs
            to the parent class."""

        # Configuring intents to filter out events
        # that we won't process with the bot.
        intents = Intents(messages=True, guild_messages=True,
                          guilds=True)

        # Configuring Activity
        currently = Activity(
            name="y'alls links",
            type=ActivityType.watching,
            state='Scanning',
            details="Passively scanning messages for URLs.")

        super().__init__(command_prefix=command_prefix,
                         intents=intents, activity=currently)

        # Build custom URL using supplied API key
        # TODO: Convert to using POST Request instead of GET request
        self.url: str = f"{URLBot.API_URL}?key={api_key}"
        self.api = SafeBrowsing(api_key)

    async def on_ready(self):
        # TODO: Add activity update code to indicate bot readyness.
        URLBot.LOGGER.info("Discord Bot is ready to go.")

    async def on_message(self, message):

        # Catch, do not want bot to process messages
        # generated by itself.
        if message.author == self.user:
            return

        # Scan message and check for links in message using REGEX
        matches = re.findall(URLBot.URL_RE, message.content)
        for match in matches:
            match_info = self.get_url_info(match)
            # if match_info is not None and match_info['dangerous']:
            # url_embed = self.generate_embed(match_info)
            await message.channel.send(content=match_info)

        # TODO Make the message a rich embed instead of just text.

    # async def on_error(self, event, *args, **kwargs):

    #     if event == "on_message":
    #         # Error triggered by on_message event.
    #         # TODO: Make this more descriptive about what error occured
    #         # with this message.
    #         URLBot.LOGGER.error(
    #             f"Unhandled Message: \"{args[0].content}\" {args[0]}")
    #     else:
    #         raise

    def get_url_info(self, url: str):
        """Get information about URL using API Request to Safe Browsing API
            and report back as object url trustworthiness"""

        url_data = self.api.lookup_url(url)

        # # Interpret Results
        # if url_data['success']:
        #     results = {
        #         "url": url,
        #         "dangerous": url_data['unsafe'],
        #         "risk_score": url_data['risk_score'],
        #         "tags": [tag for tag in URLBot.TAGS if url_data[tag]]
        #     }

        #     return results
        # else:
        #     # TODO Make this raise an error instead
        #     return None

        return url_data

    def generate_embed(self, url_dict) -> Embed:
        """Generate an embed from url data and return"""
        # TODO Change url_dict to object for holding URL data.

        embed = Embed(
            title="Malicious URL Check Results",
            description='Here are the results from our investigation.')

        embed.add_field(
            name="URL",
            value=url_dict['url'],
            inline=False)
        embed.add_field(
            name="Risk Percent",
            value=f"{url_dict['risk_score']:0.1f} %")
        embed.add_field(
            name='Tags', value=", ".join(url_dict['tags']))
        embed.set_footer(text="Definitely not provided by Google")

        return embed
