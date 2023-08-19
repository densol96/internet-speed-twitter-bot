from twitter_bot import InternetSpeedTwitterBot

twitter_bot = InternetSpeedTwitterBot()
twitter_bot.get_internet_speed()
twitter_bot.tweet_at_provider(twitter_bot.download_speed, twitter_bot.upload_speed)