# Main file for the bot, theres no main in python so imma 
# make my own main entry point haha lmao xddd

# System imports
import os
import json

# Imports from discord
import discord
from discord.ext import commands
from discord.ext.commands.bot import Bot
from discord.message import Message

# Imports from local files
import help_command

# ----------------------------------------
# GLOBAL DEFINITIONS
# btw this is really ugly, reckon there's a better way?
global CURR_DIR_PATH
global SETTINGS_PATH
CURR_DIR_PATH = os.path.abspath(os.path.dirname(__file__)) + '/'
SETTINGS_PATH = f"{CURR_DIR_PATH}../settings/settings.json"
# ----------------------------------------

# main fnc
def main():

    # Set intents
    intents = discord.Intents.all()

    bot = commands.Bot(
        command_prefix = 
            commands.when_mentioned_or(get_prefix(SETTINGS_PATH)), 

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
    bot.run('OTIxMzI4NTEyNzE4MjA5MDU1.YbxUCg._ZmyMkTtgFh_znDg3xxuZw6KAZY')

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

# Load cogs
def load_cogs(bot: Bot, ignore_list, curr_dir: str):
    # Load cogs
    for files in os.listdir(curr_dir):
        if not files in ignore_list:
            print(f"Loaded {files}")
            bot.load_extension(f"{files[:-3]}")

# Only execute main if user executes this file
if __name__ == '__main__':
    main()