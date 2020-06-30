import os
import re
import tweepy
import requests
import importlib
from typing import Optional
from datetime import datetime
from dotenv import load_dotenv

from data.parsing import tweet_parser
from data.parsing import parser_associations
from webapp import webapp_parent


PARSER_PATH = 'data.parsing.'


class TwitterScraper:

    def __init__(self, file_name=None, account=None):
        self._file_name = file_name
        self._consumer_key = None
        self._consumer_secret = None
        self._access_token = None
        self._access_token_secret = None
        self._auth = None
        self._account = None
        self._parser: Optional[tweet_parser.TweetParser] = None

        self._load_config(file_name)

        self._api = tweepy.API(self._auth, wait_on_rate_limit=True)
        self.formatted_tweets = None

        if account is not None:
            self.set_account(account)

    def set_account(self, account):
        if account in parser_associations.ASSOCIATIONS['accounts'].keys():
            # parsing logic has been set for account's tweets
            self._account = account
            self._load_parser(parser_associations.ASSOCIATIONS['accounts'][account])
        else:
            raise Exception('Invalid account. No associated parsing logic.')

    def _load_parser(self, association):
        # load the class name
        class_ = getattr(importlib.import_module(f'{PARSER_PATH}{association["module"]}'), association['class_name'])
        # instantiate
        self._parser = class_(self._file_name)

    def _load_config(self, file_name=None):
        if file_name is not None:
            # read the credentials
            with open(file_name, 'r') as f:
                lines = f.read()
                keys = re.split("\n", lines)
                self._consumer_key = keys[0]
                self._consumer_secret = keys[1]
                self._access_token = keys[2]
                self._access_token_secret = keys[3]
                f.close()

        else:
            # load in configuration
            load_dotenv(os.path.join(webapp_parent, '.env'))
            if 'TWITTER_CONSUMER_KEY' not in os.environ.keys():
                raise Exception('No configuration found')
            else:
                self._consumer_key = os.environ.get('TWITTER_CONSUMER_KEY')
                self._consumer_secret = os.environ.get('TWITTER_CONSUMER_SECRET')
                self._access_token = os.environ.get('TWITTER_ACCESS_TOKEN')
                self._access_token_secret = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')

        self._auth = tweepy.OAuthHandler(self._consumer_key, self._consumer_secret)
        self._auth.set_access_token(self._access_token, self._access_token_secret)

    def get_tweets_from_user(self, count=3):
        def format_tweet(tweet):
            return tweet.created_at.strftime('%Y-%m-%d'), tweet.id, tweet.text

        # try:
            # Pulling individual tweets from query
        twitter_response = self._api.user_timeline(id=self._account.replace("@", ""), count=count)
        self._parser.parse_tweets([
                format_tweet(tweet) for tweet in twitter_response
            ])

        # except BaseException as e:
        #     print('failed on_status,', str(e))

    def format_tweets_for_upload(self):

        def format_key(k):
            return k.lower().replace(' ', '_').replace('%', 'pct')

        def format_value(v):
            if isinstance(v, str) and '$' in v:
                v = float(v.replace('$', ''))
            return v

        def format_tweet(tweet):
            return {
                **{format_key(k): format_value(v) for k, v in tweet.items()},
                'account_id': account_info['id'],
                'scraped_on': datetime.now().strftime('%Y-%m-%d')
            }

        def valid(tweet):
            res = tweet['twitter_id'] not in account_info['tweet_ids']
            return res

        account_info = requests.get(f'http://127.0.0.1:5000/api/followed_accounts/handle/{self._account}').json()
        self.formatted_tweets = [
            format_tweet(tweet) for _, tweet in self._parser.get_parsed_tweets().items() if valid(tweet)
        ]

    def upload_tweets(self):
        requests.post(f'http://127.0.0.1:5000/api/upload_tweets', json=self.formatted_tweets)
