# File for all commands that uses API
# Command dosent require any permission

# Import from system
import json
import requests
import datetime
import traceback

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

            # Get data between time interval: yesterday - today
            data = ""
            today = datetime.date.today()
            yesterday = (today - datetime.timedelta(days = 1)).isoformat()
            if country:
                country = country.lower()
                get_url = f"https://api.covid19api.com/live/country/{country}/status/confirmed/date/{yesterday}T00:00:00Z"
                data = requests.get(get_url).json()
            else:
                get_url = f"https://api.covid19api.com/world?from={yesterday}T00:00:00Z&to={today}T00:00:00Z"
                data = requests.get(get_url).json()

            self.gen_covid_details(embed_msg, data, country)
            
        await ctx.send(embed = embed_msg)

    # Helper function, generates embed contents
    def gen_covid_details(self, embed_msg: Embed, data, is_country: bool):

        # If data is null or no item in data
        if data == None or len(data) == 0:
            embed_msg.add_field(
                name = "Error fetching data",
                value = "Did you input the correct country slug?"
            )
            return
        
        if is_country:
            self.gen_country_details(embed_msg, data)
        else:
            self.gen_global_details(embed_msg, data)

    # Helper function, generates country covid details
    def gen_country_details(self, embed_msg: Embed, data):
        lookup_list = ['Confirmed', 'Deaths', 'Recovered', 'Active']
        embed_msg.add_field(
            name = f"● {data[0]['Country']}",
            value = (
                f"> Confirmed: `{sum([item[lookup_list[0]] for item in data])}`\n" + 
                f"> Deaths: `{sum([item[lookup_list[1]] for item in data])}`\n" +
                f"> Recovered: `{sum([item[lookup_list[2]] for item in data])}`\n" +
                f"> Active: `{sum([item[lookup_list[3]] for item in data])}`"
            )
        )
        embed_msg.set_footer(text = f"Data might not be accurate | {data[0]['Date']}")

    # Helper function, generates global covid details
    def gen_global_details(self, embed_msg: Embed, data):
        lookup_list = ['TotalConfirmed', 'TotalDeaths', 'TotalRecovered', 'NewConfirmed']
        embed_msg.add_field(
            name = "● Global stats",
            value = (
                f"> Confirmed: `{data[0][lookup_list[0]]}`\n" + 
                f"> Deaths: `{data[0][lookup_list[1]]}`\n" +
                f"> Recovered: `{data[0][lookup_list[2]]}`\n" +
                f"> Active: `{data[0][lookup_list[3]]}`"
            )
        )
        embed_msg.set_footer(text = f"Data might not be accurate | {data[0]['Date']}")
    # ========================================

    # ========================================
    # Anime command
    # Usage: anime [title] Optional[offset]
    # Returns an embed containing the anime's info
    @commands.command(
        name = "anime",
        help = "anime [title]",
        description = "Returns an embed containing the anime's info"
    )
    async def anime(self, ctx: Context, *, args: str):
        embed_msg = await self.get_weeb_api_embed(ctx, args)

        await ctx.send(embed = embed_msg)
    # ========================================

    # ========================================
    # Manga command
    # Usage: manga [title] Optional[offset]
    # Returns an embed containing the manga's info
    @commands.command(
        name = "manga",
        help = "manga [title]",
        description = "Returns an embed containing the manga's info"
    )
    async def manga(self, ctx: Context, *, args: str):
        embed_msg = await self.get_weeb_api_embed(ctx, args)

        await ctx.send(embed = embed_msg)
    # ========================================

    # ========================================
    # Helper function for anime and manga cmd
    # ========================================

    # ========================================
    # Generate embed containing info of anime / manga
    # Returns an error embed if the process failed
    async def get_weeb_api_embed(self, ctx: Context, args: str):
        async with ctx.typing():
            try:
                embed_msg = self.gen_weeb_embed(ctx, args)
            except:
                traceback.print_exc()
                # Generate error embed
                embed_msg = self.spawn_embed(ctx, title = "Oops! An error occurred.")
                args = f"\"{args}\"" if '"' not in args else args
                embed_msg.description = (f"{ctx.command.name.capitalize()} not found\n" +
                    f"You might want to try: `{ctx.prefix}{ctx.command.name} {args}`")
        return embed_msg

    # ========================================
    # generate an embed containing info of anime / manga
    def gen_weeb_embed(self, ctx: Context, args: str):
        get_url = f"https://kitsu.io/api/edge/{ctx.command.name}?filter[text]={args}&page[limit]=1"
        data = requests.get(get_url).json()['data'][0]
        print(json.dumps(data, indent = 4))

        # Attributes
        attr = data['attributes']
        english_title = attr['titles']['en'] if 'en' in attr['titles'] else attr['titles']['en_jp']
        embed_msg = self.spawn_embed(ctx, title = f"{english_title} | {attr['titles']['ja_jp']}")
        embed_msg.add_field(name = "Release Date", value = f"> {attr['startDate']}")
        embed_msg.add_field(name = "End Date", value = f"> {attr['endDate']}")
        embed_msg.add_field(name = "Status", value = f"> {attr['status']}")

        # Episodes and runtime
        if ctx.command.name == "anime":
            embed_msg.add_field(name = "Episodes", value = f"> {attr['episodeCount']}")
            embed_msg.add_field(name = "Runtime", value = f"> {attr['episodeLength']}")
            embed_msg.add_field(name = "Show Type", value = f"> {attr['showType']}")

        # Genres and Ratings and nsfw
        genre_list = self.get_genre(data)
        embed_msg.add_field(name = "Genre", value = f"> {', '.join(genre_list)}")
        embed_msg.add_field(name = "NSFW", value = "> {}".format(attr['nsfw'] if 'nsfw' in attr else "N/A"))
        embed_msg.add_field(name = "Ratings", value = f"> {attr['averageRating']}")

        # Description
        embed_msg.add_field(name = "Intro", value = f"{attr['description'][:300]}...")

        # Images
        if attr['posterImage'] != None:
            embed_msg.set_thumbnail(url = attr['posterImage']['medium'])

        if attr['coverImage'] != None:
            embed_msg.set_image(url = attr['coverImage']['original'])

        # Footer
        embed_msg.set_footer(
            text = (f"Not the result you expected? Type {ctx.prefix}help {ctx.command.name}"),
            icon_url = ctx.bot.user.avatar_url
        )

        return embed_msg

    # Helper function, returns the genre of the anime
    # Returns list only contains "N/A" if there are no genres
    def get_genre(self, data):
        get_url = data['relationships']['genres']['links']['related']
        genres = requests.get(get_url).json()
        print(json.dumps(genres, indent = 4))
        
        if len(genres['data']) == 0:
            return ["N/A"]
        else:
            return [item['attributes']['name'] for item in genres['data']]
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