# Main file for the bot, theres no main in python so imma 
# make my own main entry point haha lmao xddd

# Imports from libraries
from discord.ext import commands
from discord.message import Message

# Imports from own file
from bot_commands import commandsCommon

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
    bot.add_cog(commandsCommon(bot))

    # run token
    bot.run('Place token here')

# Only execute main if user executes this file
if __name__ == '__main__':
    main()