# import tweepy
import json
from abc import ABC, abstractmethod
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class ApiStrategy(ABC):
    @abstractmethod
    def fetchUserTweets(self, username, count):
        pass

# Concrete implementation for Twitter API
# class TwitterApiStrategy(ApiStrategy):
    # def __init__(self, api_key, api_secret_key, access_token, access_token_secret):
        # auth = tweepy.OAuthHandler(api_key, api_secret_key)
        # auth.set_access_token(access_token, access_token_secret)
        # self.api = tweepy.API(auth)

    # def fetchUserTweets(self, username, count=10):
    #     try:
    #         user_tweets = self.api.user_timeline(screen_name=username, count=count)
    #         return [tweet.text for tweet in user_tweets]
    #     except tweepy.TweepError as e:
    #         print(f"Error fetching tweets for {username} from Twitter API: {str(e)}")
    #         return None

class MockApiStrategy(ApiStrategy):
    def _load_mock_data(self):
        try:
            with open('twitter_mocked.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Mock data file twitter_mocked.json not found.")
            return None
        except json.JSONDecodeError:
            print(f"Error decoding JSON from file twitter_mocked.json.")
            return None

    def fetchUserTweets(self, username, count=10):
        mock_data = self._load_mock_data()
        return [tweet for tweet in mock_data["includes"]["tweets"]]

# Adapter class to switch between strategies
class ApiAdapter:
    def __init__(self, api_strategy):
        self.api_strategy = api_strategy

    def fetchUserTweets(self, username, count=10):
        return self.api_strategy.fetchUserTweets(username, count)


# api_key = 'YOUR_API_KEY'
# api_secret_key = 'YOUR_API_SECRET_KEY'
# access_token = 'YOUR_ACCESS_TOKEN'
# access_token_secret = 'YOUR_ACCESS_TOKEN_SECRET'
analyzer = SentimentIntensityAnalyzer()
mock_api_strategy = MockApiStrategy()
api_adapter = ApiAdapter(mock_api_strategy)
tweets_from_mock = api_adapter.fetchUserTweets('twitterusername', count=5)
# print("Tweets from Mock API:", tweets_from_mock)
scores = analyzer.polarity_scores(tweets_from_mock[0]['text'])

if scores['compound'] >= 0.05:
    sentiment = "positive"
elif scores['compound'] <= -0.05:
    sentiment = "negative"
else:
    sentiment = "neutral"

print(sentiment, scores)