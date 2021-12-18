# Main file for the bot, theres no main in python so imma 
# make my own main entry point haha lmao xddd

# Imports from libraries
import os
from discord.ext import commands
from discord.message import Message

# main fnc
def main():
    # prefix variable
    prefix = '$'

    bot = commands.Bot(command_prefix=prefix)

    # Execute commands after recievesa message
    @bot.event
    async def on_message(message: Message):

        # Ignore if the message is sent by the bot itself
        if message.author == bot.user:
            return

        # Print out the message if user tries to
        # use the bot (commands that does not exist also prints)
        if prefix in message.content.split()[0]:
            print(f"{message.author}: {message.content}")
        
        await bot.process_commands(message)

    # Import Cogs from files
    for files in os.listdir(os.path.dirname(__file__)):
        if files != "__pycache__" and files != "mu_sick_bot.py":
            bot.load_extension(f"{files[:-3]}")

    # run token
    bot.run('OTIxMzI4NTEyNzE4MjA5MDU1.YbxUCg._ZmyMkTtgFh_znDg3xxuZw6KAZY')

# Only execute main if user executes this file
if __name__ == '__main__':
    main()