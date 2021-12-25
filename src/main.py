#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""Malicious URL Checker: A simple Discord bot that passively checks URLs
    for untrustworthy sites."""

# Built-in Modules
import logging
from os import getenv
from sys import exit
from typing import Union

# Third-Party Modules
import discord

from dotenv import load_dotenv

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

    # Quit if no token is found
    if TOKEN is None:
        logger.critical(
            "No env \"DISCORD_TOKEN\" was found.")
        exit(1)

    client: discord.Client = discord.Client()

    @client.event
    async def on_ready():
        logger.info("Discord Bot is ready to go.")

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        if message.content == 'raise-exception':
            raise discord.DiscordException

    @client.event
    async def on_error(event, *args, **kwargs):

        if event == "on_message":
            logger.error(
                f"Unhandled Message: \"{args[0].content}\" {args[0]}")
        else:
            raise

    client.run(TOKEN)
