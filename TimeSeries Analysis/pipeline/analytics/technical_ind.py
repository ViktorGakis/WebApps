from warnings import filterwarnings

filterwarnings("ignore")


import plotly.graph_objs as go
import plotly.io as pio
import ta
from pandas import DataFrame, Series
from pandas.core.frame import DataFrame

pio.templates.default = "plotly_dark"


class TechnicalIndicators:
    """
    A class that calculates various technical indicators for a given stock price dataset.

    Args:
    -----------
        data (pandas.DataFrame): The stock price dataset to calculate technical indicators for.
        symbol (str): The stock symbol to retrieve data for.
        sma_window (int, optional): The window size for the simple moving average. Default is 20.
        ema_window (int, optional): The window size for the exponential moving average. Default is 20.
        rsi_window (int, optional): The window size for the Relative Strength Index. Default is 14.
        adx_window (int, optional): The window size for the Average Directional Index. Default is 14.
        bb_window (int, optional): The window size for the Bollinger Bands. Default is 20.
        bb_std (float, optional): The number of standard deviations to use for the Bollinger Bands. Default is 2.

    Attributes:
    -------------
        data (pandas.DataFrame): The stock price dataset to calculate technical indicators for.
        symbol (str): The stock symbol to retrieve data for.
        sma_window (int): The window size for the simple moving average.
        ema_window (int): The window size for the exponential moving average.
        rsi_window (int): The window size for the Relative Strength Index.
        adx_window (int): The window size for the Average Directional Index.
        bb_window (int): The window size for the Bollinger Bands.
        bb_std (float): The number of standard deviations to use for the Bollinger Bands.

    Methods:
    -----------
        calculate_sma() -> pandas.Series:
            Calculates the simple moving average and adds it to the dataset.
            Returns:
                pandas.Series: The simple moving average.

        calculate_ema() -> pandas.Series:
            Calculates the exponential moving average and adds it to the dataset.
            Returns:
                pandas.Series: The exponential moving average.

        calculate_macd() -> pandas.DataFrame:
            Calculates the Moving Average Convergence Divergence (MACD) and adds it to the dataset.
            Returns:
                pandas.DataFrame: A dataframe with the MACD, signal line, and histogram.

        calculate_rsi() -> pandas.Series:
            Calculates the Relative Strength Index (RSI) and adds it to the dataset.
            Returns:
                pandas.Series: The RSI.

        calculate_adx() -> pandas.Series:
            Calculates the Average Directional Index (ADX) and adds it to the dataset.
            Returns:
                pandas.Series: The ADX.

        calculate_obv() -> pandas.Series:
            Calculates the On-Balance Volume (OBV) and adds it to the dataset.
            Returns:
                pandas.Series: The OBV.

        calculate_bollinger_bands(window=20, k=2) -> pandas.DataFrame:
            Calculates the Bollinger Bands and adds them to the dataset.
            Args:
                window (int, optional): The window size for the moving average. Default is 20.
                k (float, optional): The number of standard deviations to use for the upper and lower bands.
                    Default is 2.
            Returns:
                pandas.DataFrame: The complete dataset with the Bollinger Bands appended to it.

        calculate_all(sma_window=None, ema_window=None, rsi_window=None, adx_window=None, bb_window=None, bb_std=None) -> pandas.DataFrame:
            Calculates all technical indicators and adds them to the dataset.
            Args:
                sma_window (int, optional): The window size for the simple moving average. Default is the value specified in the constructor.
                ema_window (int, optional): The window size for the exponential moving average. Default is the value specified in the constructor.
                rsi_window (int, optional): The window size for the Relative Strength Index. Default is the value specified in the constructor.
                adx_window (int, optional): The window size for the Average Directional Index. Default is the value specified in the constructor.
                bb_window (int, optional): The window size for the Bollinger Bands. Default is the value specified in the constructor.
                bb_std (float, optional): The number of standard deviations to use for the Bollinger Bands. Default is the value specified in the constructor.
            Returns:
                pandas.DataFrame: The complete dataset with the technical indicators appended to it.

    """

    def __init__(
        self,
        data: DataFrame,
        symbol: str,
        sma_window=20,
        ema_window=20,
        rsi_window=14,
        adx_window=14,
        bb_window=20,
        bb_std=2,
    ) -> None:
        """
        Constructs a new TechnicalIndicators object.

        Args:
            data (pandas.DataFrame): The stock price dataset to calculate technical indicators for.
            sma_window (int, optional): The window size for the simple moving average. Default is 20.
            ema_window (int, optional): The window size for the exponential moving average. Default is 20.
            rsi_window (int, optional): The window size for the Relative Strength Index. Default is 14.
            adx_window (int, optional): The window size for the Average Directional Index. Default is 14.
            bb_window (int, optional): The window size for the Bollinger Bands. Default is 20.
            bb_std (float, optional): The number of standard deviations to use for the Bollinger Bands. Default is 2.
        """
        self.data: DataFrame = data.copy()
        self.symbol: str = symbol
        self.sma_window: int = sma_window
        self.ema_window: int = ema_window
        self.rsi_window: int = rsi_window
        self.adx_window: int = adx_window
        self.bb_window: int = bb_window
        self.bb_std: int = bb_std

    def calculate_sma(self) -> Series:
        """
        Calculates the simple moving average and adds it to the dataset.

        Returns:
            pandas.Series: The simple moving average.
        """
        sma: Series = ta.trend.sma_indicator(self.data["Close"], window=self.sma_window)
        self.data["SMA"] = sma
        return sma

    def calculate_ema(self) -> Series:
        """
        Calculates the exponential moving average and adds it to the dataset.

        Returns:
            pandas.Series: The exponential moving average.
        """
        ema: Series = ta.trend.ema_indicator(self.data["Close"], window=self.ema_window)
        self.data["EMA"] = ema
        return ema

    def calculate_macd(self) -> Series:
        """
        Calculates the Moving Average Convergence Divergence (MACD) and adds it to the dataset.

        Returns:
            pandas.DataFrame: A dataframe with the MACD, signal line, and histogram.
        """
        macd, signal, hist = (
            ta.trend.macd(self.data["Close"]),
            ta.trend.macd_signal(self.data["Close"]),
            ta.trend.macd_diff(self.data["Close"]),
        )
        self.data["MACD"] = macd
        self.data["Signal"] = signal
        self.data["Histogram"] = hist
        return self.data[["MACD", "Signal", "Histogram"]]

    def calculate_rsi(self) -> Series:
        """
        Calculates the Relative Strength Index (RSI) and adds it to the dataset.

        Returns:
            pandas.Series: The RSI.
        """
        rsi: Series = ta.momentum.rsi(self.data["Close"], window=self.rsi_window)
        self.data["RSI"] = rsi
        return rsi

    def calculate_adx(self) -> Series:
        """
        Calculates the Average Directional Index (ADX) and adds it to the dataset.

        Returns:
            pandas.Series: The ADX.
        """
        adx: Series = ta.trend.adx(
            self.data["High"],
            self.data["Low"],
            self.data["Close"],
            window=self.adx_window,
            fillna=True,
        )
        self.data["ADX"] = adx
        return adx

    def calculate_obv(self) -> Series:
        """
        Calculates the On-Balance Volume (OBV) and adds it to the dataset.

        Returns:
            pandas.Series: The OBV.
        """
        obv: Series = ta.volume.on_balance_volume(
            self.data["Close"], self.data["Volume"]
        )
        self.data["OBV"] = obv
        return obv

    def calculate_bollinger_bands(self, window=20, k=2) -> DataFrame:
        """
        Calculates the Bollinger Bands and adds them to the dataset.

        Args:
            window (int, optional): The window size for the moving average. Default is 20.
            k (float, optional): The number of standard deviations to use for the upper and lower bands.
                Default is 2.

        Returns:
            pandas.DataFrame: The complete dataset with the Bollinger Bands appended to it.
        """
        ma: Series = ta.trend.sma_indicator(self.data["Close"], window=window)
        std: Series = ta.volatility.bollinger_mavg(
            self.data["Close"], window=window, fillna=True
        )
        upper_band: Series = ma + k * std
        lower_band: Series = ma - k * std
        band_width: Series = (upper_band - self.data["Close"]) / self.data["Close"]

        self.data["Upper Band"] = upper_band
        self.data["Lower Band"] = lower_band
        self.data["Band Width"] = band_width

        return self.data

    def calculate_all(
        self,
        sma_window=None,
        ema_window=None,
        rsi_window=None,
        adx_window=None,
        bb_window=None,
        bb_std=None,
    ) -> DataFrame:
        """
        Calculates all technical indicators and adds them to the dataset.

        Args:
            sma_window (int, optional): The window size for the simple moving average. Default is the value specified in the constructor.
            ema_window (int, optional): The window size for the exponential moving average. Default is the value specified in the constructor.
            rsi_window (int, optional): The window size for the Relative Strength Index. Default is the value specified in the constructor.
            adx_window (int, optional): The window size for the Average Directional Index. Default is the value specified in the constructor.
            bb_window (int, optional): The window size for the Bollinger Bands. Default is the value specified in the constructor.
            bb_std (float, optional): The number of standard deviations to use for the Bollinger Bands. Default is the value specified in the constructor.

        Returns:
            pandas.DataFrame: The complete dataset with the technical indicators appended to it.
        """
        if sma_window is not None:
            self.sma_window = sma_window
        if ema_window is not None:
            self.ema_window = ema_window
        if rsi_window is not None:
            self.rsi_window = rsi_window
        if adx_window is not None:
            self.adx_window = adx_window
        if bb_window is not None:
            self.bb_window = bb_window
        if bb_std is not None:
            self.bb_std = bb_std

        self.calculate_sma()
        self.calculate_ema()
        self.calculate_macd()
        self.calculate_rsi()
        self.calculate_adx()
        self.calculate_obv()
        self.calculate_bollinger_bands()

        return self.data


