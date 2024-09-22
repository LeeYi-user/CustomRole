import discord, json
from discord.ext import commands
from dislash import *
from core import *

class AtCommand(Cog):
    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def help(self, ctx, *, command = None):
        permission = ctx.me.permissions_in(ctx.channel)

        if (permission.embed_links == True) and (permission.read_message_history == True):
            await ctx.send(embed = await Core.help(command))

        ctx.command.reset_cooldown(ctx)

    @help.error
    async def help_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown) == True:
            if ctx.me.permissions_in(ctx.channel).manage_messages == True:
                await ctx.message.delete()
        else:
            if str(error.original) == "can't find command":
                await ctx.send(embed = discord.Embed(title = "Command is Not Found", color = discord.Color.red()))
            else:
                await ctx.send(embed = discord.Embed(title = "Unknown Error Occurred", color = discord.Color.red()))
                print(error)

            ctx.command.reset_cooldown(ctx)

    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def get(self, ctx, *, msg):
        permission = ctx.me.permissions_in(ctx.channel)

        if (permission.embed_links == True) and (permission.read_message_history == True):
            await ctx.trigger_typing()
            strings = msg.split(" ")

            with open("color_names.json") as f:
                color_names = json.loads(f.read())

            if (len(strings) > 1) and ((strings[-1].lower() in color_names) or (strings[-1][0] == "#")):
                name = " ".join(strings[:-1])
                color = strings[-1]
            else:
                name = msg
                color = "black"

            await ctx.send(embed = await Core.get(ctx, name, color))

        ctx.command.reset_cooldown(ctx)

    @get.error
    async def get_error(self, ctx, error):
        permission = ctx.me.permissions_in(ctx.channel)

        if isinstance(error, commands.CommandOnCooldown) == True:
            if permission.manage_messages == True:
                await ctx.message.delete()
        else:
            if isinstance(error, commands.MissingRequiredArgument) == True:
                pass
            elif str(error.original) == "can't use here":
                await ctx.send(embed = discord.Embed(title = "You Cannot Use It Here", color = discord.Color.red()))
            elif str(error.original) == "can't manage roles":
                await ctx.send(embed = discord.Embed(title = "I Need Manage Roles to Do This", color = discord.Color.red()))
            elif str(error.original) == "can't view audit log":
                await ctx.send(embed = discord.Embed(title = "I Need View Audit Log to Do This", color = discord.Color.red()))
            elif str(error.original) == "can't manage user":
                await ctx.send(embed = discord.Embed(title = "I Need Higher Role to Do This", color = discord.Color.red()))
            elif str(error.original) == "can't create role":
                await ctx.send(embed = discord.Embed(title = "Role Amount Must Be Less Than 250", color = discord.Color.red()))
            elif str(error.original) == "can't set name":
                await ctx.send(embed = discord.Embed(title = "Name Length Must Be Less Than 100", color = discord.Color.red()))
            elif str(error.original) == "can't find color":
                await ctx.send(embed = discord.Embed(title = "Color is Not Found", color = discord.Color.red()))
            else:
                await ctx.send(embed = discord.Embed(title = "Unknown Error Occurred", color = discord.Color.red()))
                print(error)

            ctx.command.reset_cooldown(ctx)

    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def remove(self, ctx):
        permission = ctx.me.permissions_in(ctx.channel)

        if (permission.embed_links == True) and (permission.read_message_history == True):
            await ctx.trigger_typing()
            await ctx.send(embed = await Core.remove(ctx))

        ctx.command.reset_cooldown(ctx)

    @remove.error
    async def remove_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown) == True:
            if ctx.me.permissions_in(ctx.channel).manage_messages == True:
                await ctx.message.delete()
        else:
            if str(error.original) == "can't use here":
                await ctx.send(embed = discord.Embed(title = "You Cannot Use It Here", color = discord.Color.red()))
            elif str(error.original) == "can't manage roles":
                await ctx.send(embed = discord.Embed(title = "I Need Manage Roles to Do This", color = discord.Color.red()))
            elif str(error.original) == "can't view audit log":
                await ctx.send(embed = discord.Embed(title = "I Need View Audit Log to Do This", color = discord.Color.red()))
            elif str(error.original) == "can't manage user":
                await ctx.send(embed = discord.Embed(title = "I Need Higher Role to Do This", color = discord.Color.red()))
            elif str(error.original) == "can't find role":
                await ctx.send(embed = discord.Embed(title = "Role is Not Found", color = discord.Color.red()))
            else:
                await ctx.send(embed = discord.Embed(title = "Unknown Error Occurred", color = discord.Color.red()))
                print(error)

            ctx.command.reset_cooldown(ctx)

    @commands.command()
    @commands.is_owner()
    async def server(self, ctx):
        permission = ctx.me.permissions_in(ctx.channel)

        if (permission.embed_links == True) and (permission.read_message_history == True):
            await ctx.send(embed = discord.Embed(title = f"There Are {len(self.client.guilds)} Servers Using Me", color = discord.Color.orange()))

