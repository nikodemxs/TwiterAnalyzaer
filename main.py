import os
import sys
import questionary
from dotenv import load_dotenv
from src.constants.main import STOCK_API_KEY
from src.apis.twitter_api import TwitterMockApi
from src.apis.stock_api import StockAPI
from src.utils.config import load_config, get_ceo_by_config_name
from src.utils.analysis import analyze_sentiment, analyze_correlation
from src.utils.date import TimeFrameError, calculate_date_range
from src.utils.export import export_to_csv, export_to_xlsx, export_to_json, print_in_console

load_dotenv()
config = load_config()
CEOs = config["availableCEOs"]

selected_ceo_name = questionary.select(
        "Choose a CEO whose tweets you want to compare to auction data",
        choices=[ceo["name"] for ceo in CEOs]).ask()

ceo = get_ceo_by_config_name(CEOs, selected_ceo_name)

twitter_api = TwitterMockApi()
stock_api = StockAPI(os.getenv(STOCK_API_KEY))

tweets = twitter_api.fetch_user_tweets(ceo["twitterAccountName"], 2)

if tweets is None:
    print("Error: Something went wrong with fetching tweets")
    sys.exit(1)

# TODO: remove - debugging purposes only
print(f"Collected tweets: {tweets}")

data = []

for(i, tweet) in enumerate(tweets):
    try:
        sentiment = analyze_sentiment(tweet['text'])
        date_from, date_to = calculate_date_range(tweet['created_at'])

        # TODO: remove - debugging purposes only
        print(f"Sentiment: {sentiment}")
        print(f"Date from: {date_from}")
        print(f"Date to: {date_to}")

        stock_data = stock_api.fetch_stock_data(ceo["marketSymbol"], date_from, date_to)

        # TODO: remove - debugging purposes only
        print(f"Stock data: {stock_data}")

        if stock_data is [] or stock_data is None:
            continue

        stock_30_m_before_tweet, stock_30_m_after_tweet = stock_data[-1], stock_data[0]
        correlation_results = analyze_correlation(sentiment, stock_30_m_after_tweet["last"], stock_30_m_before_tweet["last"])

        # TODO: remove - debugging purposes only
        print(f"Correlation results: {correlation_results}")
        print(f"Stock 30 min before tweet: {stock_30_m_before_tweet}")
        print(f"Stock 30 min after tweet: {stock_30_m_after_tweet}")

        data.append({
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
        continue

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
    export_methods[data_export_method](data, f"{ceo["name"]}_tweets_analysis")
    sys.exit(0)
else:
    print("Invalid export method")
    sys.exit(1)