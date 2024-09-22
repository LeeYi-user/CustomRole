import discord, json
from discord.ext import commands

class Cog(commands.Cog):
    def __init__(self, client):
        self.client = client

class Core(Cog):
    async def help(command):
        if command == None:
            return discord.Embed(title = "Commands", description = "`/get <name> [color]`\nGet the custom role\n\u200B\n`/help [command]`\nHelp with custom role\n\u200B\n`/remove`\nRemove the custom role", color = discord.Color.orange())
        elif command == "get":
            return discord.Embed(title = "Example", description = "`/get name:King color:orange`", color = discord.Color.orange())
        elif command == "help":
            return discord.Embed(title = "Example", description = "`/help command:get`", color = discord.Color.orange())
        elif command == "remove":
            return discord.Embed(title = "Example", description = "`/remove`", color = discord.Color.orange())

        raise LookupError("can't find command")

    async def check(intext):
        try:
            permission = intext.guild.me.permissions_in(intext.channel)
        except:
            raise ConnectionError("can't use here")

        if permission.manage_roles == False:
            raise PermissionError("can't manage roles")
        elif permission.view_audit_log == False:
            raise PermissionError("can't view audit log")

    async def find(guild, member):
        roles = []
        for role in member.roles:
            roles.append(role)

        async for log in guild.audit_logs(limit = None, user = guild.me, action = discord.AuditLogAction.role_create):
            if log.target in roles:
                if log.target.position >= guild.me.top_role.position:
                    raise PermissionError("can't manage user")

                return log.target

    async def get(intext, name, color):
        await Core.check(intext)
        role = await Core.find(intext.guild, intext.author)

        if len(intext.guild.roles) >= 250:
            raise MemoryError("can't create role")
        elif len(name) > 100:
            raise NameError("can't set name")

        with open("color_names.json") as f:
            color_names = json.loads(f.read())

        try:
            color = int(color_names[color.lower()].replace("#", "0x"), 16)
        except:
            try:
                if color[0] != "#":
                    raise

                color = int(color.replace("#", "0x"), 16)

                if (color > 16777215) or (color < 0):
                    raise
            except:
                raise LookupError("can't find color")

        if role != None:
            await role.delete()

        role = await intext.guild.create_role(name = name, color = discord.Color(color))
        for i in range(intext.me.top_role.position, 0, -1):
            try:
                await intext.guild.edit_role_positions(positions = {role: i})
                break
            except:
                pass

        await intext.author.add_roles(role)
        return discord.Embed(title = f"You Have Got the \"{role.name}\" Role", color = discord.Color.orange())

    async def remove(intext):
        await Core.check(intext)
        role = await Core.find(intext.guild, intext.author)

        if role != None:
            await role.delete()
            return discord.Embed(title = f"You Have Removed the \"{role.name}\" Role", color = discord.Color.orange())
        else:
            raise LookupError("can't find role")

def setup(client):
    client.add_cog(Core(client))