class SlashCommand(Cog):
    @slash_commands.command(description = "Help with custom role", options = [Option("command", "e.g. get")])
    @slash_commands.cooldown(1, 60, commands.BucketType.user)
    async def help(self, inter):
        await inter.reply(embed = await Core.help(inter.get("command", default = None)))
        inter.slash_command.reset_cooldown(inter)

    @help.error
    async def help_error(self, inter, error):
        if isinstance(error, slash_commands.CommandOnCooldown) == True:
            pass
        else:
            if str(error) == "can't find command":
                await inter.reply(embed = discord.Embed(title = "Command is Not Found", color = discord.Color.red()))
            else:
                await inter.reply(embed = discord.Embed(title = "Unknown Error Occurred", color = discord.Color.red()))
                print(error)

            inter.slash_command.reset_cooldown(inter)

    @slash_commands.command(description = "Get the custom role", options = [Option("name", "e.g. King", required = True), Option("color", "e.g. orange")])
    @slash_commands.cooldown(1, 60, commands.BucketType.user)
    async def get(self, inter):
        await inter.reply()
        await inter.edit(embed = await Core.get(inter, inter.get("name"), inter.get("color", default = "black")))
        inter.slash_command.reset_cooldown(inter)

    @get.error
    async def get_error(self, inter, error):
        if isinstance(error, slash_commands.CommandOnCooldown) == True:
            pass
        else:
            if str(error) == "can't use here":
                await inter.edit(embed = discord.Embed(title = "You Cannot Use It Here", color = discord.Color.red()))
            elif str(error) == "can't manage roles":
                await inter.edit(embed = discord.Embed(title = "I Need Manage Roles to Do This", color = discord.Color.red()))
            elif str(error) == "can't view audit log":
                await inter.edit(embed = discord.Embed(title = "I Need View Audit Log to Do This", color = discord.Color.red()))
            elif str(error) == "can't manage user":
                await inter.edit(embed = discord.Embed(title = "I Need Higher Role to Do This", color = discord.Color.red()))
            elif str(error) == "can't create role":
                await inter.edit(embed = discord.Embed(title = "Role Amount Must Be Less Than 250", color = discord.Color.red()))
            elif str(error) == "can't set name":
                await inter.edit(embed = discord.Embed(title = "Name Length Must Be Less Than 100", color = discord.Color.red()))
            elif str(error) == "can't find color":
                await inter.edit(embed = discord.Embed(title = "Color is Not Found", color = discord.Color.red()))
            else:
                await inter.edit(embed = discord.Embed(title = "Unknown Error Occurred", color = discord.Color.red()))
                print(error)

            inter.slash_command.reset_cooldown(inter)

    @slash_commands.command(description = "Remove the custom role")
    @slash_commands.cooldown(1, 60, commands.BucketType.user)
    async def remove(self, inter):
        await inter.reply()
        await inter.edit(embed = await Core.remove(inter))
        inter.slash_command.reset_cooldown(inter)

    @remove.error
    async def remove_error(self, inter, error):
        if isinstance(error, slash_commands.CommandOnCooldown) == True:
            pass
        else:
            if str(error) == "can't use here":
                await inter.edit(embed = discord.Embed(title = "You Cannot Use It Here", color = discord.Color.red()))
            elif str(error) == "can't manage roles":
                await inter.edit(embed = discord.Embed(title = "I Need Manage Roles to Do This", color = discord.Color.red()))
            elif str(error) == "can't view audit log":
                await inter.edit(embed = discord.Embed(title = "I Need View Audit Log to Do This", color = discord.Color.red()))
            elif str(error) == "can't manage user":
                await inter.edit(embed = discord.Embed(title = "I Need Higher Role to Do This", color = discord.Color.red()))
            elif str(error) == "can't find role":
                await inter.edit(embed = discord.Embed(title = "Role is Not Found", color = discord.Color.red()))
            else:
                await inter.edit(embed = discord.Embed(title = "Unknown Error Occurred", color = discord.Color.red()))
                print(error)

            inter.slash_command.reset_cooldown(inter)

def setup(client):
    client.add_cog(AtCommand(client))
    client.add_cog(SlashCommand(client))
