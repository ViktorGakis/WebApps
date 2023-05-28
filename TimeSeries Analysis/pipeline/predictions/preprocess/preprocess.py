from warnings import filterwarnings

filterwarnings("ignore")

from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.graph_objs as go
import plotly.io as pio
import seaborn as sns
import talib
from pandas import DataFrame
from pandas.core.frame import DataFrame
from plotly.offline import init_notebook_mode
from sklearn.model_selection import (
    train_test_split,
)
from sklearn.preprocessing import StandardScaler


sns.set(style="darkgrid")
plt.style.use("dark_background")
plt.rcParams.update({"grid.linewidth": 0.5, "grid.alpha": 0.5})
plt.rc("figure", figsize=(16, 10))
plt.rc("lines", markersize=4)
plt.rcParams["figure.autolayout"] = True
sns.set_context("poster")
init_notebook_mode(connected=True)
pio.templates.default = "plotly_dark"


class InputVariables:
    def __init__(self, data: DataFrame, col="Close") -> None:
        self.data: DataFrame = data.copy()
        self.col: str = col

    def calculate_log_returns(self) -> None:
        self.data["log_returns"] = np.log(self.data[self.col]) - np.log(
            self.data[self.col].shift(1)
        )

    def add_Indicators(self) -> None:
        inds = pd.DataFrame()
        succeed = []
        failed = []
        for func in talib.get_functions():
            try:
                ind = getattr(talib, func)(self.data.loc[:, self.col]).rename(func)
                inds = pd.concat([inds, ind], axis=1)
                succeed += [func]
            except:
                failed += [func]
        self.data = pd.concat([self.data, inds], axis=1)

    def clean_data(self, threshold) -> None:
        df: DataFrame = self.data
        # calculate the percentage of missing values for each column
        percent_missing = df.isna().sum() / len(df)

        # create a boolean mask of columns that exceed the threshold percentage
        mask = percent_missing > threshold

        # use the boolean mask to select only the columns that don't exceed the threshold
        self.data = df.loc[:, ~mask]

    def generate_all(self, threshold=0.05) -> DataFrame:
        self.calculate_log_returns()
        self.add_Indicators()
        self.clean_data(threshold)
        return self.data


class DataPreparer(InputVariables):
    def __init__(
        self,
        df: pd.DataFrame,
        target_col: str,
        testsize: float = 0.3,
        random_state: int = 101,
        shuffle=False,
        features: Optional[list] = None,
        scale: bool = True,
    ) -> None:
        super().__init__(df, target_col)
        self.target_col: str = target_col
        self.testsize: float = testsize
        self.random_state: int = random_state
        self.shuffle: bool = shuffle
        self.scale: bool = scale
        self.startup(features)

    def startup(self, features) -> None:
        self.data = self.generate_all().dropna()
        if self.scale:
            self.X: DataFrame = self.scale_data(
                self.data.drop(columns=[self.target_col]).loc[:, features]
                if features
                else self.data.drop(columns=[self.target_col])
            )
        else:
            self.X: DataFrame = (
                self.data.drop(columns=[self.target_col]).loc[:, features]
                if features
                else self.data.drop(columns=[self.target_col])
            )
        self.y: DataFrame = self.data[[self.target_col]]
        self.train_test_split()

    def scale_data(self, X: pd.DataFrame) -> pd.DataFrame:
        scaler = StandardScaler()
        scaled_X = pd.DataFrame(
            scaler.fit_transform(X), index=X.index, columns=X.columns
        )
        return scaled_X

    def train_test_split(self) -> None:
        X_train, X_test, y_train, y_test = train_test_split(
            self.X,
            self.y,
            test_size=self.testsize,
            shuffle=self.shuffle,
            random_state=self.random_state,
        )
        self.X_train = X_train.sort_index()
        self.X_test = X_test.sort_index()
        self.y_train = y_train.sort_index()
        self.y_test = y_test.sort_index()

    def plot(self) -> go.Figure:
        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=self.X_train.index,
                y=self.y_train[self.target_col],
                mode="lines",
                name=f"Train Data {1 - self.testsize}%",
            )
        )
        fig.add_trace(
            go.Scatter(
                x=self.X_test.index,
                y=self.y_test[self.target_col],
                mode="lines",
                name=f"Test Data {self.testsize}%",
            )
        )

        fig.update_layout(
            title="Train and Test Data",
            xaxis_title="Date",
            yaxis_title=self.target_col,
        )
        return fig
