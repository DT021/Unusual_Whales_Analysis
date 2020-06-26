from data.scraping.twitter.scraper import TwitterScraper


def main():
    twitter_scraper = TwitterScraper('/home/paul/personal-repos/.personal-info/keys.yek', '@unusual_whales')
    twitter_scraper.get_tweets_from_user(5)

if __name__ == "__main__":
    main()
