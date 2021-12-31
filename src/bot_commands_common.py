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
    ## NOTE: When you do ".hello hi", the type-check fails, so it goes straight to the bot_logger errors, NOT the 'except' block.
    ##       ALSO, u dont need the 'except' block
    async def hello(self, ctx: Context, num: int = 1):
        try:
            if num <= 10 and num > 0:
                await ctx.send("Hello World\n" * num)
            elif num == 0:
                return
            else: 
                await ctx.send(f"{num} is not between 0 and 10!") 
        except:
            await ctx.send("Please check you have entered the correct format. Run '.help [cmd]' for further info!")
            ## ADD A COOLDOWN !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
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
            await ctx.send("No additional arguments found. Run '.help [cmd]' for further info")
    # ========================================


    # ========================================
    # Random command
    # usage: rand
    # Selects a random [common] command (not inclu. "rand")
    @commands.command(
        name = "rand",
        help = "rand",
        description = "Selects a random [common] command"
    )
    async def rand(self, ctx: Context):
        await ctx.send(args)

    # ========================================
    # General Helper functinos
    # ========================================

    # any general helper function at the class level goes here
    # e.g.
    #
    # def i_love_blonde_loli(self):
    #   print("8-yo blonde loli saigo!")