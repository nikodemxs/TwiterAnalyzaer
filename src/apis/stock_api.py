import requests
from typing import List
from abc import ABC, abstractmethod
from src.utils.logger import Logger
from src.interfaces.main import Stock

class AbstractStockAPI(ABC):
    @abstractmethod
    def fetch_stock_data(self, symbol):
        pass

class StockAPI(AbstractStockAPI):
    def __init__(self, api_key):
        self.logger = Logger("Stock API Service")
        self.base_url = "http://api.marketstack.com/v1/intraday"
        self.api_key = api_key

    def fetch_stock_data(self, symbol, date_from, date_to) -> List[Stock] | None:
        try:
            params = {
                "interval": "30min",
                "symbols": symbol,
                "access_key": self.api_key,
                "date_from": date_from,
                "date_to": date_to,
            }
            self.logger.debug(f"Making request to {self.base_url} with params: {params}")
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            return response.json()["data"]
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error fetching stock data for {symbol} from Stock API: {str(e)}")
            return None
