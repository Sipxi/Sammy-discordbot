import os
import discord
from settings import *
from discord.ext import commands
import pretty_errors


class SammyBot(commands.Bot):

    def __init__(self):
        #   Set intents
        intents = discord.Intents.default()  
        intents.members = True  
        
        super().__init__(command_prefix=self.prefix, intents =intents,case_insensitive=True)
        
        #   Remove help message to make a custom one
        self.remove_command('help')
        
    def setup(self): 
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py") and filename != "__init__.py":
                self.load_extension(f'cogs.{filename[:-3]}')
                print(f"{filename} is loaded" )
    
    async def activity(self):
        activity = discord.Activity(type=discord.ActivityType.watching, name="灰と幻想のグリムガル")
        await self.change_presence(activity=activity)
        print("Ready for action!")
    
    def run(self):
        self.setup()
        super().run(DISCORD_BOT_TOKEN, reconnect = True)
    
    async def shutdown(self):
        print("Closing connection to Discord...")
        await super().close()
    
    async def on_resumed(self):
        print("Bot resumed.")
    
    async def on_disconnect(self):
        print("Bot disconnected.")

    async def on_ready(self):
        self.client_id = (await self.application_info()).id
        await self.activity()
    
    async def on_connect(self):
        print(f"Connected to Discord (latency: {self.latency*1000:,.0f} ms).")
        
    async def close(self):
        print("Closing connection due keyboard interrupt...")
        await self.shutdown()
    
    async def prefix(self, bot, msg):
        #   Set bot prefix
        return commands.when_mentioned_or("!")(bot,msg)
    
    async def process_commands(self, msg):
        ctx = await self.get_context(msg, cls=commands.Context)

        if ctx.command is not None:
            await self.invoke(ctx)
    
    async def on_message(self, msg):
        if not msg.author.bot:
            await self.process_commands(msg)
        
        
        
def main():
    pretty_errors.activate()
    bot = SammyBot()
    bot.run()


if __name__ == "__main__":
    main()
