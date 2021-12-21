# Main file for the bot, theres no main in python so imma 
# make my own main entry point haha lmao xddd

# Imports from libraries
import os
import json
from discord.ext import commands
from discord.message import Message

# main fnc
def main():
    #Read in json file
    f = open('../settings/settings.json', 'r')
    data = json.load(f)

    # prefix variable
    prefix = data['Prefix']['defaultPrefix']

    #close json file
    f.close()

    bot = commands.Bot(command_prefix = commands.when_mentioned_or(prefix), strip_after_prefix = True)

    # Execute commands after recievesa message
    @bot.event
    async def on_message(message: Message):

        # Ignore if the message is sent by the bot itself
        if message.author == bot.user:
            return
        
        # Execute commands
        await bot.process_commands(message)

    # Load cogs
    for files in os.listdir(os.path.dirname(__file__)):
        if files != "mu_sick_bot.py" and files != "__pycache__":
            print(f"Loaded {files}")
            bot.load_extension(f"{files[:-3]}")

    # run token
    bot.run('OTIxMzI4NTEyNzE4MjA5MDU1.YbxUCg._ZmyMkTtgFh_znDg3xxuZw6KAZY')

# Only execute main if user executes this file
if __name__ == '__main__':
    main()