from warnings import filterwarnings

filterwarnings("ignore")

import numpy as np
import plotly.graph_objs as go
import plotly.io as pio
from pandas import DataFrame
from pandas.core.frame import DataFrame
from plotly.subplots import make_subplots
from .stock_data import Stock
from .stock_metrics import StockMetrics
from .anomalies import StockOutliersDetector
from .technical_ind import (
    CANDLESMASubplot,
    DINDICATORSSubplot,
    MACDSubplot,
    RSI_ADXSubplot,
    TechnicalIndicators,
)

pio.templates.default = "plotly_dark"


class TechDashboard:
    """
    A class that generates a financial dashboard using Plotly to visualize technical analysis of stock prices.

    Attributes:
    -----------
    technicalIndicators: TechnicalIndicators
        The stock price dataset with all technical indicators calculated.

    Methods:
    --------
    generate_obv() -> go.Scatter:
        Generates an On Balance Volume (OBV) line chart.

    add_range_slider(fig) -> None:
        Adds a range slider to the bottom subplot.

    plot() -> go.Figure:
        Combines all the figures into a single subplot.

    Usage:
    ------
    To use the `TechDashboard` class, you need to provide it with a `TechnicalIndicators` object as input, which contains the stock price data and all the calculated technical indicators:

    >>> from my_package import TechnicalIndicators, TechDashboard
    >>> tech_indicators = TechnicalIndicators(symbol='AAPL', start_date='2020-01-01', end_date='2022-01-01')
    >>> dashboard = TechDashboard(tech_indicators)

    Once the object is created, you can generate the financial dashboard using the `plot()` method:

    >>> fig = dashboard.plot()

    The financial dashboard visualizes the following technical indicators for a given stock:

        - Candlestick chart with Moving Average (MA) overlay
        - Outliers and Close Price
        - MACD (Moving Average Convergence Divergence) chart
        - RSI (Relative Strength Index) and ADX (Average Directional Index) chart
        - On Balance Volume (OBV) chart

    The `generate_obv()` method generates the On Balance Volume (OBV) line chart for the stock.

    The `add_range_slider()` method adds a range slider to the bottom subplot, which allows the user to select a time period for analysis.
    """

    def __init__(self, technicalIndicators: TechnicalIndicators) -> None:
        """
        Constructs a new PlotlyDashboard object.

        Args:
            technicalIndicators (TechnicalIndicators): The stock price dataset with all technical indicators calculated.
        """
        self.data: DataFrame = technicalIndicators.calculate_all()
        self.symbol: str = technicalIndicators.symbol

    def generate_obv(self) -> go.Scatter:
        """
        Generates an On Balance Volume (OBV) line chart.

        Returns:
            plotly.graph_objs.Scatter: The OBV chart.
        """
        return go.Scatter(
            x=self.data.index,
            y=self.data["OBV"],
            mode="lines",
            name=f"OBV ({self.data['OBV'].name})",
            legendgroup="OBV",
            legendgrouptitle_text="OBV",
        )

    def add_range_slider(self, fig) -> None:
        fig.add_trace(
            go.Scatter(
                x=self.data.index,
                y=np.repeat(0, self.data.shape[0]),
                name="Data",
                line=dict(color="rgba(0,0,0,0.0)"),
                showlegend=False,
                hovertemplate="%{y}",
                hoverinfo="y",
                mode="lines",
                fill="tonexty",
                fillcolor="rgba(0,0,0,0.3)",
            ),
            row=2,
            col=1,
        )

        # Update x-axes with range slider
        fig.update_xaxes(
            rangeselector=dict(
                buttons=list(
                    [
                        dict(count=1, label="1m", step="month", stepmode="backward"),
                        dict(count=6, label="6m", step="month", stepmode="backward"),
                        dict(count=1, label="YTD", step="year", stepmode="todate"),
                        dict(count=1, label="1y", step="year", stepmode="backward"),
                        dict(step="all"),
                    ]
                ),
                bgcolor="white",
                activecolor="gray",
                font=dict(color="black"),
            ),
            type="date",
            row=2,
            col=1,
        )

        fig.update_yaxes(visible=False, row=2, col=1)
        fig.update_xaxes(rangeslider_visible=False, matches="x")

    def plot(self) -> go.Figure:
        """
        Combines all the figures into a single subplot.

        Returns:
            plotly.graph_objs.Figure: The combined subplot figure.
        """

        fig: go.Figure = make_subplots(
            rows=7,
            cols=5,
            shared_xaxes=True,
            vertical_spacing=0.07,
            row_heights=[0.05, 0.05, 0.45, 0.45, 0.2, 0.2, 0.2],
            specs=[
                [
                    {"type": "Indicator"},
                    {"type": "Indicator"},
                    {"type": "Indicator"},
                    {"type": "Indicator"},
                    {"type": "Indicator"},
                ],
                [{"colspan": 5}, {}, {}, {}, {}],
                [{"colspan": 5}, {}, {}, {}, {}],
                [{"colspan": 5}, {}, {}, {}, {}],
                [{"colspan": 5}, {}, {}, {}, {}],
                [{"colspan": 5}, {}, {}, {}, {}],
                [{"colspan": 5}, {}, {}, {}, {}],
            ],
            subplot_titles=(
                None,
                None,
                None,
                None,
                None,
                "RangeSlider",
                None,
                None,
                None,
                None,
                "Candles and MA",
                None,
                None,
                None,
                None,
                "Outliers and Close Price",
                None,
                None,
                None,
                None,
                "MACD",
                None,
                None,
                None,
                None,
                "RSI and ADX",
                None,
                None,
                None,
                None,
                "OBV",
                None,
                None,
                None,
                None,
            ),
        )

        # Add the indicators to the first row
        for idx, indicator in enumerate(DINDICATORSSubplot(self.data).fig(), start=1):
            fig.add_trace(indicator, row=1, col=idx)

        # Candles and MA
        fig.add_traces(CANDLESMASubplot(self.data).fig(), rows=3, cols=1)

        # Outliers and Close Price
        for trace in StockOutliersDetector(
            self.data, z_threshold=3, rolling_threshold=2, rolling_window=30
        ).get_outliers_traces():
            fig.add_trace(trace, row=4, col=1)

        # MACD
        fig.add_traces(MACDSubplot(self.data).fig(), rows=5, cols=1)

        # RSI and ADX
        fig.add_traces(RSI_ADXSubplot(self.data).fig(), rows=6, cols=1)

        # OBV
        fig.add_trace(self.generate_obv(), row=7, col=1)

        # Add range slider to bottom subplot
        self.add_range_slider(fig)

        # Set layout for each subplot
        fig.update_xaxes(range=[self.data.index.min(), self.data.index.max()])

        # Update legend appearance
        fig.update_layout(
            title=f"Technical Analysis of stock symbol: {self.symbol}",
            margin=dict(l=20, r=20, t=100, b=20),
            height=1000,
            legend=dict(
                groupclick="toggleitem",
                orientation="v",
                # yanchor="bottom",
                y=0,
                # xanchor="right",
                x=1,
                font=dict(size=10),
                tracegroupgap=70,
                bordercolor="Black",
                borderwidth=1,
            ),
        )

        # config={"displayModeBar": False} when plotting
        return fig

