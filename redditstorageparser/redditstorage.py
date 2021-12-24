import json

from settings import DATA_DIR

class RedditStorage():
    def __init__(self) -> None:
        self.subreddit_json_path = DATA_DIR + "/subreddits.json"
        self.subscribtions_json_path = DATA_DIR + "/subscriptions.json"
        self.subreddits = self.get_subreddits()
        self.subscribtions = self.get_subscribtions()







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


    def get_subscribtions(self) -> dict:
        """Get subscribtions from subreddits local json file"""
        try:
            with open(
                self.subscribtions_json_path, "r", encoding="utf-8"
            ) as subscribtion_file:
                subscribtions = json.load(subscribtion_file)
        except FileNotFoundError:
            print("Error FNFE")
            with open(
                self.subscribtions_json_path, "w", encoding="utf-8"
            ) as subscribtion_file:
                subscribtions = {}
                json.dump(subscribtions, subscribtion_file, indent=4) #!indent? max json capacity?
        return subscribtions


    def save_subscribtions(self) -> None:
        """Save subscribtions to local json file"""
        with open(self.subscribtions_json_path, "w", encoding="utf-8") as subscribtion_file:
            json.dump(self.subscribtions, subscribtion_file, indent=4)

    def add_subscribiton(self, subreddit, channel_id) -> None:
        # If dict is empty
        if not bool(self.subscribtions):
            self.subscribtions.update({subreddit: [channel_id]})
            print("Empty dict")
        else:

            for theme in self.subscribtions:
                #If subreddit is already in json
                if subreddit == theme:
                    for id in self.subscribtions[theme]:
                        # channel id is already subscribed
                        if id != channel_id:
                            self.subscribtions[subreddit] .append(channel_id)
                            break
                        else:
                            self.subscribtions.update({subreddit: [channel_id]})
        self.save_subscribtions()



