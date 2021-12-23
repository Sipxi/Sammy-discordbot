from discord.ext import commands
from extensions.customCog import CustomCog
import aiohttp
import discord

#TODO comments, brief,

class Images(CustomCog):
    def __init__(self, bot) -> None:
        super().__init__(bot)

    @commands.command()
    async def cat(self, ctx) -> None:
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get("https://aws.random.cat/meow") as r:
                    data = await r.json()
                    embed = discord.Embed(title="Meow")
                    embed.set_image(url=data["file"])
                    embed.set_footer(text="A picture of a cat! Meow;)")
                    await ctx.send(embed=embed)

    @commands.command()
    async def fox(self, ctx) -> None:
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get("https://randomfox.ca/floof/") as r:
                    data = await r.json()
                    embed = discord.Embed(title="Foxy")
                    embed.set_image(url=data["image"])
                    embed.set_footer(text="A picture of a foxy! :)")
                    await ctx.send(embed=embed)

    @commands.command()
    async def dog(self, ctx) -> None:
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get("https://dog.ceo/api/breeds/image/random") as r:
                    data = await r.json()
                    embed = discord.Embed(title="Woof")
                    embed.set_image(url=data["message"])
                    embed.set_footer(text="A picture of a dog! Woof-woof!")
                    await ctx.send(embed=embed)


def setup(bot) -> None:
    bot.add_cog(Images(bot))
