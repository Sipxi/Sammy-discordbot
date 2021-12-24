from discord.ext import commands
from discord.ext.commands.core import guild_only
from extensions.customCog import CustomCog
import asyncpraw
from discord.ext import tasks

from settings import REDDIT_ID, REDDIT_SECRET, REDDIT_ENABLED_SUBREDDITS

from redditstorageparser.redditstorage import RedditStorage
import discord

#TODO comments, brief, hourlyreddit
#?different reddits/nsfw commands?


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
        self.storage = RedditStorage()
        if REDDIT_ID and REDDIT_SECRET:
            self.reddit = asyncpraw.Reddit(
                client_id=REDDIT_ID,
                client_secret=REDDIT_SECRET,
                user_agent="Sammy Draitor:%s:1.0" % REDDIT_ID,
            )
    @commands.Cog.listener()
    async def on_ready(self) -> None:
        """Bot ready event"""
        # self.test.start() 


    @commands.command()
    async def reddit(self, ctx, user_subreddit: str = "") -> None:
        async with ctx.channel.typing():
            # If user doesn't specify subreddit, take default one
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
            await self.send_subreddit(ctx.channel.id, chosen_subreddit)
    

    
    
    @guild_only()
    @commands.command()
    async def subscribe_reddit(self, ctx, user_subreddit: str= "") -> None:
        async with ctx.channel.typing():
            if self.reddit:
                # If instance start
                if user_subreddit in REDDIT_ENABLED_SUBREDDITS:
                    if user_subreddit is not None:
                        self.storage.add_subscribiton(user_subreddit, ctx.channel.id)
                        await ctx.send(f"I've successfully subscribed this channel to reddit {user_subreddit} thingy!")
                    else:
                        await ctx.send("Hey, tell me the subreddit i have to subscribe on~")
                        return
                else:
                        await ctx.send("Hey, tell me the subreddit i have to subscribe on~")
                        return
                    
    
    # @tasks.loop(hours=1)
    # async def test(self):
    #     channels = self.storage.get_subscribtions()
    #     # fetching subreddits
    #     for subreddit_name in channels:
    #         subreddit = await self.reddit.subreddit(subreddit_name, fetch=True)
    #         await self.send_subreddit(channels[subreddit_name], subreddit)
    #         print("Hourly post was successful at")
    #         print(f"Channel {channels[subreddit_name]}")
    #         print(f"Theme:  {subreddit_name}")
            
    async def send_subreddit(self, channel_id, user_subreddit) -> None:
        channel = self.bot.get_channel(channel_id)
        submission = await user_subreddit.random()
        embed = await make_reddit_embed(submission)
        await channel.send(embed=embed)       
            
             
def setup(bot) -> None:
    bot.add_cog(Reddit(bot))
