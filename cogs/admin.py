from discord import channel
from discord.ext import commands
from extensions.customCog import CustomCog
import discord
from extensions.utils import notify_member
from extensions.utils import owner_or_mods

from extensions.utils import permission_check
# TODO brief error handlers




class Admin(CustomCog, description="Admin commands"):
    def __init__(self, bot) -> None:
        super().__init__(bot)
        
    async def cog_check(self, ctx):
         return permission_check(ctx)
    
    
    
    @owner_or_mods()
    @commands.command(help = "I'll get the status of the server")
    async def status(self, ctx, *args) -> None:
        # Making embed for status
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


    @commands.command(help = "I'll unlaod the cog")
    async def unload(self, ctx, cog_name: str) -> None:
        try:
            self.bot.unload_extension(f"cogs.{cog_name.lower()}")
        except Exception as e:
            await ctx.send("I can't unload this cog for some reason")
            print(e)
            return
        await ctx.send("I've unloaded cog this cog, yay!")


    @commands.command(help = "I'll load the cog")
    async def load(self, ctx, cog_name: str) -> None:
        try:
            self.bot.load_extension(f"cogs.{cog_name.lower()}")
        except Exception as e:
            await ctx.send("I can't load this cog for some reason")
            print(e)
            return
        await ctx.send("I've loaded cog this cog, yay!")


    @commands.command(help = "I'll reload the cog")
    async def reload(self, ctx, cog_name: str) -> None:
        try:
            self.bot.unload_extension(f"cogs.{cog_name.lower()}")
            self.bot.load_extension(f"cogs.{cog_name.lower()}")
        except Exception as e:
            await ctx.send("I can't reload this cog for some reason")
            print(e)
            return
        await ctx.send("I've reloaded cog this cog, yay!")


    @commands.command(help= "I'll kick the member")
    async def kick(
        self, ctx, member: discord.Member = None, reason: str = "Because"
    ) -> None:
        if member is not None:
            await ctx.guild.kick(member, reason=reason)
            await ctx.send(f" I kicked this guy:( -------> {member}")
        else:
            await ctx.send(
                "Couldn't kick this guy, maybe because I can't find him? Specify please with @mention"
            )

    @commands.command(help= "I'll ban the member")
    async def ban(
        self, ctx, member: discord.Member = None, reason: str = "Horny morny you got banned:( "
    ) -> None:
        if member is not None:
            await ctx.guild.ban(member, reason=reason)
            await ctx.send(f" I banned this guy:( -------> {member}")
        else:
            await ctx.send(
                "Couldn't ban this guy, maybe because I can't find him? Specify please with @mention"
            )


    @commands.command(help = "I'll unban the member")
    async def unban(self, ctx, member: str, reason: str = "Because") -> None:
        bans = await ctx.guild.bans()
        if member is not None:
            for b in bans:
                if b.user.name == member:
                    
                    await ctx.guild.unban(b.user, reason=reason)    
                    await ctx.send(f" I unbanned this guy, happy to hear! -------> {member}")
        else:
            await ctx.send(
                "Couldn't unban this guy, maybe because i can't find him? Don't use @mention btw, just write he's nickname:)"
            )
    
    
    @commands.command(help = "I'll bang the player in DM", description = "I'll bang the player in DM")
    async def bang(self, ctx, member: discord.Member = None):
        message = f"{ctx.author.name} banged you. Pew Pew 🔫"
        await ctx.send("I banged him/her! Now he/she is dead, how dare you?:(")
        await notify_member(member, message)
    
    @commands.command()
    async def chr(self, ctx, member: discord.Member = None):
        message = f"🎅🎅🎅Merry Christmas bro! That's from him:)--->{ctx.author.name} "
        await notify_member(member, message)
def setup(bot) -> None:
    bot.add_cog(Admin(bot))
