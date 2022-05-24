from discord.ext import commands


#? logger, more info, error handler?

class CustomCog(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.hidden = False
    
    async def cog_before_invoke(self, ctx: commands.Context) -> commands.Context:
        """Code that runs before invoked command.
        Used for logging chat commands.
        """
        return ctx