class MACDSubplot:
    """
    A class that generates a MACD subplot using Plotly.

    Args:
    -----------
        df (pandas.DataFrame): The stock price dataset with MACD data.

    Attributes:
    -----------
        data (pandas.DataFrame): The stock price dataset with MACD data.

    Methods:
    -----------
        generate_macd(): Generates a MACD line chart.
        generate_macd_signal(): Generates a MACD signal line chart.
        generate_macd_histogram(): Generates a MACD histogram bar chart.
        fig(): Combines all the MACD charts into a single subplot.
    """

    def __init__(self, df: DataFrame) -> None:
        """
        Constructs a new MACDSubplot object.

        Args:
            df (pandas.DataFrame): The stock price dataset with MACD data.
        """
        self.data: DataFrame = df

    def generate_macd(self) -> go.Scatter:
        """
        Generates a MACD line chart.

        Returns:
            plotly.graph_objs.Scatter: The MACD chart.
        """
        return go.Scatter(
            x=self.data.index,
            y=self.data["MACD"],
            mode="lines",
            name="MACD",
            legendgroup="MACD",
            legendgrouptitle_text="MACD",
        )

    def generate_macd_signal(self) -> go.Scatter:
        """
        Generates a MACD signal line chart.

        Returns:
            plotly.graph_objs.Scatter: The MACD signal line chart.
        """
        return go.Scatter(
            x=self.data.index,
            y=self.data["Signal"],
            mode="lines",
            name="Signal",
            legendgroup="MACD",
            legendgrouptitle_text="MACD",
        )

    def generate_macd_histogram(self) -> go.Bar:
        """
        Generates a MACD histogram bar chart.

        Returns:
            plotly.graph_objs.Bar: The MACD histogram chart.
        """
        return go.Bar(
            x=self.data.index,
            y=self.data["Histogram"],
            name="Histogram",
            legendgroup="MACD",
            legendgrouptitle_text="MACD",
        )

    def fig(self) -> tuple[go.Scatter, go.Scatter, go.Bar]:
        """
        Combines all the MACD charts into a single subplot.

        Returns:
            tuple: A tuple of MACD line chart, MACD signal line chart, and MACD histogram bar chart.
        """
        return (
            self.generate_macd(),
            self.generate_macd_signal(),
            self.generate_macd_histogram(),
        )


