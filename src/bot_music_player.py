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
    # Initalizer
    def __init__(self):
        self.queue = musicQueue()

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
                'default_search': 'ytsearch1',
                'preferffmpeg': True
            }
            await self.process_play_audio(ctx, link, ydl_opts)

        except Exception as e:
            if ctx.voice_client != None and type(e).__name__ != "KeyError":
                self.queue.clean()
                await ctx.voice_client.disconnect()

            traceback.print_exc()

            error_embed = self.spawn_error_embed(ctx, e.args[0])
            return await ctx.send(embed = error_embed)

    # Wrapper for playing the youtube link
    async def process_play_audio(self, ctx: Context, link: str, ydl_opts):
        self.queue_vdo_info(link, ydl_opts)

        # Error checking
        if ctx.author.voice == None:
            error_embed = self.spawn_error_embed(ctx, "Voice channel not found.")
            return await ctx.send(embed = error_embed)

        # Connect and play audio
        vc = await ctx.author.voice.channel.connect() if not ctx.voice_client else ctx.voice_client

        await self.play_audio(ctx, vc)

    # Returns video info in json string, prints error message if failed
    def queue_vdo_info(self, link: str, ydl_opts):
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            vid_info = ydl.extract_info(url = link, download = False)

        print(json.dumps(vid_info, indent = 4))
        self.queue.queue(vid_info)

    async def play_audio(self, ctx: Context, vc):
        if not self.queue.empty() and not vc.is_playing():
            await self.np(ctx)

            vid_meta = self.queue.first()

            song_src = await FFmpegOpusAudio.from_probe(
                source = vid_meta.url,
                before_options = '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                options = '-vn'
            )
            vc.play(
                song_src,
                after = lambda e: self.music_after(ctx)
            )
        else :
            embed_msg = self.spawn_embed(ctx, title = "Added to quque")
            embed_msg.description = f"Queued `{self.queue.last().title}`"
            await ctx.send(embed = embed_msg)
    
    # Funtion to run after music is finished
    def music_after(self, ctx: Context):
        self.queue.dequeue()

        if self.queue.empty():
            asyncio.run_coroutine_threadsafe(ctx.send("finished playing"), ctx.bot.loop)
            asyncio.run_coroutine_threadsafe(ctx.voice_client.disconnect(), ctx.bot.loop)
        else:
            asyncio.run_coroutine_threadsafe(self.play_audio(ctx, ctx.voice_client), ctx.bot.loop)

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

        self.queue.clean()
        await ctx.voice_client.disconnect()
    # ========================================

    # ========================================
    # now playing command
    # Usage: np
    # Displays the current playing song
    # ========================================
    @commands.command(
        name = "np",
        help = "np",
        description = "Display the current song"
    )
    async def np(self, ctx: Context):
        embed_msg = self.spawn_embed(ctx, title = "Now Playing")

        if self.queue.empty():
            embed_msg.description = "There are no songs currently playing"
        else:
            curr_song = self.queue.first()
            embed_msg.description = (
                f"**{curr_song.title}**\n"
                f"Duration: `{curr_song.get_time()}`"
            )

        await ctx.send(embed = embed_msg)

    # ========================================
    # queue command
    # Usage: queue
    # Displays the current queue
    @commands.command(
        name = "queue",
        help = "queue",
        description = "Displays the current queue"
    )
    async def queue(self, ctx: Context):
        embed_msg = self.spawn_embed(ctx, title = "Music queue")

        if self.queue.empty():
            embed_msg.description = "There are currently no songs in queue"
        else:
            q_list = self.queue.dump()
            embed_msg.description = f"There are {len(q_list)} songs in queue"

            for i in range(0, len(q_list)):
                song = q_list[i]

                embed_msg.add_field(
                    name = f"{i + 1}. {song.title}",
                    value = f"Duration: {song.get_time()}",
                    inline = False
                )

        await ctx.send(embed = embed_msg)
    # ========================================
    
    # ========================================
    # skip command
    # Usage: skip
    # Skips the current song
    @commands.command(
        name = "skip",
        help = "skip",
        description = "Skips the curret song"
    )
    async def skip(self, ctx: Context):
        embed_msg = self.spawn_embed(ctx, title = "Skip")

        if self.queue.empty():
            embed_msg.description = "There are currently no songs playing"
        else:
            curr_music = self.queue.first()
            embed_msg.description = f"Skipping: `{curr_music.title}`"
            await ctx.send(embed = embed_msg)

            ctx.voice_client.pause()
            self.queue.dequeue()
            await self.play_audio(ctx, ctx.voice_client)
    # ========================================

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

# A queue system for the music bot
class musicQueue():
    def __init__(self):
        self.queue_list = []

    def queue(self, data):
        self.queue_list.append(youtubeVidMeta(data))

    def dequeue(self):
        self.queue_list.pop(0)

    def dump(self):
        return [vid_meta for vid_meta in self.queue_list]
    
    def empty(self):
        return len(self.queue_list) == 0

    def clean(self):
        self.queue_list.clear()

    def first(self):
        return self.queue_list[0]

    def last(self):
        return self.queue_list[-1]

# A class representing a youtube video
# Contains metadata such as title, url, etc...
class youtubeVidMeta():
    def __init__(self, data):
        self.url = data['formats'][0]['url']
        self.duration = data['duration']
        self.title = data['title']

    def get_time(self):
        m, s = divmod(self.duration, 60)
        return "{:02d}:{:02d}".format(m, s)

    def printData(self):
        print(f"Title: {self.title}")
        print(f"Duration: {self.duration}")
        print(f"Url: {self.url}")