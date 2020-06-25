from TwitterScraper import TwitterScraper
import Analysis


class UnusualWhales:
    def __init__(self, key_file: str):
        self.tscraper = TwitterScraper(key_file)

    def create_data(self):
        tweets = self.tscraper.get_tweets_from_user("unusual_whales",5)
        Analysis.create_dict_from_str(tweets[0][1])