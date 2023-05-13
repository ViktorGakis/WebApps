from warnings import filterwarnings

filterwarnings("ignore")


import numpy as np
import plotly.graph_objs as go
import plotly.io as pio
from plotly.subplots import make_subplots

pio.templates.default = "plotly_dark"


class StockMetrics:
    """
    A class to represent financial metrics of a stock and visualize them using Plotly.

    Attributes:
    -----------
    symbol : str
        The stock symbol.
    info : dict
        A dictionary containing the stock's financial information.

    Methods:
    --------
    startup()
        Initializes the financial attributes for the stock.

    create_indicators()
        Creates a list of Plotly Indicator traces for the financial attributes.

        Returns:
        List[go.Indicator]
            A list of Plotly Indicator traces representing the financial metrics.

    create_subplot()
        Creates a Plotly Subplot using the financial attributes.

        Returns:
        go.Figure
            A Plotly Figure containing the subplot with the financial metrics.

    Usage:
    ------
    To use this class, create an instance with the stock symbol and a dictionary of the stock's financial information.
    Then call the `create_subplot()` method to get a Plotly figure with the financial metrics represented as Indicator traces.

    Example:
    --------
    >>> import plotly.graph_objs as go
    >>> from plotly.subplots import make_subplots
    >>> import numpy as np
    >>>
    >>> symbol = "AAPL"
    >>> info = {"trailingEps": 3.28, "trailingPE": 34.26, "totalRevenue": 365.7, "dividendYield": 0.0065, "payoutRatio": 0.175, "priceToSalesTrailing12Months": 7.08, "priceToBook": 31.16, "debtToEquity": 204.64, "returnOnEquity": 0.9345, "grossMargins": 0.42, "currentRatio": 1.15, "returnOnAssets": 0.2037}
    >>>
    >>> stock_metrics = StockMetrics(symbol, info)
    >>> fig = stock_metrics.create_subplot()
    >>> fig.show()
    """

    def __init__(self, symbol, info) -> None:
        self.symbol = symbol
        self.info = info
        self.startup()

    def startup(self) -> None:
        """
        Initializes the financial attributes for the stock.
        """
        self.eps = self.info.get("trailingEps", np.nan)
        self.pe_ratio = self.info.get("trailingPE", np.nan)
        self.revenue = self.info.get("totalRevenue", np.nan)
        self.dividend_yield = self.info.get("dividendYield", np.nan)
        self.payout_ratio = self.info.get("payoutRatio", np.nan)
        self.price_to_sales = self.info.get("priceToSalesTrailing12Months", np.nan)
        self.price_to_book = self.info.get("priceToBook", np.nan)
        self.debt_to_equity = self.info.get("debtToEquity", np.nan)
        self.return_on_equity = self.info.get("returnOnEquity", np.nan)
        self.gross_margin = self.info.get("grossMargins", np.nan)
        self.current_ratio = self.info.get("currentRatio", np.nan)
        self.return_on_assets = self.info.get("returnOnAssets", np.nan)

    def create_indicators(self):
        """
        Creates a list of Plotly Indicator traces for the financial attributes.

        Returns:
        --------
        List[go.Indicator]
            A list of Plotly Indicator traces.
        """
        indicators = []
        title_size = 22
        number_size = 20
        warehouse = [
            ("EPS", self.eps, "$", None),
            ("P/E Ratio", self.pe_ratio, None, None),
            ("Revenue", self.revenue, "$", None),
            ("Dividend Yield", self.dividend_yield * 100, None, "%"),
            ("Payout Ratio", self.payout_ratio * 100, None, "%"),
            ("P/S Ratio", self.price_to_sales, None, None),
            ("P/B Ratio", self.price_to_book, None, None),
            ("Debt-to-Equity", self.debt_to_equity, None, None),
            ("Return on Equity", self.return_on_equity * 100, None, "%"),
            ("Gross Margin", self.gross_margin * 100, None, "%"),
            ("Current Ratio", self.current_ratio, None, None),
            ("Return on Assets", self.return_on_assets * 100, None, "%"),
        ]
        for title, val, prefix, suffix in warehouse:
            number: dict[str, dict[str, int]] = {"font": {"size": number_size}}
            if suffix is not None:
                number |= {"suffix": suffix}
            if prefix is not None:
                number |= {"prefix": prefix}
            indicators.append(
                go.Indicator(
                    mode="number",
                    value=val,
                    number=number,
                    title={"text": title, "font": {"size": title_size}},
                )
            )

        return indicators

    def create_subplot(self) -> go.Figure:
        """
        Creates a Plotly Subplot using the financial attributes.

        Returns:
        --------
        go.Figure
            A Plotly Figure containing the subplot.
        """
        fig = make_subplots(
            rows=2,
            cols=6,
            specs=[
                [
                    {"type": "indicator"},
                    {"type": "indicator"},
                    {"type": "indicator"},
                    {"type": "indicator"},
                    {"type": "indicator"},
                    {"type": "indicator"},
                ],
                [
                    {"type": "indicator"},
                    {"type": "indicator"},
                    {"type": "indicator"},
                    {"type": "indicator"},
                    {"type": "indicator"},
                    {"type": "indicator"},
                ],
            ],
        )

        indicators = self.create_indicators()

        for i, indicator in enumerate(indicators):
            row: int = i // 6 + 1
            col: int = i % 6 + 1
            fig.add_trace(indicator, row=row, col=col)

        fig.update_layout(
            title=f"Fundamentals of ticker: {self.symbol}", margin=dict(t=100)
        )

        return fig
