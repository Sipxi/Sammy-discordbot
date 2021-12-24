import json

from settings import DATA_DIR

from customError import isSubscribed

class RedditStorage:
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
                json.dump(
                    subreddits, subreddits_file, indent=4
                )  #!indent? max json capacity?
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
                json.dump(
                    subscribtions, subscribtion_file, indent=4
                )  #!indent? max json capacity?
        return subscribtions


    def save_subscribtions(self) -> None:
        """Save subscribtions to local json file"""
        with open(
            self.subscribtions_json_path, "w", encoding="utf-8"
        ) as subscribtion_file:
            json.dump(self.subscribtions, subscribtion_file, indent=4)

    def add_subscribiton(self, subreddit, channel_id) -> None:
        # If dict is empty
        if not bool(self.subscribtions):
            # Add subscribtion to json file and save it
            self.subscribtions.update({subreddit: [channel_id]})
            self.save_subscribtions()
            return
        #If subbredit is in subscriptions
        if subreddit in self.subscribtions:
            #iIf channel is not subscribed
            if not channel_id in self.subscribtions[subreddit]:
                self.subscribtions[subreddit].append(channel_id)
            else:
                raise isSubscribed
        else:
            #If not is not in subscriptions
            self.subscribtions.update({subreddit: [channel_id]})
        self.save_subscribtions()

    def delete_subscribtions(self, user_subreddit, channel_id):
        #If subreddit is in subscribed subrredits
        if user_subreddit in self.subscribtions:
            # Unsubscribe subscription from this channel
            if channel_id in self.subscribtions[user_subreddit]:
                self.subscribtions[user_subreddit].remove(channel_id)
                # If subrredit doesn't have any channels, delete it
                if not self.subscribtions[user_subreddit]:
                    self.subscribtions.pop(user_subreddit)
        else:
            raise Exception("Couldn't find sub")
        self.save_subscribtions()
                
