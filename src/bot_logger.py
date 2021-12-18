# Files for logging user and bot activities
from discord.ext import commands
from discord.ext.commands.bot import Bot

def setup(bot: Bot):
    bot.add_cog(logger(bot))

class logger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('We have logged in as {0.user}'.format(self.bot))
    