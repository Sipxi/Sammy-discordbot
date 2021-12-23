import random

from discord.ext import commands
from extensions.customCog import CustomCog



class Gamble(CustomCog):
    def __init__(self, bot) -> None:
        super().__init__(bot)
        

    @commands.command(brief="Gives a random number between 1 and 100")
    async def roll(self, ctx)-> None:
        n = random.randrange(1, 101)
        await ctx.send(n)

    @commands.command(brief="Random number between 1 and 6")
    async def dice(self, ctx)-> None:
        n = random.randrange(1, 6)
        await ctx.send(n)

    @commands.command(brief="Either Heads or Tails")
    async def coin(self, ctx)-> None:
        n = random.randint(0, 1)
        await ctx.send("Heads" if n == 1 else "Tails")

def setup(bot):
    bot.add_cog(Gamble(bot))