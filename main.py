# import tweepy
import json
from abc import ABC, abstractmethod
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class AbstractTwitterApiStrategy(ABC):
    @abstractmethod
    def fetchUserTweets(self, username, count):
        pass

# Concrete implementation for Twitter API
# class TwitterApi(AbstractTwitterApiStrategy):
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

class TwitterMockApi(AbstractTwitterApiStrategy):
    def __init__(self):
        self.user_tweets_mock_filepath = 'mocks/twitter_user_tweets_response_mock.json'
    
    def _load_mock_data(self):
        try:
            with open(self.user_tweets_mock_filepath, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Mock data file {self.user_tweets_mock_filepath} not found.")
            return None
        except json.JSONDecodeError:
            print(f"Error decoding JSON from file {self.user_tweets_mock_filepath}.")
            return None

    def fetchUserTweets(self, username, count=10):
        mock_data = self._load_mock_data()
        return [tweet for tweet in mock_data["includes"]["tweets"]]

# Adapter class to switch between strategies
class TwitterApiAdapter:
    def __init__(self, api_strategy):
        self.api_strategy = api_strategy

    def fetchUserTweets(self, username, count=10):
        return self.api_strategy.fetchUserTweets(username, count)

def determine_sentiment(scores):
    if scores['compound'] >= 0.05:
        return "positive"
    elif scores['compound'] <= -0.05:
        return "negative"
    else:
        return "neutral"

# api_key = 'YOUR_API_KEY'
# api_secret_key = 'YOUR_API_SECRET_KEY'
# access_token = 'YOUR_ACCESS_TOKEN'
# access_token_secret = 'YOUR_ACCESS_TOKEN_SECRET'

api_strategy = TwitterMockApi()
twitter_api = TwitterApiAdapter(api_strategy)
tweets_from_mock = twitter_api.fetchUserTweets('twitterusername', count=5)
print("Tweet from Mock API:", tweets_from_mock, '\n')

analyzer = SentimentIntensityAnalyzer()
scores = analyzer.polarity_scores(tweets_from_mock[0]['text'])
sentiment = determine_sentiment(scores)
print("Sentiment analyzer output: ", sentiment)
print("Sentiment scores output: ", scores)