# System imports
from typing import Mapping
from itertools import chain
import discord

# Discord imports
from discord.ext import commands
from discord import Embed
from discord.ext.commands.help import HelpCommand
from discord.ext.commands.bot import Bot

class customHelpCmd(commands.HelpCommand):

    # Initialize the HelpCommand class
    def __init__(self):
        HelpCommand.__init__(self)

    # Triggered if user only type "help"
    async def send_bot_help(self, mapping: Mapping):
        # Get a list of the commands
        cmd_list = list(chain.from_iterable(mapping[cogs] for cogs in mapping))

        embed_msg = Embed(
            title = "Command List",
            description = "List of commands, type help [command] for more info",
            colour = 0x9b59b6
        )

        embed_msg.set_author(
            name = self.context.bot.user.name,
            icon_url = self.context.bot.user.avatar_url
        )

        for cmd in cmd_list: 
            if cmd.name != 'help':
                value_str = f"Usage: {cmd.help}"
                embed_msg.add_field(name = cmd.name, value = value_str, inline = False)

        await self.get_destination().send(embed = embed_msg)