from discord.ext import commands


#? logger, more info, error handler?

class CustomCog(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
    
    
