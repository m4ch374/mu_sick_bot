# File for playing music, managing queue etc.
# Command dosent require any permission

# Import from system
import asyncio
import json
import traceback

# Import from ytdl
import youtube_dl

# Import from discord
from discord.ext import commands
from discord.ext.commands.bot import Bot
from discord.ext.commands.context import Context
from discord.embeds import Embed
from discord import FFmpegOpusAudio

def setup(bot: Bot):
    bot.add_cog(commandsMusick())

class commandsMusick(commands.Cog, name = "Music"):

    # ========================================
    # Play command
    # Usage: play [url]
    # Plays a youtube video on discord
    @commands.command(
        name = "play",
        help = "play [url]",
        description = "Plays a youtube vido on discord"
    )
    async def play(self, ctx: Context, *, link: str):
        link = link.strip(" <>")
        
        try:
            # youtube dl options
            ydl_opts = {
                'format': 'bestaudio/best',
                'extractaudio': True,
                'audioformat': 'ogg',
                'noplaylist': True,
                'simulate': True,
                'default_search': 'ytsearch1'
            }
            await self.process_play_audio(ctx, link, ydl_opts)
            
        except Exception as e:
            if ctx.voice_client != None:
                await ctx.voice_client.disconnect()

            error_embed = self.spawn_error_embed(ctx, e.args[0])
            return await ctx.send(embed = error_embed)

    # Wrapper for playing the youtube link
    async def process_play_audio(self, ctx: Context, link: str, ydl_opts):
        vid_info = await self.get_vdo_info(ctx, link, ydl_opts)

        # Error checking
        if ctx.author.voice == None:
            error_embed = self.spawn_error_embed(ctx, "Voice channel not found.")
            return await ctx.send(embed = error_embed)

        # Connect and play audio
        print(json.dumps(vid_info, indent = 4))
        vc = await ctx.author.voice.channel.connect()

        song_src = await FFmpegOpusAudio.from_probe(
            source = vid_info['formats'][0]['url'],
            before_options = '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            options = '-vn'
        )
        vc.play(
            song_src,
            after = lambda e: self.music_after(ctx)
        )

    # Returns video info in json string, prints error message if failed
    async def get_vdo_info(self, ctx: Context, link: str, ydl_opts):
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            vid_info = ydl.extract_info(url = link)

        return vid_info
    
    # Funtion to run after music is finished
    def music_after(self, ctx: Context):
        asyncio.run_coroutine_threadsafe(ctx.send("finished playing"), ctx.bot.loop)
        asyncio.run_coroutine_threadsafe(ctx.voice_client.disconnect(), ctx.bot.loop)

    # ========================================

    # ========================================
    # disconnect command
    # Usage: disconnect
    # Disconnects from a voice channel
    @commands.command(
        name = "disconnect",
        help = "disconnect",
        description = "Disconnects from a voice channel"
    )
    async def disconnect(self, ctx: Context):
        if ctx.voice_client == None:
            error_embed = self.spawn_error_embed(ctx, "Not in a voice channel.")
            return await ctx.send(embed = error_embed)

        await ctx.voice_client.disconnect()

    # ========================================
    # General helper function
    # ========================================

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

    # ========================================
    # Spawns an error embed
    def spawn_error_embed(self, ctx: Context, description: str):
        embed_msg = self.spawn_embed(ctx, "Oops! An error occurred.")
        embed_msg.description = description
        return embed_msg
    # ========================================