# File for playing music, managing queue etc.
# Command dosent require any permission

# Import from discord
from discord.ext import commands
from discord.ext.commands.bot import Bot
from discord.ext.commands.context import Context

def setup(bot: Bot):
    bot.add_cog(commandsMusick())

class commandsMusick(commands.Cog, name = "Music"):
    @commands.command(name = "play")
    async def play(self, ctx: Context):
        await ctx.send("command triggered")