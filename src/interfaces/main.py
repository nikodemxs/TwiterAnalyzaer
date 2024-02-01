from typing import TypedDict

class CEO(TypedDict):
    name: str
    company: str
    twitterAccountName: str
    marketSymbol: str

class Tweet(TypedDict):
    text: str
    created_at: str
    id: str

class Stock(TypedDict):
    open: int
    high: int
    low: int
    last: int
    close: int | None
    volume: int | None
    date: str
    symbol: str
    exchange: str