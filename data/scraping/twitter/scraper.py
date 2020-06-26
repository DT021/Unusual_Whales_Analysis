import re
import tweepy
import importlib
from typing import Optional

from data.parsing import parser_associations


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
        self._parser = None  # type: Optional[tweet_parser.TweetParser]

        self._load_config(file_name)

        self._api = tweepy.API(self._auth, wait_on_rate_limit=True)

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
        # TODO set up our environments so that the keys are automatically taken from them, maybe using netrc config
        #  or something
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

            self._auth = tweepy.OAuthHandler(self._consumer_key, self._consumer_secret)
            self._auth.set_access_token(self._access_token, self._access_token_secret)
        else:
            print('No credentials!!!')
            raise Exception('Missing credentials')

    def get_tweets_from_user(self, count=3):

        try:
            # Pulling individual tweets from query
            twitter_response = self._api.user_timeline(id=self._account.replace("@", ""), count=count)
            self._parser.parse_tweets([
                tweet.text for tweet in twitter_response
            ])

        except BaseException as e:
            print('failed on_status,', str(e))
