# File for logging user and bot activities
# Also contains general error checking responses

# Import from discord
from discord.ext import commands
from discord.ext.commands import CommandError
from discord.ext.commands.bot import Bot
from discord.ext.commands.context import Context

# Import from own files
import mu_sick_bot

def setup(bot: Bot):
    bot.add_cog(logger(bot))

class logger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ========================================
    # on_ready Listener
    # prints username on ready
    @commands.Cog.listener()
    async def on_ready(self):
        print('We have logged in as {0.user}'.format(self.bot))
        mu_sick_bot.set_activity(self.bot)
    # ========================================

    # ========================================
    # on_connect Listener
    # prints "Bot connected" at connection
    @commands.Cog.listener()
    async def on_connect(self):
        print('Bot connected')
    # ========================================
    
    # ========================================
    # on_command Listener
    # prints the user and the command
    # function fires when a command is detected
    @commands.Cog.listener()
    async def on_command(self, ctx: Context):
        print(f"{ctx.author}: {ctx.message.content}")
    # ========================================

    # ========================================
    # General error handlers
    @commands.Cog.listener()
    async def on_command_error(self, ctx: Context, error: CommandError):
        # Checks if ctx.cmd is "None"
        if ctx.command:
            if ctx.command.has_error_handler(): return

        # Ignore command not found error
        if isinstance(error, commands.CommandNotFound):
            return
        
        if isinstance(error, commands.MissingPermissions):
            message = "You are missing the required permissions to run this command!"
        elif isinstance(error, commands.CommandOnCooldown):
            message = f"Hey `{ctx.author.name}`, please wait `{round(error.retry_after)}` seconds before executing this command!"
        elif isinstance(error, commands.errors.MemberNotFound):
            message = f"`{error.argument}` appears to be absent from this server!"
            # UserInputError is a very generalised error, hence goes at the bottom
        elif isinstance(error, commands.UserInputError):
            message = (f"Something about your input was wrong, " +
                f"type `{ctx.prefix}help {ctx.command}` for more info")
        else:
            print(error)

        await ctx.send(message)
    # ========================================