# %%
class RSI_ADXSubplot:
    """
    A class for generating a subplot of Relative Strength Index (RSI) and
    Average Directional Index (ADX) technical indicators for a given stock price dataset.

    Args:
    -----------
        df (pandas.DataFrame): The stock price dataset with RSI and ADX data.

    Attributes:
    -----------
        data (pandas.DataFrame): The stock price dataset with RSI and ADX data.

    Methods:
    -----------
        generate_rsi_chart() -> plotly.graph_objs.Scatter:
            Generates a Relative Strength Index (RSI) line chart.

        generate_rsi_30_line() -> plotly.graph_objs.Scatter:
            Generates a dashed line representing the RSI threshold of 30.

        generate_rsi_70_line() -> plotly.graph_objs.Scatter:
            Generates a dashed line representing the RSI threshold of 70.

        generate_adx_chart() -> plotly.graph_objs.Scatter:
            Generates an Average Directional Index (ADX) line chart.

        fig() -> Tuple[plotly.graph_objs.Scatter]:
            Plots the RSI and ADX charts.
    """

    def __init__(self, df: DataFrame) -> None:
        """
        Constructs a new RSI_ADXSubplot object.

        Args:
            df (pandas.DataFrame): The stock price dataset with RSI and ADX data.
        """
        self.data: DataFrame = df

    def generate_rsi_chart(self) -> go.Scatter:
        """
        Generates a Relative Strength Index (RSI) line chart.

        Returns:
            plotly.graph_objs.Scatter: The RSI chart.
        """
        return go.Scatter(
            x=self.data.index,
            y=self.data["RSI"],
            mode="lines",
            name=f"RSI ({self.data['RSI'].name})",
            line=dict(color="blue"),
            legendgroup="RSI and ADX",
            legendgrouptitle_text="RSI and ADX",
        )

    def generate_rsi_30_line(self) -> go.Scatter:
        """
        Generates a dashed line representing the RSI threshold of 30.

        Returns:
            plotly.graph_objs.Scatter: The RSI 30 line.
        """
        return go.Scatter(
            x=self.data.index,
            y=[30] * len(self.data.index),
            mode="lines",
            name="RSI 30",
            line=dict(color="red", dash="dash"),
            legendgroup="RSI and ADX",
            legendgrouptitle_text="RSI and ADX",
        )

    def generate_rsi_70_line(self) -> go.Scatter:
        """
        Generates a dashed line representing the RSI threshold of 70.

        Returns:
            plotly.graph_objs.Scatter: The RSI 70 line.
        """
        return go.Scatter(
            x=self.data.index,
            y=[70] * len(self.data.index),
            mode="lines",
            name="RSI 70",
            line=dict(color="green", dash="dash"),
            legendgroup="RSI and ADX",
            legendgrouptitle_text="RSI and ADX",
        )

    def generate_adx_chart(self) -> go.Scatter:
        """
        Generates an Average Directional Index (ADX) line chart.

        Returns:
            plotly.graph_objs.Scatter: The ADX chart.
        """
        return go.Scatter(
            x=self.data.index,
            y=self.data["ADX"],
            mode="lines",
            name=f"ADX ({self.data['ADX'].name})",
            legendgroup="RSI and ADX",
            legendgrouptitle_text="RSI and ADX",
        )

    def fig(self) -> tuple[go.Scatter, go.Scatter, go.Scatter, go.Scatter]:
        """
        Plots the RSI and ADX charts.

        Returns:
            tuple[plotly.graph_objs.Scatter]: A tuple of the RSI chart, RSI 30 line, RSI 70 line, and ADX chart.
        """
        return (
            self.generate_rsi_chart(),
            self.generate_rsi_30_line(),
            self.generate_rsi_70_line(),
            self.generate_adx_chart(),
        )


