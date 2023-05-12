from warnings import filterwarnings
filterwarnings("ignore")
import numpy as np
import plotly.graph_objs as go
import plotly.io as pio

pio.templates.default = "plotly_dark"


class StockOutliersDetector:
    """
    A class for detecting outliers in stock data.

    Args:
    ---------
        stock_data (pandas.DataFrame): The stock data to analyze.

        z_threshold (int, optional): The number of standard deviations from the mean at which to consider a point a
            z-score outlier. Defaults to 3.

        rolling_threshold (int, optional): The number of standard deviations from the rolling mean at which to
            consider a point a rolling outlier. Defaults to 2.

        rolling_window (int, optional): The window size in days for calculating the rolling mean and standard deviation.
            Defaults to 30.

    Attributes:
    ---------
        stock_data (pandas.DataFrame): The stock data to analyze.

        z_threshold (int): The number of standard deviations from the mean at which to consider a point a z-score outlier.

        rolling_threshold (int): The number of standard deviations from the rolling mean at which to consider a point
            a rolling outlier.

        rolling_window (int): The window size in days for calculating the rolling mean and standard deviation.

    Methods:
    ---------
        _calculate_z_scores(self) -> pandas.Series:
            Calculates the z-scores for the closing prices.

        _calculate_rolling_mean_and_std(self) -> Tuple[pandas.Series, pandas.Series]:
            Calculates the rolling mean and standard deviation for the closing prices.

        detect_outliers(self) -> Tuple[np.ndarray, np.ndarray]:
            Detects z-score outliers and rolling outliers in the closing prices.

        get_outliers_traces(self) -> List[plotly.graph_objects.Scatter]:
            Returns a list of Scatter traces for the closing prices and detected outliers.

        fig(self) -> plotly.graph_objects.Figure:
            Returns a Figure object containing the closing prices and detected outliers.

    Usage:
    ---------
        # Create a StockOutliersDetector object
        >>> detector = StockOutliersDetector(stock_data)

        # Detect outliers
        >>> zscore_outliers_mask, rolling_outliers_mask = detector.detect_outliers()

        # Get scatter traces for closing prices and detected outliers
        >>> traces = detector.get_outliers_traces()

        # Create a plotly figure
        >>> fig = detector.fig()
    """

    def __init__(
        self, stock_data, z_threshold=3, rolling_threshold=2, rolling_window=30
    ) -> None:
        self.stock_data = stock_data
        self.z_threshold: int = z_threshold
        self.rolling_threshold: int = rolling_threshold
        self.rolling_window = rolling_window

    def _calculate_z_scores(self):
        closing_prices = self.stock_data["Close"]
        return (closing_prices - np.mean(closing_prices)) / np.std(closing_prices)

    def _calculate_rolling_mean_and_std(self):
        closing_prices = self.stock_data["Close"]
        return (
            closing_prices.rolling(window=self.rolling_window).mean(),
            closing_prices.rolling(window=self.rolling_window).std(),
        )

    def detect_outliers(self):
        closing_prices = self.stock_data["Close"]
        z_scores = self._calculate_z_scores()
        rolling_mean, rolling_std = self._calculate_rolling_mean_and_std()

        zscore_outliers_mask = z_scores > self.z_threshold
        rolling_outliers_mask = (
            closing_prices - rolling_mean
        ) > self.rolling_threshold * rolling_std

        return zscore_outliers_mask, rolling_outliers_mask

    def get_outliers_traces(self):
        zscore_outliers_mask, rolling_outliers_mask = self.detect_outliers()
        closing_prices = self.stock_data["Close"]

        zscore_trace = go.Scatter(
            x=closing_prices.index,
            y=closing_prices.where(zscore_outliers_mask, np.nan),
            mode="markers",
            name="Z-score Outliers",
            marker=dict(
                symbol="triangle-down",
                color="red",
                size=10,
                line=dict(width=1, color="black"),
            ),
            showlegend=True,
            legendgroup="Close and Outliers",
            legendgrouptitle_text="Close and Outliers",
        )

        rolling_trace = go.Scatter(
            x=closing_prices.index,
            y=closing_prices.where(rolling_outliers_mask, np.nan),
            mode="markers",
            name="Rolling Outliers",
            marker=dict(
                symbol="triangle-down",
                color="green",
                size=10,
                line=dict(width=1, color="black"),
            ),
            showlegend=True,
            legendgroup="Close and Outliers",
            legendgrouptitle_text="Close and Outliers",
        )

        close_trace = go.Scatter(
            x=closing_prices.index,
            y=closing_prices,
            mode="lines",
            name="Close Price",
            line=dict(color="blue"),
            showlegend=True,
            legendgroup="Close and Outliers",
            legendgrouptitle_text="Close and Outliers",
        )

        return [close_trace, zscore_trace, rolling_trace]

    def fig(self) -> go.Figure:
        fig = go.Figure()

        for trace in self.get_outliers_traces():
            fig.add_trace(trace)

        fig.update_layout(
            title="Stock Price with Outliers Detected",
            xaxis_title="Date",
            yaxis_title="Closing Price",
        )
        closing_prices = self.stock_data["Close"]
        min_date = closing_prices.index.min()
        max_date = closing_prices.index.max()
        fig.update_xaxes(range=[min_date, max_date])

        return fig
