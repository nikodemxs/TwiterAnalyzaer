import json
import requests
from typing import List
from abc import ABC, abstractmethod
from src.utils.logger import Logger
from src.constants.main import MOCKS_DIRECTORY_PATH
from src.interfaces.main import Tweet, Tweeter_User

class AbstractTwitterApiStrategy(ABC):
    @abstractmethod
    def fetch_user_tweets(self, username, count):
        pass

class TwitterMockApi(AbstractTwitterApiStrategy):
    def __init__(self):
        self.logger = Logger("Twitter Mock API Service")

    def _load_mock_data(self, username):
        try:
            self.user_tweets_mock_filepath = f'{MOCKS_DIRECTORY_PATH}/{username}_tweets_response_mock.json'
            self.logger.debug(f"Loading mock data from {self.user_tweets_mock_filepath}")
            
            with open(self.user_tweets_mock_filepath, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            self.logger.error(f"Mock data file {self.user_tweets_mock_filepath} not found.")
            return None
        except json.JSONDecodeError:
            self.logger.error(f"Error decoding JSON from file {self.user_tweets_mock_filepath}.")
            return None

    def fetch_user_tweets(self, username: str, count=10) -> List[Tweet] | None:
        mock_data = self._load_mock_data(username)
        if not mock_data:
            return None
        
        self.logger.debug(f"Mock data: {mock_data}")
        return [tweet for tweet in mock_data.get("includes", {}).get("tweets", [])][:count]

class TwitterApi(AbstractTwitterApiStrategy):
    def __init__(self, bearer_token):
        self.logger = Logger("Twitter API Service")
        self.base_url = "https://api.twitter.com/2/"
        self.auth_headers = {
            'authorization': f'Bearer {bearer_token}',
        }

    def _get_request(self, endpoint, params=None):
        self.logger.debug(f"Making request to {endpoint} with params: {params}")
        return requests.get(f"{self.base_url}{endpoint}", headers=self.auth_headers, params=params)

    def _get_user_by_username(self, username) -> Tweeter_User | None:
        try: 
            user_response = self._get_request(endpoint=f"users/by/username/{username}")
            user_response_json = user_response.json()
            self.logger.debug(f"User response status code: {user_response.status_code}")
            self.logger.debug(f"User response JSON: {user_response_json}")

            if "data" in user_response_json:
                user_data: Tweeter_User = user_response_json["data"]
                return user_data
            else:
                return None
                
        except requests.exceptions.RequestException as e:
            self.logger.error(f"An error occurred while fetching user data: {e}")
            return None

    def fetch_user_tweets(self, username, count=10) -> List[Tweet] | None:
        try:
            user_data = self._get_user_by_username(username)
            if user_data is None:
                self.logger.error(f"User '{username}' not found.")
                return None

            user_id = user_data["id"]
            user_tweets_response = self._get_request(endpoint=f"users/{user_id}/tweets", params={
                "max_results": count,
                "tweet.fields": "created_at,text",
                "exclude": "retweets,replies"
            })
            user_tweets_json = user_tweets_response.json()
            self.logger.debug(f"User tweets response status code: {user_tweets_response.status_code}")
            self.logger.debug(f"User tweets response JSON: {user_tweets_json}")

            if "data" in user_tweets_json:
                user_tweets_data: List[Tweet] = user_tweets_json["data"]
                return user_tweets_data
            else:
                return None
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"An error occurred while fetching user tweets: {e}")
            return None