# %%
class BBANDSSubplot:
    """
    A class used to represent a subplot containing Bollinger Bands data for stock prices.

    Args:
    ----------
        df (pandas.DataFrame): The stock price dataset with Bollinger Bands data.

    Attributes:
    ----------
        data (pandas.DataFrame): The stock price dataset with Bollinger Bands data.

    Methods:
    ----------
        generate_upper_band() -> go.Scatter:
            Generates an upper Bollinger Band line chart.

        generate_band_width() -> go.Scatter:
            Generates a mid Bollinger Band line chart.

        generate_lower_band() -> go.Scatter:
            Generates a lower Bollinger Band line chart.

        fig() -> tuple[go.Scatter, go.Scatter, go.Scatter]:
            Returns all three Bollinger Bands charts as a tuple of Scatter objects.

    This class generates a subplot that displays Bollinger Bands data for stock prices. It takes in a `pandas.DataFrame` object that contains the stock price data and the Bollinger Bands data. Once the object is created, you can generate the subplot using the `fig()` method.

    The `generate_upper_band()` method generates the upper Bollinger Band line chart.

    The `generate_band_width()` method generates the mid Bollinger Band line chart.

    The `generate_lower_band()` method generates the lower Bollinger Band line chart.

    The `fig()` method returns all three Bollinger Bands charts as a tuple of `plotly.graph_objs.Scatter` objects.
    """

    def __init__(self, df: DataFrame) -> None:
        """
        Constructs a new BBANDSSubplot object.

        Args:
            df (pandas.DataFrame): The stock price dataset with Bollinger Bands data.
        """
        self.data: DataFrame = df

    def generate_upper_band(self) -> go.Scatter:
        """
        Generates an upper Bollinger Band line chart.

        Returns:
            plotly.graph_objs.Scatter: The upper Bollinger Band chart.
        """
        return go.Scatter(
            x=self.data.index,
            y=self.data["Upper Band"],
            mode="lines",
            name="Bollinger Bands (Upper)",
            legendgroup="Bollinger Bands",
            legendgrouptitle_text="BBANDS",
        )

    def generate_band_width(self) -> go.Scatter:
        """
        Generates a mid Bollinger Band line chart.

        Returns:
            plotly.graph_objs.Scatter: The mid Bollinger Band chart.
        """
        return go.Scatter(
            x=self.data.index,
            y=self.data["Band Width"],
            mode="lines",
            name="Bollinger Bands (Mid)",
            legendgroup="Bollinger Bands",
            legendgrouptitle_text="BBANDS",
        )

    def generate_lower_band(self) -> go.Scatter:
        """
        Generates a lower Bollinger Band line chart.

        Returns:
            plotly.graph_objs.Scatter: The lower Bollinger Band chart.
        """
        return go.Scatter(
            x=self.data.index,
            y=self.data["Lower Band"],
            mode="lines",
            name="Bollinger Bands (Lower)",
            legendgroup="Bollinger Bands",
            legendgrouptitle_text="BBANDS",
        )

    def fig(self) -> tuple[go.Scatter, go.Scatter, go.Scatter]:
        """
        Returns all the figures.

        Returns:
            tuple[plotly.graph_objs.Scatter]: A tuple of the three Bollinger Bands charts.
        """
        return (
            self.generate_upper_band(),
            self.generate_band_width(),
            self.generate_lower_band(),
        )


