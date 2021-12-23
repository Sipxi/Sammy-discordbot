import os


from discord.ext import commands

from settings import *


#Set the bot prefix
bot = commands.Bot(command_prefix="!")


#Load cogs dynamically
for filename in os.listdir("./cogs"):
    if filename.endswith(".py") and filename != "__init__.py":
        bot.load_extension(f'cogs.{filename[:-3]}')

#Start the bot with token
bot.run(DISCORD_BOT_TOKEN)