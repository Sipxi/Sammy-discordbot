from settings import *
from discord.ext import commands
import time
import discord


#   Check admin privileges
def owner_or_mods() -> bool:
    original = commands.has_permissions(kick_members = True).predicate
    async def extended_check(ctx):
        if ctx.guild is None:
            return False
        return ctx.guild.owner_id == ctx.author.id or await original(ctx)
    return commands.check(extended_check)


def is_channel_nsfw(channel: discord.TextChannel):
    pass
    
async def notify_member(member: discord.Member, message: str):
    if member is not None:
        channel = member.dm_channel
        if channel is None:
            channel = await member.create_dm()
        await channel.send(message)
        
    
#Timer class
#?  Multiple timers?
class Timer:
    def __init__(self) -> None:
        self.started_time = None

    def start(self) -> None:
        self.started_time = time.time()


    def time_convert(self,sec) -> str:
        mins = sec // 60
        sec = sec % 60
        hours = mins // 60
        mins = mins % 60
        elapsed_time = "Time Lapsed = {0}:{1}:{2}".format(int(hours),int(mins),sec)
        return elapsed_time
    
    def stop(self) -> str:
        end_time = time.time()
        time_lapsed = end_time - self.started_time
        elapsed_time = self.time_convert(time_lapsed)
        return elapsed_time

    def reset(self) -> None:
        self.started_time = None


