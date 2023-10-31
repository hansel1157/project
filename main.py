import discord 
from discord.ext import commands
import os 


from help_cog import help_cog
from music_cog import music_cog

Bot = commands.Bot(command_prefix = "/")

Bot.add_cog(help_cog(Bot))
Bot.add_cog(music_cog(Bot))

Bot.run(os.getenv("TOKEN"))