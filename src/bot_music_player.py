# File for playing music, managing queue etc.
# Command dosent require any permission

# Import from system
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
    async def play(self, ctx: Context, link: str):
        try:
            # youtube dl options
            ydl_opts = {
                'format': 'bestaudio/best',
                'extractaudio': True,
                'audioformat': 'ogg',
                'noplaylist': True
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                vid_info = ydl.extract_info(
                    url = link,
                    download = False
                )
        except Exception as e:
            traceback.print_exc()
            
            error_embed = self.spawn_error_embed(ctx, "Make sure your enter a valid link!")
            return await ctx.send(embed = error_embed)

        if ctx.author.voice == None:
            error_embed = self.spawn_error_embed(ctx, "Voice channel not found.")
            return await ctx.send(embed = error_embed)

        print(json.dumps(vid_info, indent = 4))
        vc = await ctx.author.voice.channel.connect()
        try:
            vc.play(
                FFmpegOpusAudio(
                    source = vid_info['formats'][0]['url'],
                    before_options = '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                    options = '-vn'
                )
            )
        except Exception as e:
            if ctx.voice_client != None:
                await ctx.voice_client.disconnect()

            error_embed = self.spawn_error_embed(ctx, e.args[0])
            return await ctx.send(embed = error_embed)
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