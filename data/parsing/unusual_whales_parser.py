import re

from data.parsing.tweet_parser import TweetParser
from utils.string_manipulation import *


class UnusualWhalesParser(TweetParser):
    # @TODO maybe rename the class or something

    def __init__(self, tweet=None):
        self._parsed_tweets = {}

        # allow ability to parse tweets during construction
        if tweet is not None and not isinstance(tweet, list):
            self.parse_tweet(tweet)
        elif tweet is not None:
            self.parse_tweets(tweet)

    def validate_tweet(self, tweet_text):
        # validates the tweets have the valid format for use
        matcher_emoji = ".+\n\$[A-Z]+\s[0-9-]+\s[CP]\s\$[0-9.]+\n\n.+"
        matcher_no_emoji = "\$[A-Z]+\s[0-9-]+\s[CP]\s\$[0-9.]+\n\n.+"
        return bool(re.match(matcher_emoji, tweet_text)) or bool(re.match(matcher_no_emoji, tweet_text))

    def get_parsed_tweets(self):
        return self._parsed_tweets

    def parse_tweets(self, tweets: list):
        # wraps parse_tweet function to allow one call to UnusualWhalesParser
        for tweet in tweets:
            self.parse_tweet(*tweet)

    def parse_tweet(self, user_id, tweet_id, tweet_text: str):
        # single class can parse any tweet by @unusual_whales
        # every time a new tweet is parsed it's just added to the end of the dict
        if (self.validate_tweet(tweet_text)):
            self._parsed_tweets[len(self._parsed_tweets.keys())] = self._create_dict_from_str(user_id, tweet_id, tweet_text)

    @staticmethod
    def _create_dict_from_str(tweet_time, tweet_id, tweet_text: str):
        tweet_lines = remove_empty_entries(re.split('\n', de_emojify(tweet_text)))
        print(tweet_lines)
        # dictionary for the symbol retrieved in the unusual flow call out
        symbol_dict = {}
        for i in range(len(tweet_lines)):
            if i == 0:
                new_entry = re.split(' ', tweet_lines[i])
                for j in range(len(new_entry)):
                    if j == 0:
                        new_entry[i] = new_entry[j].replace('$', '')
                        dict_name = 'Name'
                    elif j == 1:
                        dict_name = 'Expiration Date'
                    elif j == 2:
                        dict_name = 'Type'
                    else:
                        new_entry[i] = new_entry[j].replace('$', '')
                        dict_name = 'Strike'
                    symbol_dict[dict_name] = new_entry[j]
                continue
            new_entry = re.split(": ", tweet_lines[i])

            if len(new_entry) > 1 and '$' in new_entry[1]:
                new_entry[1] = new_entry[1].replace('$', '')
            elif len(new_entry) > 1 and '%' in new_entry[1]:
                new_entry[1] = new_entry[1].replace('%', '')

            if len(new_entry) > 1:
                symbol_dict[new_entry[0]] = float(new_entry[1])
        return {
            'tweet_time': tweet_time,
            'twitter_id': tweet_id,
            **symbol_dict
        }
