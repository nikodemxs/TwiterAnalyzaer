import os
from dotenv import load_dotenv
from twitter_api_strategy import TwitterMockApi
from alpha_vantage_api_strategy import AlphaVantageAPI
from sentiment_analysis import determine_sentiment
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

load_dotenv()

ALPHA_VANTAGE_API_KEY = "ALPHA_VANTAGE_API_KEY"

alpha_vantage_api_key = os.getenv(ALPHA_VANTAGE_API_KEY)

alpha_vantage_api = AlphaVantageAPI(alpha_vantage_api_key)

stock_data = alpha_vantage_api.fetch_stock_data("IBM")
print(stock_data)

api_strategy = TwitterMockApi()
tweets_from_mock = api_strategy.fetch_user_tweets('twitterusername', count=5)
print("Tweet from Mock API:", tweets_from_mock, '\n')

analyzer = SentimentIntensityAnalyzer()
if tweets_from_mock:
    scores = analyzer.polarity_scores(tweets_from_mock[0]['text'])
    sentiment = determine_sentiment(scores)
    print("Sentiment analyzer output: ", sentiment)
    print("Sentiment scores output: ", scores)


#  godziny otwarcia 14 - 19

#  createdAt=2023-04-28 03:27:23

#  if twitt nie stworzony w godzinach otwarcia giełdy
#    30minBefore=2023-04-27 19:00:00
#    30minAfter=2023-04-28 14:00:00

#  createdAt=2023-04-28 03:00:00
#  30minBefore=2023-04-28 02:30:00
#  30minAfter=2023-04-28 03:30:00
