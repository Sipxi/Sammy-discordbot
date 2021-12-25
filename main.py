import os
import discord
from settings import *
from discord.ext import commands
import pretty_errors


pretty_errors.activate()
#Set intents to get members
intents = discord.Intents.default()  
intents.members = True  
#Set bot prefix
bot = commands.Bot(command_prefix="!", intents=intents)
bot.remove_command('help')

@bot.event
async def on_ready():
    activity = discord.Activity(type=discord.ActivityType.watching, name="灰と幻想のグリムガル")
    await bot.change_presence(activity=activity)
    print("Ready for action!")

#Load cogs dynamically
for filename in os.listdir("./cogs"):
    if filename.endswith(".py") and filename != "__init__.py":
        bot.load_extension(f'cogs.{filename[:-3]}')
        print(f"{filename} is loaded" )
#Start the bot with token
bot.run(DISCORD_BOT_TOKEN)