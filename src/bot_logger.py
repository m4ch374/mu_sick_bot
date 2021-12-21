# Files for logging user and bot activities
from discord.ext import commands
from discord.ext.commands.bot import Bot
from discord.ext.commands.context import Context

def setup(bot: Bot):
    bot.add_cog(logger(bot))

class logger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # on_ready Listener
    # output the following string after the bot
    # is online and ready
    @commands.Cog.listener()
    async def on_ready(self):
        print('We have logged in as {0.user}'.format(self.bot))

    @commands.Cog.listener()
    async def on_connect(self):
        print('Bot connected')
    
    @commands.Cog.listener()
    async def on_command(self, ctx: Context):
        print(f"{ctx.author}: {ctx.message.content}")
    