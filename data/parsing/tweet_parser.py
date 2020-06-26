from abc import ABC, abstractmethod


class TweetParser(ABC):

    @abstractmethod
    def parse_tweet(self, tweet_text):
        pass

    @abstractmethod
    def parse_tweets(self, tweets: list):
        pass
