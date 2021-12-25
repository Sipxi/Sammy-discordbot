from discord.ext import commands
from discord.ext.commands.core import guild_only
from extensions.customCog import CustomCog
import asyncpraw
from discord.ext import tasks

from settings import REDDIT_ID, REDDIT_SECRET, REDDIT_ENABLED_SUBREDDITS

from redditstorageparser.redditstorage import RedditStorage
import discord

from extensions.customError import *

# TODO comments, briefs, unsubscribe from all reddits?


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
            
    # Start loop
    @commands.Cog.listener()
    async def on_ready(self) -> None:
        """Bot ready event"""
        self.reddit_loop.start()
        
        
    # Send reddit by command
    @commands.command(help= "Send random reddit post")
    async def reddit(self, ctx, user_subreddit: str = "") -> None:
        async with ctx.channel.typing():
            # If user doesn't specify subreddit, take default one
            chosen_subreddit = await self.reddit.subreddit(REDDIT_ENABLED_SUBREDDITS[0], fetch=True)
            
            # If user_subreddit is allowed fetch it
            if user_subreddit in REDDIT_ENABLED_SUBREDDITS:
                user_subreddit = await self.reddit.subreddit(user_subreddit, fetch=True)
                # If user subreddit is allowed but nsfw
                if user_subreddit.over18 and not ctx.channel.is_nsfw():
                    await ctx.send("I can't send these horny stuff here!")
                else:
                    # If it's good, set the user subreddit to chosen one and send it
                    chosen_subreddit = user_subreddit
                    await self.send_subreddit(ctx.channel.id, chosen_subreddit)
            else:
                await ctx.send(f"I can't send this type of subreddit ->{user_subreddit}, please choose one from: {', '.join(REDDIT_ENABLED_SUBREDDITS)}")

    @guild_only() 
    @commands.command(help = "Subscribe the channel to given reddit posts")
    async def subscribe_reddit(self, ctx, user_subreddit: str = "") -> None:
        async with ctx.channel.typing():
            # If user input is none, return
            if user_subreddit is None:
                await ctx.send("Hey, tell me the subreddit i have to subscribe on~")
                return
            # if user subreddit is allowed
            if user_subreddit in REDDIT_ENABLED_SUBREDDITS:
                try:
                    self.storage.add_subscribiton(user_subreddit, ctx.channel.id)
                    await ctx.send(f"I've successfully subscribed this channel to reddit {user_subreddit} thingy!")
                except isSubscribed:
                    await ctx.send(f"This channel is already subscribed to reddit {user_subreddit} thingy!")
            else:
                await ctx.send(f"I can't subscribe to this type of subreddit -> {user_subreddit}, please choose one from: {', '.join(REDDIT_ENABLED_SUBREDDITS)}")

    @tasks.loop(seconds=10)
    async def reddit_loop(self) -> None:
        subscribtions = self.storage.get_subscribtions()
        # fetching subreddits
        for subreddit_name in subscribtions:
            subreddit = await self.reddit.subreddit(subreddit_name, fetch=True)
            for id in subscribtions[subreddit_name]:
                await self.send_subreddit(id, subreddit)
                print("########################")
                print("Hourly post was successful at")
                print(f"Channel {id}")
                print(f"Theme:  {subreddit_name}")
                print("########################")


    async def send_subreddit(self, channel_id, user_subreddit) -> None:
        #Get the channel by id
        channel = self.bot.get_channel(channel_id)
        
        #Take random submission from subreddit
        submission = await user_subreddit.random()
        
        #Make custom embed and send it 
        embed = await make_reddit_embed(submission)
        await channel.send(embed=embed)

    @commands.command(help= "Unsubscribe the channel to given reddit posts")
    async def unsubscribe_reddit(self, ctx, user_subreddit: str = "") -> None:
        async with ctx.channel.typing():
            if user_subreddit is not None:
                try:
                    self.storage.delete_subscribtions(user_subreddit, ctx.channel.id)
                    await ctx.send(f"I've successfully unsubscribed this channel from {user_subreddit} reddit posts!")
                except badName:
                    await ctx.send(f"Hmmmm, I think this channel is subscribed to {user_subreddit}")
            else:
                await ctx.send("Hey, what do i have to unsubscribe?")
                
def setup(bot) -> None:
    bot.add_cog(Reddit(bot))
