# We could use classes for organizing different types of
# commands for the discord bot

# Error handling goes to the same file
import json
from discord.ext import commands
from discord.ext.commands import Context
from discord.ext.commands.bot import Bot

def setup(bot: Bot):
    bot.add_cog(commandsCommon(bot))
    bot.add_cog(commandsRestricted(bot))

class commandsCommon(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    # Hello command
    # usage: hello
    # returns a massage saying "hello world"
    @commands.command(name = "hello")
    async def hello(self, ctx: Context):
        await ctx.send("hello world")

    # ========
    # Echo command
    # usage: echo [arg]
    # returns a message of the arg
    @commands.command(name = "echo")
    async def echo(self, ctx: Context, *, args):
        await ctx.send(args)

    # Error handler
    @echo.error
    async def echo_error(self, ctx: Context, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("No arguments found")
    # ========

class commandsRestricted(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    # ========
    # Set prefix 
    # usage: setPrefix [new_prefix]
    # sets prefix and return a message
    @commands.command(name = "setPrefix")
    async def setPrefix(self, ctx: Context, *, new_prefix: str):
        # Remove head and tail whitespace
        new_prefix.strip()

        if "<@!" in new_prefix:
            return await ctx.send("Cannot set prefix as user")

        #Read in json file
        f = open('../settings/settings.json', "r+")
        data = json.load(f)

        #Set new prefix
        data['Prefix']['defaultPrefix'] = new_prefix
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()

        #close json file
        f.close()
        
        self.bot.command_prefix = new_prefix
        await ctx.send(f"Prefix updated to {new_prefix}")

    # error handling
    @setPrefix.error
    async def setPrefix_error(self, ctx: Context, error):
        output_str = ""

        if isinstance(error, commands.MissingRequiredArgument):
            output_str = "Error: too little arguments\n"
        else:
            output_str = "Error: unidentified error\n"
        
        output_str += "\nUsage: setPrefix [new_prefix]"
        await ctx.send(output_str)
    # ========
