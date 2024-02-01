import json
import tweepy
from typing import List
from abc import ABC, abstractmethod
from src.constants.main import MOCKS_DIRECTORY_PATH
from src.interfaces.main import Tweet

class AbstractTwitterApiStrategy(ABC):
    @abstractmethod
    def fetch_user_tweets(self, username, count):
        pass

class TwitterMockApi(AbstractTwitterApiStrategy):
    def _load_mock_data(self, username):
        try:
            self.user_tweets_mock_filepath = f'{MOCKS_DIRECTORY_PATH}/{username}_tweets_response_mock.json'
            with open(self.user_tweets_mock_filepath, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Mock data file {self.user_tweets_mock_filepath} not found.")
            return None
        except json.JSONDecodeError:
            print(f"Error decoding JSON from file {self.user_tweets_mock_filepath}.")
            return None

    def fetch_user_tweets(self, username: str, count=10) -> List[Tweet] | None:
        mock_data = self._load_mock_data(username)
        if not mock_data:
            return None

        return [tweet for tweet in mock_data.get("includes", {}).get("tweets", [])][:count]

class TwitterApi(AbstractTwitterApiStrategy):
    def __init__(self, api_key, api_secret_key, access_token, access_token_secret):
        auth = tweepy.OAuthHandler(api_key, api_secret_key)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)

    def fetchUserTweets(self, username, count=10) -> List[Tweet] | None:
        try:
            user_tweets = self.api.user_timeline(screen_name=username, count=count)
            return [tweet for tweet in user_tweets.get("includes", {}).get("tweets", [])][:count]
        except tweepy.HTTPException as e:
            print(f"Error fetching tweets for {username} from Twitter API: {str(e)}")
            return None