# We could use classes for organizing different types of
# commands for the discord bot
from discord.ext import commands
from discord.ext.commands import Context

class commandsCommon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx: Context):
        await ctx.send("hello world")

    @commands.command()
    async def echo(self, ctx: Context, *, args):
        await ctx.send(args)
