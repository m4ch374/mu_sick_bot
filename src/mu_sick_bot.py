# Main file for the bot, theres no main in python so imma 
# make my own main entry point haha lmao xddd

# Imports from libraries
from discord.ext import commands
from discord.ext.commands.errors import CommandError
from discord.message import Message

from bot_logger import logger
from bot_commands import commandsCommon
from error_handling import commandsErrorCommon

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

    # Import cogs
    bot.add_cog(logger(bot))
    bot.add_cog(commandsCommon(bot))
    bot.add_cog(commandsErrorCommon(bot))

    # run token
    bot.run('OTIxMzI4NTEyNzE4MjA5MDU1.YbxUCg._ZmyMkTtgFh_znDg3xxuZw6KAZY')

# Only execute main if user executes this file
if __name__ == '__main__':
    main()