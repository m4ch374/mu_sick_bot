# System imports
from typing import Mapping
from itertools import chain
import discord

# Discord imports
from discord.ext import commands
from discord import Embed
from discord.ext.commands import Command, CommandError
from discord.ext.commands.errors import CommandNotFound
from discord.ext.commands.help import HelpCommand

class customHelpCmd(commands.HelpCommand):

    # Initialize the HelpCommand class
    def __init__(self):
        HelpCommand.__init__(self)

    # ========================================
    # Triggered when user type help only
    # i.e. <prefix> help
    # Returns an embed containing a list of commands
    async def send_bot_help(self, mapping: Mapping):
        # Get a list of the commands
        cmd_list = list(chain.from_iterable(mapping[cogs] for cogs in mapping))

        embed_msg = self.spawn_help_template(
            title = "Command List",
            desc = ("List of commands\n" +
                f"Type `{self.context.prefix}help [command]` for more info")
        )

        for cmd in cmd_list: 
            if cmd.name != 'help':
                value_str = f"Usage: `{self.context.prefix}{cmd.help}`"
                embed_msg.add_field(name = cmd.name, value = value_str, inline = False)

        await self.get_destination().send(embed = embed_msg)
    # ========================================

    # ========================================
    # Triggered when user type help [command]
    # i.e. <preifx> help [command]
    # Returns an embed with the description of the command
    # and command arguments
    async def send_command_help(self, command: Command):
        embed_msg = self.spawn_help_template(
            title = f"{command.name}",
            desc = f"Usage: `{self.context.prefix}{command.help}`"
        )

        await self.get_destination().send(embed = embed_msg)
    # ========================================

    # ========================================
    # Triggered when the inputted command does not exist
    # i.e. <prefix> help [command_not_in_cogs]
    # Returns an error message
    async def send_error_message(self, error: CommandError):
        arg_str = ' '.join(self.context.message.content.split(' ')[1:])
        embed_msg = self.spawn_help_template(
            title = "Command not found",
            desc = (f"`{arg_str}` does not exist\n\n" +
                f"Type: `{self.context.prefix}help` to get the list of commands")
        )

        await self.get_destination().send(embed = embed_msg)
    # ========================================

    # ========================================
    # General Helper functinos
    # ========================================
    
    # ========================================
    # Spawns an embed template
    # Template properties:
    #   color = purple
    #   author = bot
    def spawn_help_template(self, title: str, desc: str):
        embed = Embed(colour = 0x9b59b6, title = title, description = desc)
        embed.set_author(
            name = self.context.bot.user.name,
            icon_url = self.context.bot.user.avatar_url
        )

        return embed
    # ========================================