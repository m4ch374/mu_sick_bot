# File for commands that only fit for the worthy

# Requires permission to use the command
# Permission function is cog_check, MUST return a bool type
# (Another black magic from discord.py lol)

# Commands and error handling goes to the same file

import json
from discord import Role
from discord import Member
from discord.ext import commands
from discord.ext.commands import Context
from discord.ext.commands.bot import Bot

# Import form own file
import mu_sick_bot
from mu_sick_bot import SETTINGS_PATH

def setup(bot: Bot):
    bot.add_cog(commandsRestricted())

class commandsRestricted(commands.Cog, name = "Moderation"):
    # Initial const variables
    json_file_path = SETTINGS_PATH

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
        new_prefix = new_prefix.strip()

        # Mentions starts with "<@!"
        if "<@!" in new_prefix:
            return await ctx.send("Cannot set prefix as user")

        # Change the new prefix in json
        self.modify_json_prefix(new_prefix)
        
        # Change the new prefix for the bot
        ctx.bot.command_prefix = new_prefix
        mu_sick_bot.set_activity(ctx.bot)
        await ctx.send(f"Prefix updated to `{new_prefix}`")

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
    # Usage: kick [member] [reason]
    # Kicks a member and returns a confirmation msg
    @commands.command(
        name = "kick",
        help = "kick [member] [reason]",
        description = "Kicks a member and returns a confirmation msg"
    )
    async def kick(self, ctx: Context, member: Member, *, args: str=None):
        mem_name = member.display_name

        # kick with reason if reason is provided, only kicks otherwise
        await member.kick(reason = args) if args != None else await member.kick()
        await ctx.send(f"Users: `{mem_name}` has been kicked")
    # ========================================

    # ========================================
    # Ban a member
    # Usage: ban [member] [reason]
    # Bans member(s) and returns a confirmation msg
    @commands.command(
        name = "ban",
        help = "ban [member] [reason]",
        description = "Ban a member and returns a confirmation msg"
    )
    async def ban(self, ctx: Context, member: Member, *, args: str=None):
        mem_name = member.display_name

        # ban with reason if reason is provided, only bans otherwise
        await member.ban(reason = args) if args != None else await member.ban()
        await ctx.send(f"Users: `{mem_name}` has been banned")
    # ========================================

    # ========================================
    # whitelist command
    # Usage: whitelist [role]
    # Set the role as whitelisted role.
    # i.e. said roles has access to restricted commands
    @commands.command(
        name = "whitelist",
        help = "whitelist [role]",
        description = ("Set the role as whitelisted role\n" +
            "i.e. said role has access to restricted commands")
    )
    async def whitelist(self, ctx: Context, role: Role):
        self.modify_json_whitelist(role.name)

        await ctx.send(f"Whitelisted role: `{role.name}`")

    # Helper function
    def modify_json_whitelist(self, role_name: str):
        #Read in json file
        f = open(self.json_file_path, "r+")
        data = json.load(f)

        #Set new prefix
        data['whitelistRole'] = role_name
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()

        #close json file
        f.close()
    # ========================================

    # ========================================
    # General Helper functinos
    # ========================================
    # 