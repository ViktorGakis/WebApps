from warnings import filterwarnings

from torch import Value

filterwarnings("ignore")

from typing import Any

import plotly.io as pio
import yfinance as yf
from pandas import DataFrame
from pandas.core.frame import DataFrame
from yfinance.ticker import Ticker

pio.templates.default = "plotly_dark"


class Stock:
    """
    A class for retrieving historical stock data from Yahoo Finance using the yfinance library.

    Args:
    ----------
        symbol (str): The stock symbol to retrieve data for.

        start_date (str, optional): The start date of the date range to retrieve data for, in YYYY-MM-DD format. If not specified, defaults to the earliest available date for the given stock.

        end_date (str, optional): The end date of the date range to retrieve data for, in YYYY-MM-DD format. If not specified, defaults to the current date.

        interval (str, optional): The time interval between data points. Valid values are '1d' (daily), '1wk' (weekly), '1mo' (monthly), '1m' (1-minute), '2m' (2-minute), '5m' (5-minute), '15m' (15-minute), '30m' (30-minute), '60m' (60-minute), '90m' (90-minute), and '1h' (hourly). Default is '1d' for daily data.

    Attributes:
    ----------
        symbol (str): The stock symbol being retrieved.

        start_date (str): The actual start date of the retrieved data, in YYYY-MM-DD format.

        end_date (str): The actual end date of the retrieved data, in YYYY-MM-DD format.

        interval (str): The time interval between data points.

        data (pandas.DataFrame): A DataFrame containing the retrieved stock data.

        ticker (yfinance.ticker.Ticker): A Ticker object for the given stock symbol.

        info (dict): A dictionary containing information about the stock, such as its name and industry.

    Methods:
    ----------
        startup(symbol: str, start_date: str, end_date: str, interval: str) -> None:
            Constructs a new StockData object and downloads the stock data from Yahoo Finance.

    Usage:
    ----------
        # Instantiate a Stock object
        >>> stock = Stock(symbol="AAPL", start_date="2020-01-01", end_date="2022-04-17", interval="1d")

        # Access stock data
        >>> stock.data

        # Access stock information
        >>> stock.info
    """

    def __init__(self, symbol, start_date=None, end_date=None, interval="1d") -> None:
        self.startup(symbol, start_date, end_date, interval)

    def startup(self, symbol, start_date, end_date, interval) -> None:
        """
        Constructs a new StockData object and downloads the stock data from Yahoo Finance.

        Args:
            symbol (str): The stock symbol to retrieve data for.

            start_date (str): The start date of the date range to retrieve data for, in YYYY-MM-DD format.

            end_date (str): The end date of the date range to retrieve data for, in YYYY-MM-DD format.

            interval (str, optional): The time interval between data points. Default is '1d' for daily data. Valid values are '1d' (daily), '1wk' (weekly), '1mo' (monthly), '1m' (1-minute), '2m' (2-minute), '5m' (5-minute), '15m' (15-minute), '30m' (30-minute), '60m' (60-minute), '90m' (90-minute), and '1h' (hourly).
        """
        self.symbol: str = symbol
        self.start_date: str = start_date
        self.end_date: str = end_date
        self.interval: str = interval
        self.data: DataFrame = yf.download(
            symbol, start=start_date, end=end_date, interval=interval
        )
        if isinstance(self.data, DataFrame) and self.data.shape[0]>0:
            if self.start_date is None and self.end_date is None:
                self.start_date = str(self.data.iloc[0].name)
                self.end_date = str(self.data.iloc[-1].name)
            self.ticker: Ticker = yf.Ticker(symbol)
            self.info: dict[Any, Any] = self.ticker.info

    def __repr__(self) -> str:
        """
        Returns a string representation of the StockData object.
        """
        return f"StockData(symbol={self.symbol}, start_date={self.start_date}, end_date={self.end_date}, interval={self.interval})"

    def __str__(self) -> str:
        """
        Returns a string representation of the stock data.
        """
        return str(self.data)
