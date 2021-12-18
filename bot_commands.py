# We could use classes for organizing different types of
# commands for the discord bot
from discord.ext import commands

class commandsCommon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx):
        await ctx.send("hello world")

