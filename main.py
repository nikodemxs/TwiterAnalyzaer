import os
import sys
import time
import questionary
from dotenv import load_dotenv
from src.constants.main import STOCK_API_KEY, TWITTER_BEARER_TOKEN
from src.apis.twitter_api import TwitterApi
from src.apis.stock_api import StockAPI
from src.utils.logger import Logger
from src.utils.config import load_config, get_ceo_by_config_name
from src.utils.analysis import analyze_sentiment, analyze_correlation
from src.utils.date import TimeFrameError, calculate_date_range
from src.utils.export import export_to_csv, export_to_xlsx, export_to_json, print_in_console

load_dotenv()
logger = Logger("Script runner")
config = load_config()
availableCEOs = config["availableCEOs"]

selected_ceo_name = questionary.select(
        "Choose a CEO whose tweets you want to compare to auction data",
        choices=[ceo["name"] for ceo in availableCEOs]).ask()

ceo = get_ceo_by_config_name(availableCEOs, selected_ceo_name)

twitter_api = TwitterApi(bearer_token=os.getenv(TWITTER_BEARER_TOKEN))
stock_api = StockAPI(api_key=os.getenv(STOCK_API_KEY))

tweets = twitter_api.fetch_user_tweets(ceo["twitterAccountName"], 100)

if tweets is None:
    logger.error("Something went wrong with fetching tweets")
    sys.exit(1)

logger.debug(f"Collected tweets: {tweets}")
logger.info(f"Collected {len(tweets)} tweets")

output_data = []

for(i, tweet) in enumerate(tweets):
    try:
        logger.info(f"Analyzing tweet {i+1}/{len(tweets)}")
        sentiment = analyze_sentiment(tweet['text'])
        date_from, date_to = calculate_date_range(tweet['created_at'])

        logger.debug(f"Sentiment: {sentiment}")
        logger.debug(f"Date from: {date_from}")
        logger.debug(f"Date to: {date_to}")

        stock_data = stock_api.fetch_stock_data(ceo["marketSymbol"], date_from, date_to)

        logger.debug(f"Stock data: {stock_data}")

        if stock_data is None or stock_data == []:
            logger.debug(f"No data found for the action within the specified time range: {date_from} - {date_to}")
            continue

        stock_30_m_before_tweet, stock_30_m_after_tweet = stock_data[-1], stock_data[0]
        correlation_results = analyze_correlation(sentiment, stock_30_m_after_tweet["last"], stock_30_m_before_tweet["last"])

        logger.debug(f"Stock data 30 min before tweet: {stock_30_m_before_tweet}")
        logger.debug(f"Stock data 30 min after tweet: {stock_30_m_after_tweet}")
        logger.debug(f"Correlation results: {correlation_results}")

        output_data.append({
            "accountName": ceo["twitterAccountName"],
            "tweet": tweet['text'],
            "date": tweet['created_at'],
            "sentiment": sentiment,
            "company": ceo["company"],
            "stockPrice30MinBeforeTweet": stock_30_m_before_tweet["last"],
            "stockPrice30MinAfterTweet": stock_30_m_after_tweet["last"],
            "stockPriceChange": stock_30_m_after_tweet["last"] - stock_30_m_before_tweet["last"],
            "stockVolume30MinBeforeTweet": stock_30_m_before_tweet["volume"],
            "stockVolume30MinAfterTweet": stock_30_m_before_tweet["volume"],
            "isColerationOccurs": correlation_results
        })
    except TimeFrameError as e:
        logger.info(f"The timestamp of the specific tweet does not fall between 14:00 and 19:00. Moving on to the next tweet.")
        continue

logger.info(f"Collected {len(output_data)} tweets with stock and sentiment analysis")

export_methods = {
    "Export to csv": export_to_csv,
    "Export to xlsx": export_to_xlsx,
    "Export to json": export_to_json,
    "Print in the console": print_in_console
}

data_export_method = questionary.select(
        "What would you like to do with the collected data?",
        choices=[
            "Export to csv",
            "Export to xlsx",
            "Export to json",
            "Print in the console"
        ]).ask()

if data_export_method in export_methods:
    file_name = f"{ceo["name"].lower().replace(" ", "_")}_tweets_analysis_{int(time.time())}"
    export_methods[data_export_method](output_data, file_name)
    sys.exit(0)
else:
    logger.error("Invalid export method")
    sys.exit(1)