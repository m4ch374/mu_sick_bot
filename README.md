<h1 align="center">
  &#127925 mu_sick_bot &#127925
</h1>

<p align = "center">
  <img src="asset/mu_sick_bot_icon.png" alt="bot_icon">
</p>

# :book: Description
As music bots such as Groovy and Rythm ended their service, we thought:  
> If we don't have one, we gon' make one - Sun Tsu (probably)

And thats how the `mu_sick_bot` was born.  

`mu_sick_bot` is a discord music bot written in Python, using `discord.py`.  
It is a passion project coded by [m4ch374](https://github.com/m4ch374) and [n0t-4m17h](https://github.com/n0t-4m17h).

This bot is compatible for both `Linux` and `Windows`.

# :heavy_check_mark: Getting Started

### **1. Installing `Python`:**

To run the bot, we must first install python.

**Note: Pyhon 3.8 or higher is required.**

* For Linux users:
```
$ sudo apt-get install python
```  
* For Windows users:

> Download Python via [this link](https://www.python.org/downloads/)

### **2. Installing `FFmpeg`:**

In order for the bot to play music properly, we also need to install FFmpeg.

**Note: FFmpeg has to be in PATH.**

* For Linux users:
```
$ sudo apt-get install ffmpeg
```

* For Windows users:

> Download FFmpeg via [this link](https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z)

### **3. Installing `discord.py` and `requests`:**

To install discord.py and requests, run the following command:
```cs
# Linux users
$ python3 -m pip install -U "discord.py[voice]"
$ python3 -m pip install requests

# Windows users
$ py -3 -m pip install -U discord.py[voice]
$ py -3 -m pip install requests
```

### **4. Installing `youtube-search-python`, `youtube-dl`:**

To install these libraries, run the following commands:

```cs
# Linux users
$ python3 -m pip install youtube-search-python
$ python3 -m pip install youtube-dl

# Windows users
$ py -3 -m pip install youtube-search-python
$ py -3 -m pip install youtube-dl
```

# :desktop_computer: Running the bot

To run the bot, navigate to the directory containing the srouce file, and run:

```cs
# Linux users
$ python3 src/mu_sick_bot.py

# Windows users
$ py src/mu_sick_bot.py
```

# :robot: Commands [Default prefix: `$`]

## Help command
* help Optional[command / category]

  > Displays all commands for the bot / category if it is provided.  
  > Displays the usage of a command if it is provided.

## Available commands

The `mu_sick_bot` provides commands in these 4 main categories:

* Music
* API
* Common commands
* Moderation

## 1. Music
* play [link / title]

  > Plays the music from the given link or title

* disconnect

  > Disconnects from voice channel

* np

  > Shows the info of the music that's currently playing

* queue

  > Displays the music queue

* remove [index]

  > Removes a song from queue at specified index (Note: index starts at 1)

* skip

  > Skips the current song and plays the next song

## 2. API
* covid Optional[country_slug]

  > Discplays global covid data, displays data for specific country if `country slug` is provided  
  > **Note: The data retrieved is kinda inaccurate.**

* anime [title]

  > Displays info on the specified anime

* manga [title]

  > Displays info on the specified manga

* waifu

  > Displays an image of a random waifu

* fbi

  > Naughty stuff :eyes:  
  > **Note: Only sends out image in NSFW channels**

## 3. Common commands

* hello Optional[n]

  > Prints "Hello World" n times

* echo [args]

  > Repeats what the member typed

* yt [arg]

  > Gives the top 5 youtube links that mest matches the given input

* sesh [user]
  > Displays the discord activities that a certain member has

## 4. Moderation
* setPrefix [new_prefix]

  > Sets the prefix for the bot  
  > **Note: mentions are not allowed**

* kick [member] Optional[reason]

  > Kicks a member

* ban [member] Optional[reason]

  > Bans a member

* whitelist [role]

  > Whitelist a role such that the role has access to Moderation commands

# :triangular_ruler: Supported Sources and Restrictions
* :white_check_mark: Supported sources  
Unfortunately, at this stage we only support sources from `youtube`

* :x: Restrictions
  * The video provided **cannot be live**
  * Playlist is **not** supported, once provided, it will only add the **first song** in the playlist to the queue

----

We plan to further expand the capabilities of this bot, when we have time.