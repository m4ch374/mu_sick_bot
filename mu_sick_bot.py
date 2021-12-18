# Main file for the bot, theres no main in python so imma 
# make my own main entry point haha lmao xddd

# Imports from libraries
from logging import error
from discord.ext import commands
from discord.message import Message

# Imports from own file
import bot_commands
import error_handling

# main fnc
def main():
    # prefix variable
    prefix = '$'

    bot = commands.Bot(command_prefix=prefix)

    # event logging and stuff idk bro
    @bot.event
    async def on_ready():
        print('We have logged in as {0.user}'.format(bot))

    @bot.event
    async def on_message(message: Message):
        if message.author == bot.user:
            return

        print(f"{message.author}: {message.content}")
        await bot.process_commands(message)

    # import cogs
    bot.add_cog(bot_commands.commandsCommon(bot))
    bot.add_cog(error_handling.commandsErrorCommon(bot))

    # run token
    bot.run('OTIxMzI4NTEyNzE4MjA5MDU1.YbxUCg._ZmyMkTtgFh_znDg3xxuZw6KAZY')

# Only execute main if user executes this file
if __name__ == '__main__':
    main()