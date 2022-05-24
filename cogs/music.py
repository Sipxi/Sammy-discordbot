import discord
from discord.ext import commands
from extensions.customCog import CustomCog
import discord.utils
from music_utils.VoiceState import VoiceState
import youtube_dl
import os

# TODO join to the same VC

class Music(CustomCog):
    def __init__(self, bot) -> None:
        super().__init__(bot)
        self.voice_states = {}
    
    
    @commands.command(help = "I'll play you a song!")
    async def testmusic(self,ctx):
        print(self.voice_states)


    def get_voice_state(self, ctx) -> VoiceState:
        state = self.voice_states.get(ctx.guild.id)
        if not state:
            state = VoiceState(self.bot, ctx)
            self.voice_states[ctx.guild.id] = state
        return state
    
    async def cog_before_invoke(self, ctx: commands.Context) -> None:
        """Get voice state before commad invocation"""
        ctx = await super().cog_before_invoke(ctx)
        ctx.voice_state = self.get_voice_state(ctx)

    
    @commands.command(help = "I'll play you a song!")
    async def play(self,ctx, url : str):
        song_there = os.path.isfile("song.mp3")
        try:
            if song_there:
                os.remove("song.mp3")
        except PermissionError:
            await ctx.send("Wait for the current playing music to end or use the 'stop' command")
            return
        
        voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.rename(file, "song.mp3")
        voice_client.play(discord.FFmpegPCMAudio("song.mp3"))
            
    @commands.command(help="I will join you in Voice Channel")
    async def join(self, ctx)-> None:
        if ctx.author.voice is None:
            await ctx.send("You are not in a voice channel!")
            return
        channel = ctx.author.voice.channel
        if ctx.voice_state.voice:  
            await ctx.voice_state.move_to(channel)
        else:
            await ctx.voice_state.connect(channel)     

        
    @commands.command(help="I will leave you:(")
    async def leave(self, ctx)-> None:
        if ctx.voice_state.voice:  
            await ctx.voice_state.disconnect()
            del self.voice_states[ctx.guild.id]
        else:
            await ctx.send("Heeey, i'm not in any voice channel ya now?")
            
    @commands.command(help="I will pause a song ")
    async def pause(self,ctx):
        voice = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            voice.pause()
        else:
            await ctx.send("Currently no audio is playing.")
            
    @commands.command(help="I will resume a song")
    async def resume(self, ctx):
        voice = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        if voice.is_paused():
            voice.resume()
        else:
            await ctx.send("The audio is not paused.")
            
    @commands.command(help="I stop the song from playing")
    async def stop(self,ctx):
        voice = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        voice.stop()
        
def setup(bot):
    bot.add_cog(Music(bot))