# File for all commands that uses API
# Command dosent require any permission

# Import from system
import requests

# Imports form discord
from discord.ext import commands
from discord.ext.commands.bot import Bot
from discord.ext.commands.context import Context

def setup(bot: Bot):
    bot.add_cog(commandsAPI())

class commandsAPI(commands.Cog, name = "API"):
    # No need __init__() for now i think
    @commands.command(
        name = "covid",
        help = "covid Optional[country]",
        description = "Returns a summary of covid stats across the world"
    )
    async def covid(self, ctx: Context, country: str=None):
        get_url = "https://api.covid19api.com/summary"
        data = requests.get(get_url).json()

        await ctx.send(f"Global confirmed: {data['Global']['TotalConfirmed']}")
