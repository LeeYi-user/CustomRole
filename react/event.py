import discord
from discord.ext import commands
from core import *

class Event(Cog):
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.client.user} has online")
        await self.client.change_presence(activity = discord.Activity(type = discord.ActivityType.playing, name = "/help | @bot help"))

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        pass

    @commands.Cog.listener()
    async def on_slash_command_error(self, inter, error):
        pass

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        try:
            role = await Core.find(member.guild, member)
            await role.delete()
        except:
            pass

def setup(client):
    client.add_cog(Event(client))
