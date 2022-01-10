# File for general-purpose commands
# Command dosent require any permission

# Commands and error handling goes to the same file

# Imports from discord
import discord as discord
from discord.ext import commands
from discord.ext.commands import Context
from discord.ext.commands.bot import Bot
from discord.embeds import Embed
from discord import Spotify

# Import for Youtube-Search fnc (.yt)
from youtubesearchpython.__future__ import VideosSearch

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
        videosSearch = VideosSearch(args, limit = 2)
        videosResult = await videosSearch.next()
        # Sends link
        await ctx.send(videosResult['result'][0]['link'])
    # ========================================


    # This shit cool bruh - Henry 7/1/2022 19:26 HKT
    #
    # ========================================
    # Spotify Sesh
    # usage: spotify [str]
    # Returns data on a user's spotify sesh
    @commands.command(
        name = "spotify",
        help = "spotify [user]",
        description = "Returns data on a user's spotify sesh"
    )
    async def spotify(self, ctx: Context, user: discord.Member=None):
        if user == None: 
            user = ctx.author
        elif user.bot:
            await ctx.send(f"Sorry, `{user.name}` is a bot 🤖")
            return
        # Checks if the user has an activity at the moment
        if user.activities:
            # Accesses the user's activities (not just Spotify)
            for activity in user.activities:
                if isinstance(activity, Spotify):
                    # Simplify {duration} into h:mm:ss
                    duration = str(activity.duration)
                    final_dur = duration[0:7]
                    embed_msg = self.spawn_embed(ctx, title = f"🎧`{user.name}` is listening to:")
                    embed_msg.description = (
                        f"Title: `{activity.title}`\n"
                        f"Artist(s): `{activity.artist}`\n"
                        f"Album: `{activity.album}`\n"
                        f"Duration: `{final_dur}`"
                    )
                    await ctx.send(embed = embed_msg)
                    # await ctx.send(f"`{user.name}` is listening to `{activity.title}` by `{activity.artist}` in the album `{activity.album}`, on Spotify")
                    # 🎶 🎧
                    return
                # # FOR FURTHER EXAPNSION:
                # elif isinstance(activity, Game):
                    # print("AYYEEEEEEE")
                    # return

        await ctx.send(f"❌ **`{user.name}` is not in a session right now**")
        return


    # ========================================
    # General Helper functinos
    # ========================================

    # any general helper function at the class level goes here
    # e.g.
    #
    # def i_love_blonde_loli(self):
    #   print("8-yo blonde loli saigo!")

    # ========================================
    # Spawn an embed template
    def spawn_embed(self, ctx: Context, title: str):
        embed_msg = Embed(
            colour = 0xc27c0e,
            title = title
        )

        embed_msg.set_author(
            name = ctx.author.display_name,
            icon_url = ctx.author.avatar_url
        )

        return embed_msg
    # ========================================