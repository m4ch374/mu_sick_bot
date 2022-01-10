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

# Import from own files
from music_queue_system import youtubeVidMeta
from music_queue_system import musicQueue

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
    # Cannot access self with decorators
    # So we have to use a constant big oof
    QUEUE_EMPTY_MSG = "❌ **Queue is empty**"

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

        # "Thou shall not be sorry for finding a more efficient way to her anus" ~ Master Oogway, prolly @_@
        # nah nah all g bro, that one liner is 100% much better, also, wtf does it mean? XDDD

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
                'age_limit': '0',
                'is_live': False
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
        vid_info = self.get_vdo_info(link, ydl_opts)

        if vid_info['is_live'] == True:
            return await ctx.send("❌ **Live is not accepted**")

        self.queue.queue(vid_info)

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
    def get_vdo_info(self, link: str, ydl_opts):
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            vid_info = ydl.extract_info(url = link, download = False)

        # SPAWN OF THE DEVIL:
        #
        # That is FAX - Henry 6/1/2022 19:48 HKT
        print(json.dumps(vid_info, indent = 4))

        vid_info = vid_info['entries'][0] if 'entries' in vid_info else vid_info
        return vid_info

    # Plays audio from queue
    async def play_audio(self, ctx: Context, vc):
        # Shows the current playing video
        await self.send_current_vid_info(ctx)

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
        embed_msg = self.spawn_embed(ctx, author = "Added to Queue ✅", title = queued_song.title)
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
        await self.send_current_vid_info(ctx)

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

        # Sends error message if the queue is empty
        if self.queue.empty():
            return await ctx.send(self.QUEUE_EMPTY_MSG)
        
        # Spawn embed
        q_list = self.queue.dump()
        embed_msg = self.spawn_embed(
            ctx, 
            author = "Music queue 🎵",
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
    # remove command
    # Usage: remove [index]
    # Removes a song in queue at specified index
    @commands.command(
        name = "remove",
        help = "remove [index]",
        description = ("Removes a song in queue at specified index.\n" +
            "> Note: Index starts at `1`")
    )
    @check_voice_channel()
    async def remove(self, ctx: Context, index: int):
        # Sends error message if queue is empty
        if self.queue.empty():
            return await ctx.send(self.QUEUE_EMPTY_MSG)
        
        # Sends error message if index is out of range
        if index <= 0 or index > self.queue.get_len():
            return await ctx.send("❌ **Index out of range**")
        
        # Get the song's data
        target_song = self.queue.get_at_index(index - 1)

        if index == 1:
            self.skip_curr_vid(ctx)
        else:
            self.queue.remove_at_index(index - 1)

        embed_msg = self.spawn_embed(ctx, title = target_song.title, author = "Removed ✅")
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
            return await ctx.send(self.QUEUE_EMPTY_MSG)

        # Get the current music's data
        curr_music = self.queue.first()

        # Skips current video and play the next one
        self.skip_curr_vid(ctx)

        embed_msg = self.spawn_embed(ctx, title = curr_music.title, author = "Skip ⏭")
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
    # Send the current vid's info embed
    async def send_current_vid_info(self, ctx: Context):
        author = "Now Playing ▶️"

        # Sends error message if the queue is empty
        if self.queue.empty():
            return await ctx.send(self.QUEUE_EMPTY_MSG)

        # Spawn embed msg
        curr_song = self.queue.first()
        embed_msg = self.spawn_embed(ctx, author = author, title = curr_song.title)
        embed_msg.url = curr_song.get_vid_url()
        self.add_embed_vid_meta(embed_msg, curr_song)

        await ctx.send(embed = embed_msg)
    # ========================================

    # ========================================
    # Skips current video in playlist and play the next one
    def skip_curr_vid(self, ctx: Context):
        ctx.voice_client.pause()
        self.music_after(ctx)
    # ========================================

    # ========================================
    # Adds video meta to embed
    def add_embed_vid_meta(self, embed_msg: Embed, curr_song: youtubeVidMeta):
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