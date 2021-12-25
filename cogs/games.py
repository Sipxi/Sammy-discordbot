from discord.ext import commands
from extensions.customCog import CustomCog


from rps.model import RPS
from rps.parser import RockPaperScissorParser
from rps.controller import RPSGame


class Games(CustomCog):
    def __init__(self, bot) -> None:
        super().__init__(bot)
    
    
    @commands.command(usage="rock | paper | scissor", description = "You can play Rock/Paper/Scissor with me!")
    async def rps(self, ctx, user_choice: RockPaperScissorParser = RockPaperScissorParser(RPS.ROCK)) -> None:
        game_instance = RPSGame()

        user_choice = user_choice.choice

        won, bot_choice = game_instance.run(user_choice)
        
        match won:
            case None:
                message = f"{user_choice} vs {bot_choice}. It's a draw! I was about to win!"
            case True:
                message = f"{user_choice} vs {bot_choice}. Ahhh you win this time!"
            case False:
                message = f"{user_choice} vs {bot_choice}. Too easy for me:) Try harder next time please!"

        await ctx.send(message)

def setup(bot) -> None:
    bot.add_cog(Games(bot))