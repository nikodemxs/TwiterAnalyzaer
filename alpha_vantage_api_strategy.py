import requests
from abc import ABC, abstractmethod

class AbstractAlphaVantageAPI(ABC):
    @abstractmethod
    def fetch_stock_data(self, symbol):
        pass

class AlphaVantageAPI(AbstractAlphaVantageAPI):
    def __init__(self, api_key):
        self.base_url = "https://www.alphavantage.co/query"
        self.api_key = api_key

    def fetch_stock_data(self, symbol):
        params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": symbol,
            "apikey": self.api_key
        }
        response = requests.get(self.base_url, params=params)
        response.raise_for_status()
        return response.json()