# %%
class CANDLESMASubplot:
    """
    A class representing a candlestick chart with two moving average lines as a subplot.

    Args:
    -----------
        df (pandas.DataFrame): The stock price dataset with candlestick and MA data.

    Attributes:
    -----------
        data (pandas.DataFrame): The stock price dataset with candlestick and MA data.

    Methods:
    -----------
        generate_candlestick(): Generates a candlestick chart.
        generate_sma(): Generates a simple moving average line chart.
        generate_ema(): Generates an exponential moving average line chart.
        fig(): Generates a subplot with a candlestick chart, simple moving average line chart, and an exponential moving average line chart.

    """

    def __init__(self, df: DataFrame) -> None:
        """
        Constructs a new CANDLESMASubplot object.

        Args:
            df (pandas.DataFrame): The stock price dataset with candlestick and MA data.
        """
        self.data: DataFrame = df

    def generate_candlestick(self) -> go.Candlestick:
        """
        Generates a candlestick chart.

        Returns:
            plotly.graph_objs.Candlestick: The candlestick chart.
        """
        return go.Candlestick(
            x=self.data.index,
            open=self.data["Open"],
            high=self.data["High"],
            low=self.data["Low"],
            close=self.data["Close"],
            name="Candlestick",
            increasing=dict(line=dict(color="#00FF00")),
            decreasing=dict(line=dict(color="#FF0000")),
            legendgroup="Candles and MA",
            legendgrouptitle_text="Candles and MA",
        )

    def generate_sma(self) -> go.Scatter:
        """
        Generates a simple moving average line chart.

        Returns:
            plotly.graph_objs.Scatter: The simple moving average chart.
        """
        return go.Scatter(
            x=self.data.index,
            y=self.data["SMA"],
            mode="lines",
            name=f"SMA ({self.data['SMA'].name})",
            legendgroup="Candles and MA",
            legendgrouptitle_text="Candles and MA",
        )

    def generate_ema(self) -> go.Scatter:
        """
        Generates an exponential moving average line chart.

        Returns:
            plotly.graph_objs.Scatter: The exponential moving average chart.
        """
        return go.Scatter(
            x=self.data.index,
            y=self.data["EMA"],
            mode="lines",
            name=f"EMA ({self.data['EMA'].name})",
            legendgroup="Candles and MA",
            legendgrouptitle_text="Candles and MA",
        )

    def fig(self) -> tuple[go.Candlestick, go.Scatter, go.Scatter]:
        """
        Generates a subplot with a candlestick chart, simple moving average line chart, and an exponential moving average line chart.

        Returns:
            tuple[plotly.graph_objs.Candlestick, plotly.graph_objs.Scatter, plotly.graph_objs.Scatter]: The candlestick chart, simple moving average line chart, and exponential moving average line chart.
        """
        return (
            self.generate_candlestick(),
            self.generate_sma(),
            self.generate_ema(),
        )


