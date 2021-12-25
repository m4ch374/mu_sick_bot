from typing import Mapping
from discord.ext import commands
from discord.ext.commands.help import HelpCommand

class customHelpCmd(commands.HelpCommand):

    # Initialize the HelpCommand class
    def __init__(self):
        HelpCommand.__init__(self)

    # Triggered if user only type "help"
    async def send_bot_help(self, mapping: Mapping):
        cmd_list = '\n'.join(['\n'.join(cmd.name for cmd in mapping[cogs]) for cogs in mapping])
        await self.get_destination().send(f"{cmd_list}")