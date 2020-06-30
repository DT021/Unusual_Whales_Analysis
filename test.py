from data.scraping.twitter.scraper import TwitterScraper


def main():
    twitter_scraper = TwitterScraper( account='@unusual_whales')
    twitter_scraper.get_tweets_from_user(1000)
    twitter_scraper.format_tweets_for_upload()
    twitter_scraper.upload_tweets()


if __name__ == "__main__":
    main()
