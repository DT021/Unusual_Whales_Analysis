from abc import ABC, abstractmethod


class TweetParser(ABC):

    @abstractmethod
    def parse_tweet(self, user_id, tweet_id, tweet_text: str):
        pass

    @abstractmethod
    def parse_tweets(self, tweets: list):
        pass

    @abstractmethod
    def get_parsed_tweets(self):
        pass
