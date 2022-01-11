# File for general-purpose commands
# Command dosent require any permission

# Imports from discord
import discord as discord
from discord.ext import commands
from discord.ext.commands import Context
from discord.ext.commands.bot import Bot
from discord.embeds import Embed

# Additional imports
from youtubesearchpython.__future__ import VideosSearch
from datetime import timedelta

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
        description = "Returns a message saying \"hello world\" as many times as the [int] entered (if any)"
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
    # ========================================

    # ========================================
    # YouTube search & return link command
    # usage: yt [str]
    # Finds top result of the "str" on youtube and returns the link (does NOT add to queue, nor Play)
    @commands.command(
        name = "yt",
        help = "yt [arg]",
        description = "Finds YouTube's top search result of the 'arg' and simply returns the link"
    )
    async def yt(self, ctx: Context, *, args):
        # if len(args) == 0:
        videosSearch = VideosSearch(args, limit = 5)
        videosResult = await videosSearch.next()

        embed_msg = self.spawn_embed(ctx, title = "Results")

        for i in range(len(videosResult['result'])):
            embed_msg.add_field(
                name = f"{i + 1}. {videosResult['result'][i]['title']}",
                value = videosResult['result'][i]['link'],
                inline = False
            )

        # Sends link
        await ctx.send(embed = embed_msg)
    # ========================================


    # This shit cool bruh - Henry 7/1/2022 19:26 HKT
    #
    # ========================================
    # Discord activity data
    # usage: sesh [user]
    # Returns info on a user's discord activity. One embed per activityType.
    @commands.command(
        name = "sesh",
        help = "sesh [user]",
        description = "Returns data on a user's discord activity"
    )
    async def sesh(self, ctx: Context, user: discord.Member=None):
        # Defaults 'user' to author, if no arg is entered
        user = ctx.author if user == None else user

        # Show error message if its a bot
        if user.bot:
            return await ctx.send(f"Sorry, `{user.name}` is a bot 🤖")

        # Remove custom activities
        activity_list = ([act for act in user.activities 
            if str(act.type) != 'ActivityType.custom'])

        # When user.activities is niche
        if len(activity_list) == 0:
            return await ctx.send(f"❌ **`{user.name}` is not in a session right now**")
        
        for activity in activity_list:
            # Activity is Spotify (.listening)
            if isinstance(activity, discord.Spotify):
                embed_msg = self.get_spotify_embed(ctx, user, activity)

            # Activity is a Game (.playing)
            elif isinstance(activity, discord.Game) or isinstance(activity.type, type(discord.ActivityType.playing)):
                embed_msg = self.get_game_embed(ctx, user, activity)

            # Sends embed msg
            await ctx.send(embed = embed_msg)

    # Helper function
    def get_spotify_embed(self, ctx: Context, user: discord.Member , activity: discord.Spotify):
        embed_msg = self.spawn_embed(ctx, title = f"🎧 `{user.name}` is listening to:")
        # 🎶 🎧
        # ========================================
        # LEGACY
        # ========================================
        # embed_msg.description = (
        #     f"Title: `{activity.title}`\n"
        #     f"Artist(s): `{activity.artist}`\n"
        #     f"Album: `{activity.album}`\n"
        #     f"Duration: `{final_dur}`\n"
        #     f"**on {activity.name}**"
        # )
        # ========================================
        embed_msg.add_field(name = 'Name', value = f"> {activity.title}")
        embed_msg.add_field(name = 'Artist(s)', value = f"> {activity.artist}") 
        embed_msg.add_field(name = 'Album', value = f"> {activity.album}")
        # Simplify {duration} into h:mm:ss
        duration = str(activity.duration)
        final_dur = duration[0:7]
        embed_msg.add_field(name = 'Duration', value = f"> {final_dur}")
        
        embed_msg.set_thumbnail(url = activity.album_cover_url)
        spotify_icon_url = "https://www.freepnglogos.com/uploads/spotify-logo-png/file-spotify-logo-png-4.png"
        embed_msg.set_footer(text = f"on {activity.name}", icon_url = spotify_icon_url)
        # Set to Spotify's colour
        embed_msg.colour = activity.color

        return embed_msg

    def get_game_embed(self, ctx: Context, user: discord.Member, activity):
        embed_msg = self.spawn_embed(ctx, title = f"🎮 `{user.name}` is playing:")
        embed_msg.add_field(name = 'Name', value = f"> {activity.name}", inline = False)
        # Convert UTC time into local time (AEDT) i.e +11hrs
        if activity.start is not None:
            aedt_start = activity.start + timedelta(hours = 11)
            start_str = str(aedt_start)
            simp_start = start_str[10:19]
            embed_msg.add_field(name = 'Started', value = f"> {simp_start} (AEDT)", inline = False) 

        return embed_msg
    # ========================================

    # ========================================
    # General Helper functinos
    # ========================================

    # any general helper function at the class level goes here
    # e.g.
    #
    # def i_love_blonde_loli(self):
    #   print("18-yo blonde loli saigo!")

    # ========================================
    # Spawn an embed template
    def spawn_embed(self, ctx: Context, title: str):
        embed_msg = Embed(
            colour = 0x7289da,
            title = title
        )

        embed_msg.set_author(
            name = ctx.author.display_name,
            icon_url = ctx.author.avatar_url
        )

        return embed_msg
    # ========================================
