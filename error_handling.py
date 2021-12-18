from discord.ext import commands
from discord.ext.commands import Context

import bot_commands

class commandsErrorCommon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bot_commands.commandsCommon.echo.error
    async def echo_error(self, ctx: Context, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("No arguments found")