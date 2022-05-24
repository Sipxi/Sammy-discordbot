import asyncio
import discord

from async_timeout import timeout
from discord.ext import commands




class VoiceState:
    def __init__(self, bot: commands.Bot, ctx: commands.Context) -> None:
        """Init voice state"""
        self.bot = bot
        self.ctx = ctx

        self.current = None
        self.voice = None
        self.next = asyncio.Event()


        self.loop = False
        self._volume = 0.5
    
    
    async def move_to(self, destination: discord.VoiceChannel) -> None:
        #   Moves to voice channel
        await self.voice.move_to(destination)
    
    async def connect(self, destination: discord.VoiceChannel) -> None:
        # Connects to voice channel
        self.voice = await destination.connect()
        
    async def disconnect(self) -> None:
        await self.voice.disconnect()
        self.voice = None
        