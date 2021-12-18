# File for handling errors in bot_command
from discord.ext import commands
from discord.ext.commands import Context
from discord.ext.commands.bot import Bot

# imports from own files
import bot_commands

def setup(bot: Bot):
    bot.add_cog(commandsErrorCommon(bot))

class commandsErrorCommon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bot_commands.commandsCommon.echo.error
    async def echo_error(self, ctx: Context, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("No arguments found")