#   Get the token 
#   Share global settings to both production and development
import os 
#TODO comments



#Set the data directory
SETTINGS_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SETTINGS_DIR)
DATA_DIR = os.path.join(ROOT_DIR, 'data')
    
#Get token from environment
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN", False)


#Reddit configuration
REDDIT_ID = os.getenv("REDDIT_ID", False)
REDDIT_SECRET = os.getenv("REDDIT_SECRET", False)
REDDIT_ENABLED_SUBREDDITS = ["funny", "memes", "nsfw"]


