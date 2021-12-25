# File for general-purpose commands
# Command dosent require any permission

# Commands and error handling goes to the same file

import json
from discord.ext import commands
from discord.ext.commands import Context
from discord.ext.commands.bot import Bot

def setup(bot: Bot):
    bot.add_cog(commandsCommon())

class commandsCommon(commands.Cog):
    # Afaik commands work without constructor
    # unless we need self.Bot variable for some reson
    # if thats the case then uncomment it
    #
    # def __init__(self, bot: Bot):
    #     self.bot = bot
    
    # ========================================
    # Hello command
    # usage: hello
    # returns a massage saying "hello world"
    @commands.command(
        name = "hello",
        help = "hello",
        description = "Returns a message saying \"hello world\""
    )
    async def hello(self, ctx: Context):
        await ctx.send("hello world")
    # ========================================

    # ========================================
    # Echo command
    # usage: echo [arg]
    # returns a message of the arg
    @commands.command(
        name = "echo",
        help = "echo [arg]",
        description = "Returns a message of the arg" # change this i cannot England
    )
    async def echo(self, ctx: Context, *, args):
        await ctx.send(args)

    # Error handler
    @echo.error
    async def echo_error(self, ctx: Context, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("No arguments found")
    # ========================================

    # ========================================
    # General Helper functinos
    # ========================================

    # any general helper function at the class level goes here
    # e.g.
    #
    # def i_love_blonde_loli(self):
    #   print("8-yo blonde loli saigo!")