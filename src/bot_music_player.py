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

# ========================================
# LEGACY
# from youtubesearchpython.__future__ import VideosSearch
# ========================================

def setup(bot: Bot):
    bot.add_cog(commandsMusick())

# ========================================
# Checks
# ========================================

def check_voice_channel():
    def predicate(ctx: Context):
        # Error checking
        if ctx.author.voice == None:
            asyncio.run_coroutine_threadsafe(
                ctx.send("❌ **Not in voice channel**"), 
                ctx.bot.loop
            )
            return False

        if ctx.voice_client and ctx.author.voice.channel != ctx.voice_client.channel:
            asyncio.run_coroutine_threadsafe(
                ctx.send("❌ **Not in same voice channel**"),
                ctx.bot.loop
            )
            return False
        
        return True
    return commands.check(predicate)

def check_bot_in_vc():
    def predicate(ctx: Context):
        if ctx.voice_client == None:
            asyncio.run_coroutine_threadsafe(
                ctx.send("❌ **Bot not in voice channel**"),
                ctx.bot.loop
            )
            return False
        
        return True
    return commands.check(predicate)

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
        description = "Plays a youtube video on discord"
    )
    @check_voice_channel()
    async def play(self, ctx: Context, *, link: str):

        # ========================================
        # Im sorry bruh i've found a way to do the searching
        # without ytsearchpython but i suppose we could keep
        # the `yt` command
        # 
        # Code: `vid_info = vid_info['entries'][0] if 'entries' in vid_info else vid_info`
        # In: queue_video_info()
        #
        # ========================================
        # LEGACY
        # ========================================
        # Finds the link of the top search result of the str after '.play', in YouTube, and
        # Assigns it to the 'link' var
        # if link[:5] != 'https':
        #     videosSearch = VideosSearch(link, limit = 2)
        #     videosResult = await videosSearch.next()
        #     link = videosResult['result'][0]['link']
        # ========================================

        # Remove unwanted head and tail characters
        link = link.strip(" <>")
        
        try:
            await ctx.send(f"🎹 Searching for: `{link}`")

            # youtube dl options
            ydl_opts = {
                'format': 'bestaudio/best',
                'extractaudio': True,
                'audioformat': 'ogg',
                'noplaylist': True,
                'simulate': True,
                'default_search': 'ytsearch1',
                'preferffmpeg': True,
                'age_limit': '0'
            }
            await self.process_play_audio(ctx, link, ydl_opts)

        except Exception as e:
            # Only disconnects when the error is not key error
            # and there is a voice client
            if ctx.voice_client != None and type(e).__name__ != "KeyError":
                self.queue.clean()
                await ctx.voice_client.disconnect()

            # Prints traceback
            traceback.print_exc()

            # Send error embed
            error_embed = self.spawn_error_embed(ctx, e.args[0])
            return await ctx.send(embed = error_embed)

    # Wrapper for playing the youtube link
    async def process_play_audio(self, ctx: Context, link: str, ydl_opts):
        # Add video to queue
        self.queue_vdo_info(link, ydl_opts)

        # Connect and play audio
        vc = await ctx.author.voice.channel.connect() if not ctx.voice_client else ctx.voice_client

        # Plays when queue is not empty and bot is not playing any audio
        # Shows an embed queueing the video otherwise
        if not self.queue.empty() and not vc.is_playing():
            await self.play_audio(ctx, vc)
        else:
            await self.send_queued_message(ctx)

    # Add video to queue
    # Returns video info in json string, prints error message if failed
    def queue_vdo_info(self, link: str, ydl_opts):
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            vid_info = ydl.extract_info(url = link, download = False)

        # SPAWN OF THE DEVIL:
        #
        # That is FAX - Henry 6/1/2022 19:48 HKT
        print(json.dumps(vid_info, indent = 4))

        vid_info = vid_info['entries'][0] if 'entries' in vid_info else vid_info
        self.queue.queue(vid_info)

    # Plays audio from queue
    async def play_audio(self, ctx: Context, vc):
        # Shows the current playing video
        await self.np(ctx)

        vid_meta = self.queue.first()

        # Audio source, using FFmpegOpusAudio
        # Reconnects immediately on disconnect (before_options)
        song_src = await FFmpegOpusAudio.from_probe(
            source = vid_meta.url,
            before_options = '-re -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            options = '-vn -sample_rate 48000'
        )

        # Plays the audio in discord voice channel
        # Note: vc means voice client
        vc.play(
            song_src,
            after = lambda e: self.music_after(ctx) # e as in error
        )

    # Send a message of the queued song's info
    async def send_queued_message(self, ctx: Context):
        queued_song = self.queue.last()
        embed_msg = self.spawn_embed(ctx, author = "Added to Queue☑", title = queued_song.title)
        embed_msg.url = queued_song.get_vid_url()
        self.add_embed_vid_meta(embed_msg, queued_song)
        await ctx.send(embed = embed_msg)
    
    # Funtion to run after music is finished
    def music_after(self, ctx: Context):
        # Do not execute this function if vc is None
        if not ctx.voice_client:
            return

        # Dequeue the current song
        if not self.queue.empty():
            self.queue.dequeue()

        # Disconnect and send message if the queue has ended
        # plays the next song otherwise
        #
        # Note: using asyncio cuz this function is not async but the code it runs
        # has to be awaited
        if self.queue.empty():
            asyncio.run_coroutine_threadsafe(ctx.send("🍕 **Finished playing**"), ctx.bot.loop)
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
    @check_bot_in_vc()
    @check_voice_channel()
    async def disconnect(self, ctx: Context):
        # Remove all item in queue
        if not self.queue.empty():
            self.queue.clean()

        # Stops playing and disconnect
        ctx.voice_client.pause()
        await ctx.voice_client.disconnect()
        await ctx.send("✂️ **Disconnected**")
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
    @check_voice_channel()
    async def np(self, ctx: Context):
        author = "Now Playing ▶️"

        # Sends error message if the queue is empty
        if self.queue.empty():
            embed_msg = self.spawn_embed(
                ctx,
                author = author,
                title = "There are no songs currently playing"
            )
            return await ctx.send(embed = embed_msg)

        # Spawn embed msg
        curr_song = self.queue.first()
        embed_msg = self.spawn_embed(ctx, author = author, title = curr_song.title)
        embed_msg.url = curr_song.get_vid_url()
        self.add_embed_vid_meta(embed_msg, curr_song)

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
    @check_voice_channel()
    async def queue(self, ctx: Context):
        author = "Music queue 🎵"

        # Sends error message if the queue is empty
        if self.queue.empty():
            embed_msg = self.spawn_embed(
                ctx, 
                author = author,
                title = "There are currently no songs in queue"
            )
            return await ctx.send(embed = embed_msg)
        
        # Spawn embed
        q_list = self.queue.dump()
        embed_msg = self.spawn_embed(
            ctx, 
            author = author,
            title = f"There are {len(q_list)} songs in queue"
        )

        # Adds field for each song in queue
        for i in range(0, len(q_list)):
            song = q_list[i]

            embed_msg.add_field(
                name = f"{i + 1}. {song.title}",
                value = f"{song.get_vid_url()}\nDuration: `{song.get_time()}`",
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
    @check_voice_channel()
    async def skip(self, ctx: Context):
        # Sends error message if queue is empty
        if self.queue.empty():
            title = "There are currently no songs playing"
        else:
            # Constructs embed message
            curr_music = self.queue.first()
            title = f"{curr_music.title}"

            # skips the current music and play the next one
            ctx.voice_client.pause()
            self.music_after(ctx)

        embed_msg = self.spawn_embed(ctx, title = title, author = "Skip ⏭")
        await ctx.send(embed = embed_msg)
    # ========================================

    # ========================================
    # General helper function
    # ========================================

    # ========================================
    # Spawn an embed template
    def spawn_embed(self, ctx: Context, title: str, author: str=None):
        embed_msg = Embed(
            colour = 0xc27c0e,
            title = title
        )

        embed_msg.set_author(
            name = ctx.author.display_name if author == None else author,
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

    # ========================================
    # Adds video meta to embed
    def add_embed_vid_meta(self, embed_msg: Embed, curr_song):
        embed_msg.add_field(
            name = "Channel name:",
            value = f"> {curr_song.channel}"
        )

        embed_msg.add_field(
            name = "Duration:",
            value = f"> {curr_song.get_time()}"
        )

        embed_msg.set_thumbnail(url = curr_song.thumbnail)
    # ========================================

# A queue system for the music bot
class musicQueue():
    def __init__(self):
        self.queue_list = []

    # Queues in a list
    def queue(self, data):
        self.queue_list.append(youtubeVidMeta(data))

    # Dequeues the first item in list
    def dequeue(self):
        self.queue_list.pop(0)

    # Returns a copy of the list
    def dump(self):
        return [vid_meta for vid_meta in self.queue_list]
    
    # Check if list is empty
    def empty(self):
        return len(self.queue_list) == 0

    # Remove all item in list
    def clean(self):
        self.queue_list.clear()

    # Returns the first item in list
    def first(self):
        return self.queue_list[0]

    # Returns the last item in list
    def last(self):
        return self.queue_list[-1]

# A class representing a youtube video
# Contains metadata such as title, url, etc...
class youtubeVidMeta():
    def __init__(self, data):
        self.url = data['formats'][0]['url']
        self.duration = data['duration']
        self.title = data['title']
        self.vid_id = data['id']
        self.channel = data['channel']
        self.thumbnail = data['thumbnail']

    # Display the duration in mm:ss format
    def get_time(self):
        m, s = divmod(self.duration, 60)
        return "{:02d}:{:02d}".format(m, s)

    # Returns the original video link
    def get_vid_url(self):
        return f"https://www.youtube.com/watch?v={self.vid_id}"

    def get_embedded_title(self):
        return f"[{self.title}]({self.get_vid_url()})"

    # Prints data, for debugging
    def printData(self):
        print(f"Title: {self.title}")
        print(f"Duration: {self.duration}")
        print(f"Url: {self.url}")