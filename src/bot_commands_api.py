# File for all commands that uses API
# Command dosent require any permission

# Import from system
from discord import file
import requests

# Imports form discord
from discord.ext import commands
from discord.embeds import Embed
from discord.ext.commands.bot import Bot
from discord.ext.commands.context import Context

def setup(bot: Bot):
    bot.add_cog(commandsAPI())

class commandsAPI(commands.Cog, name = "API"):
    # No need __init__() for now i think

    # ========================================
    # Covid command
    # Usage: covid Optional[country_slug]
    # Returns a summary of covid stats across the world
    @commands.command(
        name = "covid",
        help = "covid Optional[country_slug]",
        description = "Returns a summary of covid stats across the world"
    )
    async def covid(self, ctx: Context, country: str=None):
        async with ctx.typing():
            embed_msg = self.spawn_embed(ctx, title = "Covid Update")
            embed_msg.description = (f"For more info: `{ctx.prefix}covid [country_slug]`\n" + 
                "Click [here](https://gist.github.com/Eskimon/02bf9b656f52381bb8ddf194a9979a2c) to see the full list of country slugs")

            if country:
                country.lower()
                get_url = f"https://api.covid19api.com/live/country/{country}"
                data = requests.get(get_url).json()
                self.gen_covid_details(embed_msg, data, True)
            else:
                get_url = "https://api.covid19api.com/summary"
                data = requests.get(get_url).json()['Global']
                self.gen_covid_details(embed_msg, data, False)
            
        await ctx.send(embed = embed_msg)

    # Helper function, generates embed contents
    def gen_covid_details(self, embed_msg: Embed, data, is_country: bool):
        if data == None or len(data) == 0:
            embed_msg.add_field(
                name = "Error fetching data",
                value = "Did you input the correct country slug?"
            )
            return

        field_title = "● Global stats"
        lookup_list = ['TotalConfirmed', 'TotalDeaths', 'TotalRecovered', 'NewConfirmed']
        if is_country:
            lookup_list = ['Confirmed', 'Deaths', 'Recovered', 'Active']
            data = data[-1]
            field_title = f"● {data['Country']}"

        embed_msg.add_field(
            name = field_title,
            value = (
                f"> Confirmed: `{data[lookup_list[0]]}`\n" + 
                f"> Deaths: `{data[lookup_list[1]]}`\n" +
                f"> Recovered: `{data[lookup_list[2]]}`\n" +
                f"> Active: `{data[lookup_list[3]]}`"
            )
        )
        embed_msg.set_footer(text = f"Data as of: {data['Date']}")

    # ========================================

    # ========================================
    # General Helper Functions
    # ========================================

    # ========================================
    # Spawns an Embed template, author set as msg author
    # properties: title
    def spawn_embed(self, ctx: Context, title: str):
        embed_msg = Embed(color = 0x1abc9c, title = title)
        embed_msg.set_author(
            name = ctx.author.display_name,
            icon_url = ctx.author.avatar_url
        )

        return embed_msg
    # ========================================