# File for general-purpose commands
# Command dosent require any permission

# Commands and error handling goes to the same file

# Imports from discord
from discord.ext import commands
from discord.ext.commands import Context
from discord.ext.commands.bot import Bot

def setup(bot: Bot):
    bot.add_cog(commandsCommon())

class commandsCommon(commands.Cog, name = "Common commands"):
    # Afaik commands work without constructor
    # unless we need self.Bot variable for some reson
    # if thats the case then uncomment it
    #
    # def __init__(self, bot: Bot):
    #     self.bot = bot
    
    # ========================================
    # Hello command
    # usage: hello
    # returns a massage saying "hello world" * n
    @commands.command(
        name = "hello",
        help = "hello [int] (optional)",
        description = "Returns a message saying \"hello world\" as many times as the int entered"
    )
    @commands.cooldown(rate = 4, per = 60, type = commands.BucketType.user)
    async def hello(self, ctx: Context, num: int = 1):
        if num <= 10 and num > 0:
            await ctx.send("Hello World\n" * num)
        elif num == 0:
            return
        else: 
            await ctx.send(f"{num} is not between 0 and 10!")
    # ========================================

    # ========================================
    # Echo command
    # usage: echo [arg]
    # returns a message of the arg
    @commands.command(
        name = "echo",
        help = "echo [arg]",
        description = "Returns the user's exact same input" # change this i cannot England XDDD
    )
    async def echo(self, ctx: Context, *, args):
        await ctx.send(args)

    # Error handler
    @echo.error
    async def echo_error(self, ctx: Context, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("No additional arguments found. Run '.help [cmd]' for further info")
    # ========================================


    # ========================================
    # Random command
    # usage: rand
    # Selects a random [common] command (not inclu. "rand")
    @commands.command(
        name = "rand",
        help = "rand",
        description = "Selects a random [common] cmd that doesn't require an arg"
    )
    async def rand(self, ctx: Context):
        await ctx.send(None)

    # ========================================
    # General Helper functinos
    # ========================================

    # any general helper function at the class level goes here
    # e.g.
    #
    # def i_love_blonde_loli(self):
    #   print("8-yo blonde loli saigo!")