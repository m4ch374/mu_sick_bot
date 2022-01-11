# Main file for the bot, theres no main in python so imma 
# make my own main entry point haha lmao xddd

# System imports
import os
import json
import asyncio

# Imports from discord
import discord
from discord.ext import commands
from discord.ext.commands.bot import Bot
from discord.message import Message

# Imports from local files
import help_command

# ----------------------------------------
# GLOBAL DEFINITIONS
global CURR_DIR_PATH
global SETTINGS_PATH
CURR_DIR_PATH = os.path.abspath(os.path.dirname(__file__)) + '/'
SETTINGS_PATH = f"{CURR_DIR_PATH}../settings/settings.json"
# ----------------------------------------

# main fnc
def main():
    print_logo()

    # Set intents
    intents = discord.Intents.all()

    bot = commands.Bot(
        command_prefix = get_prefix(SETTINGS_PATH),

        # Enables whitespace
        strip_after_prefix = True, 
        intents = intents,
        help_command = help_command.customHelpCmd()
    )

    # Execute commands after recievesa message
    @bot.event
    async def on_message(message: Message):

        # Ignore if the message is sent by the bot itself
        if message.author == bot.user:
            return
        
        # Execute commands
        await bot.process_commands(message)

    # load cogs with ignore list
    ignore_list = get_ignore_list(SETTINGS_PATH)
    load_cogs(bot, ignore_list, CURR_DIR_PATH)

    # run token, token should be kept as an secret
    bot.run(get_token(SETTINGS_PATH))

# Prints mu_sick_bot logo
def print_logo():
    logo = ("███╗   ███╗██╗   ██╗        ███████╗██╗ ██████╗██╗  ██╗        ██████╗  ██████╗ ████████╗\n" +
            "████╗ ████║██║   ██║        ██╔════╝██║██╔════╝██║ ██╔╝        ██╔══██╗██╔═══██╗╚══██╔══╝\n" +
            "██╔████╔██║██║   ██║        ███████╗██║██║     █████╔╝         ██████╔╝██║   ██║   ██║   \n" +
            "██║╚██╔╝██║██║   ██║        ╚════██║██║██║     ██╔═██╗         ██╔══██╗██║   ██║   ██║   \n" +
            "██║ ╚═╝ ██║╚██████╔╝███████╗███████║██║╚██████╗██║  ██╗███████╗██████╔╝╚██████╔╝   ██║   \n" +
            "╚═╝     ╚═╝ ╚═════╝ ╚══════╝╚══════╝╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═════╝  ╚═════╝    ╚═╝   \n")

    print(f"\n{logo}")

# Helper function for getting bot prefix
def get_prefix(file_path: str):
    #Read in json file
    f = open(file_path, 'r')
    data = json.load(f)

    # prefix variable
    prefix_data = data['Prefix']
    prefix = (prefix_data['customPrefix'] if prefix_data['customPrefix'] != "" 
        else prefix_data['defaultPrefix'])

    #close json file
    f.close()
    return prefix

# Retunrs the file ignore list
def get_ignore_list(file_path: str):
    # Read json file
    f = open(file_path, 'r')
    data = json.load(f)

    # gets the list
    returned_list = data['fileIgnoreList']

    # close file and return list
    f.close()
    return returned_list

# Get the bot's token
def get_token(file_path: str):
    f = open(file_path, 'r')
    data = json.load(f)

    token = data['bot_token']

    f.close()
    return token

# Load cogs
def load_cogs(bot: Bot, ignore_list, curr_dir: str):
    # Load cogs
    for files in os.listdir(curr_dir):
        if not files in ignore_list:
            print(f"* Loaded {files}")
            bot.load_extension(f"{files[:-3]}")
    # Prints new line
    print("")

# Sets the activity of the bot
def set_activity(bot: Bot):
    # Set activity
    activity = discord.Game(name = f"{bot.command_prefix}help")
    asyncio.run_coroutine_threadsafe(
        bot.change_presence(activity = activity),
        bot.loop
    )

# Only execute main if user executes this file
if __name__ == '__main__':
    main()