# %%
class DINDICATORSSubplot:
    """
    A class representing a subplot containing indicators for stock price statistics.

    Args:
    -----------
        df (pandas.DataFrame): The stock price dataset with DINDICATORS data.

    Attributes:
    -----------
        data (pandas.DataFrame): The stock price dataset with DINDICATORS data.

    Methods:
    -----------
        generate_current_close_price(row=1, col=1) -> plotly.graph_objs.Indicator:
            Generates a current close price indicator.
        generate_max_close_price(row=1, col=2) -> plotly.graph_objs.Indicator:
            Generates a max close price indicator.
        generate_min_close_price(row=1, col=3) -> plotly.graph_objs.Indicator:
            Generates a min close price indicator.
        generate_mean_close_price(row=1, col=4) -> plotly.graph_objs.Indicator:
            Generates a mean close price indicator.
        generate_std_close_price(row=1, col=5) -> plotly.graph_objs.Indicator:
            Generates a std close price indicator.
        fig() -> Tuple[plotly.graph_objs.Indicator]:
            Generates all DINDICATORS charts.

    """

    def __init__(self, df: DataFrame) -> None:
        """
        Constructs a new DINDICATORSSubplot object.

        Args:
            df (pandas.DataFrame): The stock price dataset with DINDICATORS data.
        """
        self.data: DataFrame = df

    def generate_current_close_price(self, row=1, col=1) -> go.Indicator:
        """
        Generates a current close price indicator.

        Returns:
            plotly.graph_objs.Indicator: The current close price indicator.
        """
        return go.Indicator(
            mode="number+delta",
            value=self.data["Close"].iloc[-1],
            delta={
                "reference": self.data["Close"].iloc[-2],
                "valueformat": ".2%",
            },
            title={"text": "Current Close Price", "font": {"size": 12}},
            number={"font": {"size": 20}},
            domain={"row": row, "column": col},
        )

    def generate_max_close_price(self, row=1, col=2) -> go.Indicator:
        """
        Generates a max close price indicator.

        Returns:
            plotly.graph_objs.Indicator: The max close price indicator.
        """
        return go.Indicator(
            mode="number",
            value=self.data["Close"].max(),
            title={"text": "Max Close Price", "font": {"size": 12}},
            number={"font": {"size": 20}},
            domain={"row": row, "column": col},
        )

    def generate_min_close_price(self, row=1, col=3) -> go.Indicator:
        """
        Generates a min close price indicator.

        Returns:
            plotly.graph_objs.Indicator: The min close price indicator.
        """
        return go.Indicator(
            mode="number",
            value=self.data["Close"].min(),
            title={"text": "Min Close Price", "font": {"size": 12}},
            number={"font": {"size": 20}},
            domain={"row": row, "column": col},
        )

    def generate_mean_close_price(self, row=1, col=4) -> go.Indicator:
        """
        Generates a mean close price indicator.

        Returns:
            plotly.graph_objs.Indicator: The mean close price indicator.
        """
        return go.Indicator(
            mode="number",
            value=self.data["Close"].mean(),
            title={"text": "Mean Close Price", "font": {"size": 12}},
            number={"font": {"size": 20}},
            domain={"row": row, "column": col},
        )

    def generate_std_close_price(self, row=1, col=5) -> go.Indicator:
        """
        Generates a std close price indicator.

        Returns:
            plotly.graph_objs.Indicator: The std close price indicator.
        """
        return go.Indicator(
            mode="number",
            value=self.data["Close"].std(),
            title={"text": "Std Close Price", "font": {"size": 12}},
            number={"font": {"size": 20}},
            domain={"row": row, "column": col},
        )

    def fig(
        self,
    ) -> tuple[go.Indicator, go.Indicator, go.Indicator, go.Indicator, go.Indicator]:
        """
        Generates all DINDICATORS charts.

        Returns:
            tuple: The current close price indicator, max close price indicator, min close price indicator, mean close
                price indicator, and std close price indicator.
        """
        return (
            self.generate_current_close_price(),
            self.generate_max_close_price(),
            self.generate_min_close_price(),
            self.generate_mean_close_price(),
            self.generate_std_close_price(),
        )
