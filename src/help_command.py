# System imports
from typing import Mapping

# Discord imports
from discord.ext import commands
from discord import Embed
from discord.ext.commands import Command
from discord.ext.commands import errors
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
        # Get a list of the commands for each cogs
        cog_list = [cogs for cogs in mapping if cogs != None and len(cogs.get_commands()) > 0]

        embed_msg = self.spawn_help_template(
            title = "Command List",
            desc = ("List of commands\n" +
                f"Type `{self.context.prefix}help [command]` for more info")
        )

        char = '`'
        for cogs in cog_list:
            embed_msg.add_field(
                name = f"**● {cogs.qualified_name}**",
                # expected output: `echo` `hello`
                value = f"> {' '.join([char + cmd.qualified_name + char for cmd in mapping[cogs]])}",
                inline = False
            )

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
            desc = f"{command.description}\n\n" + f"Usage:\n> {self.context.prefix}{command.help}"
        )

        await self.get_destination().send(embed = embed_msg)
    # ========================================

    # ========================================
    # Triggered when user type help [cog]
    # i.e. <prefix> help [cog]
    # Returns an embed with the commands that the cog contains
    async def send_cog_help(self, cog: commands.Cog):
        cmd_list = cog.get_commands()
        if len(cmd_list) == 0:
            return await self.send_error_message(errors.CommandNotFound)

        embed_msg = self.spawn_help_template(
            title = f"{cog.qualified_name}",
            desc = f"{cog.qualified_name} has the following commands:"
        )
        for cmd in cmd_list:
            embed_msg.add_field(
                name = f"**● {cmd.qualified_name}**",
                value = f"Usage:\n> {self.context.prefix}{cmd.help}",
                inline = False
            )

        await self.get_destination().send(embed = embed_msg)
    # ========================================

    # ========================================
    # Triggered when the inputted command does not exist
    # i.e. <prefix> help [command_not_in_cogs]
    # Returns an error message
    async def send_error_message(self, error: errors):
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
    def spawn_help_template(self, title: str, desc: str=None):
        embed = Embed(colour = 0x9b59b6, title = title, description = desc)
        embed.set_author(
            name = "I see you're a bit lost 👴🏻",
            icon_url = self.context.bot.user.avatar_url
        )

        return embed
    # ========================================