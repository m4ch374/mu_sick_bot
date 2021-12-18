# We could use classes for organizing different types of
# commands for the discord bot
from discord.ext import commands
from discord.ext.commands import Context
from discord.ext.commands.bot import Bot

# def setup(bot: Bot):
#     bot.add_cog(commandsCommon(bot))

class commandsCommon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx: Context):
        await ctx.send("hello world")

    @commands.command()
    async def echo(self, ctx: Context, *, args):
        await ctx.send(args)

    # @echo.error
    # async def echo_error(self, ctx: Context, error):
    #     if isinstance(error, commands.MissingRequiredArgument):
    #         await ctx.send("No arguments found")
