from datetime import time
import re
import tweepy

class twitterscaper:
    def __init__(self, file_name):
        f = open(file_name)
        lines = f.read()
        keys = re.split("\n", lines)
        self.consumer_key = keys[0]
        self.consumer_secret = keys[1]
        self.access_token = keys[2]
        self.access_token_secret = keys[3]
        self.auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        self.auth.set_access_token(self.access_token, self.access_token_secret)
        f.close()

    def get_tweets_from_user(self, username: str, count=3):
        api = tweepy.API(self.auth,wait_on_rate_limit=True)

        tweets = []
        try:
            # Pulling individual tweets from query
            for tweet in api.user_timeline(id=username, count=count):
            # Adding to list that contains all tweets
                tweets.append((tweet.created_at,tweet.text))
        except BaseException as e:
            print('failed on_status,', str(e))
        return tweets

if __name__ == '__main__':
    t = twitterscaper("/home/tpiggo/python-workspace/ImportantFiles/keys")
    print(t.get_tweets_from_user('unusual_whales', 5))