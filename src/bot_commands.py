# We could use classes for organizing different types of
# commands for the discord bot

# Error handling goes to the same file

from discord.ext import commands
from discord.ext.commands import Context
from discord.ext.commands.bot import Bot

def setup(bot: Bot):
    bot.add_cog(commandsCommon(bot))

class commandsCommon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Hello command
    # usage: hello
    # returns a massage saying "hello world"
    @commands.command()
    async def hello(self, ctx: Context):
        await ctx.send("hello world")

    # ========
    # Echo command
    # usage: echo [arg]
    # returns a message of the arg
    @commands.command()
    async def echo(self, ctx: Context, *, args):
        await ctx.send(args)

    # Error handler
    @echo.error
    async def echo_error(self, ctx: Context, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("No arguments found")
    # ========
