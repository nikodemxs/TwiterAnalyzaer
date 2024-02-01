import json
import tweepy
from abc import ABC, abstractmethod

class AbstractTwitterApiStrategy(ABC):
    @abstractmethod
    def fetch_user_tweets(self, username, count):
        pass

class TwitterMockApi(AbstractTwitterApiStrategy):
    def __init__(self, user_tweets_mock_filepath='mocks/twitter_user_tweets_response_mock.json'):
        self.user_tweets_mock_filepath = user_tweets_mock_filepath
    
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

    def fetch_user_tweets(self, username, count=10):
        mock_data = self._load_mock_data()
        return [tweet for tweet in mock_data.get("includes", {}).get("tweets", [])][:count]

class TwitterApi(AbstractTwitterApiStrategy):
    def __init__(self, api_key, api_secret_key, access_token, access_token_secret):
        auth = tweepy.OAuthHandler(api_key, api_secret_key)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)

    def fetchUserTweets(self, username, count=10):
        try:
            user_tweets = self.api.user_timeline(screen_name=username, count=count)
            return [tweet.text for tweet in user_tweets]
        except tweepy.TweepError as e:
            print(f"Error fetching tweets for {username} from Twitter API: {str(e)}")
            return None