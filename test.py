from data.scraping.twitter.scraper import TwitterScraper

def main():
    twitter_scraper = TwitterScraper('C://Users/User/Downloads/keys', '@unusual_whales')
    twitter_scraper.get_tweets_from_user(10)

if __name__ == "__main__":
    main()
