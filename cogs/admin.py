from discord.ext import commands
from extensions.customCog import CustomCog
import discord

#TODO unload/reload/load cog
#TODO brief
#? Is not working?


class Admin(CustomCog):
    def __init__(self, bot) -> None:
        super().__init__(bot)

    @commands.command()
    async def status(self, ctx, *args) -> None:
        #Making embed for status
        embed = discord.Embed(
            title=ctx.guild.name,
            description=f"Description: {ctx.guild.description}",
            color=0xFF0000,
        )
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.add_field(name="🆔", value=ctx.guild.id, inline=False)
        embed.add_field(name="Created", value=ctx.guild.created_at, inline=False)
        embed.add_field(name="👑 Owner 👑", value=ctx.guild.owner, inline=False)
        embed.add_field(
            name="#Text Channels", value=len(ctx.guild.text_channels), inline=True
        )
        embed.add_field(
            name="# Voice Channels", value=len(ctx.guild.voice_channels), inline=True
        )
        embed.add_field(name="# AFK Channel", value=ctx.guild.afk_channel, inline=True)
        embed.set_footer(text=f"{ctx.guild.member_count}👪")

        await ctx.send(embed=embed)


def setup(bot) -> None:
    bot.add_cog(Admin(bot))
