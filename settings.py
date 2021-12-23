import os

#! Debug is hard set
#? Is .env working?
DEBUG = True



#Load settings_files depending on debug status
if DEBUG:
    print("We're in Debug mode")
    from pathlib import Path
    from dotenv import load_dotenv
    env_path = Path(".") / ".env.debug"
    load_dotenv(dotenv_path=env_path)
    from settings_files.development import *
else:
    from dotenv import load_dotenv
    env_path = Path(".") / ".env"
    load_dotenv(dotenv_path=env_path)

    from settings_files.production import *
    print("We're in production mode")