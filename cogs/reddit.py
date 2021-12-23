from discord.ext import commands
from extensions.customCog import CustomCog
from TextToOwO.owo import text_to_owo
import asyncpraw
from settings import REDDIT_ID, REDDIT_SECRET, REDDIT_ENABLED_SUBREDDITS, DATA_DIR
import discord
import json


#TODO comments, brief, hourlyreddit
#?different reddits/nsfw commands?
#? json is needed?


async def make_reddit_embed(submission) -> discord.Embed:
    await submission.load()
    await submission.author.load()
    embed = discord.Embed(
        title=submission.title,
        url="https://reddit.com" + submission.permalink,
        description=submission.selftext,
        color=0xFF0000,
    )
    embed.set_author(name=submission.author, icon_url=submission.author.icon_img)
    embed.set_footer(
        text=f"From {submission.author} | ⬆️ {submission.score} | 💬 {submission.num_comments}",
    )
    if submission.url.startswith("https://i"):
        embed.set_image(url=submission.url)
    else:
        embed.add_field(
            name="Unfortunately, I can't play the video. But I have a link for you! Here you go!",
            value=submission.url,
        )
    return embed


class Reddit(CustomCog):
    def __init__(self, bot):
        super().__init__(bot)
        self.reddit = None
        self.subreddit_json_path = DATA_DIR + "/subreddits.json"
        self.subreddits = self.get_subreddits()

        if REDDIT_ID and REDDIT_SECRET:
            self.reddit = asyncpraw.Reddit(
                client_id=REDDIT_ID,
                client_secret=REDDIT_SECRET,
                user_agent="Sammy Draitor:%s:1.0" % REDDIT_ID,
            )

    def get_subreddits(self) -> dict:
        """Get subreddits from subreddits local json file"""
        try:
            with open(
                self.subreddit_json_path, "r", encoding="utf-8"
            ) as subreddits_file:
                subreddits = json.load(subreddits_file)
        except FileNotFoundError:
            print("Error FNFE")
            with open(
                self.subreddit_json_path, "w", encoding="utf-8"
            ) as subreddits_file:
                subreddits = {}
                json.dump(subreddits, subreddits_file, indent=4) #!indent? max json capacity?
        return subreddits

    def save_subreddits(self) -> None:
        """Save subreddits to local json file"""
        with open(self.subreddit_json_path, "w", encoding="utf-8") as subreddits_file:
            json.dump(self.subreddits, subreddits_file, indent=4)

    @commands.command()
    async def reddit(self, ctx, user_subreddit: str = "") -> None:
        async with ctx.channel.typing():
            chosen_subreddit = await self.reddit.subreddit(
                REDDIT_ENABLED_SUBREDDITS[0], fetch=True
            )
            if self.reddit:
                # If instance start
                if user_subreddit in REDDIT_ENABLED_SUBREDDITS:
                    user_subreddit = await self.reddit.subreddit(
                        user_subreddit, fetch=True
                    )
                    # If user subreddit is allowed but nsfw
                    if user_subreddit.over18 and not ctx.channel.is_nsfw():
                        await ctx.send("I can't send these horny stuff here!")
                        return
                    else:
                        chosen_subreddit = user_subreddit
            submission = await chosen_subreddit.random()
            embed = await make_reddit_embed(submission)
            await ctx.send(embed=embed)
            self.subreddits.update({submission.id: []})
            self.save_subreddits()


def setup(bot) -> None:
    bot.add_cog(Reddit(bot))
