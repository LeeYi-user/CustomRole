import discord
from discord.ext import commands
from dislash import slash_commands

client = commands.Bot(command_prefix = commands.when_mentioned, intents = discord.Intents(guilds = True, members = True, messages = True))
slash = slash_commands.SlashClient(client)
client.remove_command("help")

if __name__ == "__main__":
    client.load_extension("react.cmd")
    client.load_extension("react.event")
    client.load_extension("core")
    client.run("token")
