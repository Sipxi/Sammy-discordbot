from discord.ext import commands
from extensions.customCog import CustomCog
from TextToOwO.owo import text_to_owo
import random
import discord
from extensions.utils import notify_member
class Basic(CustomCog):
    def __init__(self, bot) -> None:
        super().__init__(bot)

    
    #? Unneeded line?
    @commands.Cog.listener()
    async def on_command_error(self, ctx, ex)  -> None:
        print(ex)
        await ctx.send("Please check with !help the usage of this command")

    @commands.command(help = "Sending your text with owo thingy:)")
    async def owo(self, ctx) -> None:
        #Send the text with owo thing
        await ctx.send(text_to_owo(ctx.message.content))
    
    
    @commands.command(help = "I'll create invite for the server")
    @commands.guild_only()
    async def invite(self, ctx) -> None:
        link = await ctx.channel.create_invite(max_age=100)
        await ctx.send(link)
        
        
    @commands.command(help ="Pong:)")
    async def ping(self, ctx) -> None:
        await ctx.send("Pong!")
    
    
    @commands.command(
        help="... my creator is very bad", description="... my creator is very bad"
    )
    async def fuck(self, ctx, member: discord.Member = None):
        message = f"{ctx.author.name} cursed you. Pew Pew"
        await ctx.send("I cursed him/her! Now he/she is sad, i hate you!:(")
        await notify_member(member, message)
    
    @commands.command(description="Ask any question to the bot.", help = "use !sammy please [question]")
    async def sammy_please(self, ctx, *, question: str):
        
        answers = ['It is certain.', 'It is decidedly so.', 'You may rely on it.', 'Without a doubt.',
                   'Yes - definitely.', 'As I see, yes.', 'Most likely.', 'Outlook good.', 'Yes.',
                   'Signs point to yes.', 'Reply hazy, try again.', 'Ask again later.', 'Better not tell you now.',
                   'Cannot predict now.', 'Concentrate and ask again later.', 'Don\'t count on it.', 'My reply is no.',
                   'My sources say no.', 'Outlook not so good.', 'Very doubtful.']
        
        embed = discord.Embed(
            title="**My Answer:**",
            description=f"{random.choice(answers)}",
            color=0x9C84EF
        )
        embed.set_footer(
            text=f"The question was: {question}"
        )
        await ctx.send(embed=embed)
    
def setup(bot) -> None:
    bot.add_cog(Basic(bot))