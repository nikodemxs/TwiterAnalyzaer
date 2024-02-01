import requests
from typing import List
from abc import ABC, abstractmethod
from src.interfaces.main import Stock
from src.constants.main import STOCK_API_URL

class AbstractStockAPI(ABC):
    @abstractmethod
    def fetch_stock_data(self, symbol):
        pass

class StockAPI(AbstractStockAPI):
    def __init__(self, api_key):
        self.base_url = STOCK_API_URL
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
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            return response.json()["data"]
        except requests.exceptions.RequestException as e:
            print(f"Error fetching stock data for {symbol} from Stock API: {str(e)}")
            return None
