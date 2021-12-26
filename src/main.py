#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""Malicious URL Checker: A simple Discord bot that passively checks URLs
    for untrustworthy sites."""


# Built-in Modules
from dotenv import load_dotenv
import logging
from os import getenv
from sys import exit
from typing import Union


# My Modules
from bot import DiscordBot
import info

__author__ = info.author
__copyright__ = info.copyright

__license__ = info.license
__version__ = info.version
__maintainer__ = info.maintainer
__email__ = info.email
__status__ = info.status

if __name__ == "__main__":

    # Discord Bot Tokens are read from an .env file
    # in the current working directory
    load_dotenv()

    # Init logging
    logger = logging.getLogger('discord')
    logger.setLevel(logging.INFO)

    msg_format = logging.Formatter(
        '[{asctime}] {levelname} {name}: {message}', style="{",
        datefmt=r'%Y-%m-%d %H:%M:%S %Z')

    # Create file logging
    file_handler = logging.FileHandler(filename='err.log',
                                       encoding='utf-8', mode='a')
    file_handler.setFormatter(msg_format)

    # Create console logging
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(msg_format)

    # Register file and console handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    TOKEN: Union[str, None] = getenv("DISCORD_TOKEN")
    API_KEY: Union[str, None] = getenv("API_KEY")

    # Quit if no token is found
    if TOKEN is None:
        logger.critical("No env \"DISCORD_TOKEN\" was found.")
        exit(1)

    # Quit if no Safe Browsing API key is found
    if API_KEY is None:
        logger.critical("No env \"API_KEY\" was found.")
        exit(1)

    client = DiscordBot(API_KEY)

    client.run(TOKEN)
