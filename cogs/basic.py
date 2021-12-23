from discord.ext import commands
from extensions.customCog import CustomCog
from TextToOwO.owo import text_to_owo



class Basic(CustomCog):
    def __init__(self, bot) -> None:
        super().__init__(bot)
        
    
    
    
    #? Unneeded line?
    @commands.Cog.listener()
    async def on_command_error(self, ctx, ex)  -> None:
        print(ex)
        await ctx.send("Please check with !help the usage of this command")

    @commands.command()
    async def owo(self, ctx) -> None:
        #Send the text with owo thing
        await ctx.send(text_to_owo(ctx.message.content))
    
    
    @commands.command()
    @commands.guild_only()
    async def invite(self, ctx) -> None:
        link = await ctx.channel.create_invite(max_age=1)
        await ctx.send(link)
        
        
    @commands.command()
    async def ping(self, ctx) -> None:
        await ctx.send("Pong!")
    
    
def setup(bot) -> None:
    bot.add_cog(Basic(bot))