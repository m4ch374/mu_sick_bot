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

# main fnc
def main():
    curr_dir_path = os.path.abspath(os.path.dirname(__file__)) + '/'
    settings_path = f"{curr_dir_path}../settings/settings.json"

    # Set intents
    intents = discord.Intents.all()

    prefix = get_prefix(settings_path)

    bot = commands.Bot(
        command_prefix = 
            commands.when_mentioned_or(get_prefix(settings_path)), 

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

    ignore_list = get_ignore_list(settings_path)
    load_cogs(bot, ignore_list, curr_dir_path)

    # run token
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

def get_ignore_list(file_path: str):
    f = open(file_path, 'r')
    data = json.load(f)

    return data['fileIgnoreList']

def load_cogs(bot: Bot, ignore_list, curr_dir: str):
    # Load cogs
    for files in os.listdir(curr_dir):
        if not files in ignore_list:
            print(f"Loaded {files}")
            bot.load_extension(f"{files[:-3]}")

# Only execute main if user executes this file
if __name__ == '__main__':
    main()