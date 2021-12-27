# File for commands that only fit for the worthy

# Requires permission to use the command
# Permission function is cog_check, MUST return a bool type
# (Another black magic from discord.py lol)

# Commands and error handling goes to the same file

import json
from discord import Member
from discord.ext import commands
from discord.ext.commands import Context
from discord.ext.commands.bot import Bot

def setup(bot: Bot):
    bot.add_cog(commandsRestricted())

class commandsRestricted(commands.Cog, name = "Moderation"):
    # Initial const variables
    json_file_path = "../settings/settings.json"

    # Applies permission check to all commands
    # Check wether the author of the message is server owner
    # Feel free to change the permission
    async def cog_check(self, ctx: Context):
        # check if author is the owner of the server
        is_owner = ctx.author == ctx.guild.owner

        # check if author is an admin in said channel
        is_admin = ctx.author.permissions_in(ctx.channel).administrator

        # check if author is whitelisted
        f = open(self.json_file_path, "r")
        data = json.load(f)
        role = data['whitelistRole']
        f.close()
        memberRoles = [role.name for role in ctx.guild.get_member(ctx.author.id).roles]
        whitelisted = role in memberRoles

        # permission conditions
        return is_owner or is_admin or whitelisted

    # ========================================
    # Set prefix 
    # usage: setPrefix [new_prefix]
    # sets prefix and return a message
    @commands.command(
        name = "setPrefix",
        help = "setPrefix [new_prefix]",
        description = "Sets prefix and return a message"
    )
    async def setPrefix(self, ctx: Context, *, new_prefix: str):
        # Remove head and tail whitespace
        new_prefix.strip()

        if "<@!" in new_prefix:
            return await ctx.send("Cannot set prefix as user")

        self.modify_json_prefix(new_prefix)
        
        ctx.bot.command_prefix = new_prefix
        await ctx.send(f"Prefix updated to {new_prefix}")

    # error handling
    @setPrefix.error
    async def setPrefix_error(self, ctx: Context, error):
        # Permission error
        if isinstance(error, commands.MissingPermissions):
            return await ctx.send("You do not have the permisssion to access this command")

        # General argument error
        output_str = ""
        if isinstance(error, commands.MissingRequiredArgument):
            output_str = "Error: too little arguments\n"
        else:
            output_str = "Error: unidentified error\n"
        
        output_str += "\nUsage: setPrefix [new_prefix]"
        await ctx.send(output_str)

    # Helper function
    def modify_json_prefix(self, new_prefix: str):
        #Read in json file
        f = open(self.json_file_path, "r+")
        data = json.load(f)

        #Set new prefix
        data['Prefix']['customPrefix'] = new_prefix
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()

        #close json file
        f.close()
    # ========================================

    # ========================================
    # Kick a member
    # Usage: kick [mention_target_member]
    # Kicks a member and returns a confirmation msg
    @commands.command(
        name = "kick",
        help = "kick [mention_target_member] [reason]",
        description = "Kicks a member and returns a confirmation msg"
    )
    async def kick(self, ctx: Context, member: Member, *, args: str=None):
        mem_name = member.display_name
        await member.kick(reason = args) if args != None else await member.kick()
        await ctx.send(f"Users: `{mem_name}` has been kicked")
    # ========================================

    # ========================================
    # Ban a member
    # Usage: ban [mention_target_member] [reason]
    # Bans member(s) and returns a confirmation msg
    @commands.command(
        name = "ban",
        help = "ban [mention_target_member] [reason]",
        description = "Ban a member and returns a confirmation msg"
    )
    async def ban(self, ctx: Context, member: Member, *, args: str=None):
        mem_name = member.display_name
        await member.ban(reason = args) if args != None else await member.ban()
        await ctx.send(f"Users: `{' '.join(mem_name)}` has been banned")
    # ========================================

    # ========================================
    # General Helper functinos
    # ========================================
    # 