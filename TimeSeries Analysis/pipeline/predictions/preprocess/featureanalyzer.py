from warnings import filterwarnings

filterwarnings("ignore")
from typing import Dict, List, Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio
import seaborn as sns
from pandas import DataFrame
from pandas.core.frame import DataFrame
from plotly.offline import init_notebook_mode
from sklearn.base import BaseEstimator
from sklearn.feature_selection import VarianceThreshold, mutual_info_regression
from sklearn.preprocessing import StandardScaler
from statsmodels.stats.outliers_influence import variance_inflation_factor

sns.set(style="darkgrid")
plt.style.use("dark_background")
plt.rcParams.update({"grid.linewidth": 0.5, "grid.alpha": 0.5})
plt.rc("figure", figsize=(16, 10))
plt.rc("lines", markersize=4)
plt.rcParams["figure.autolayout"] = True
sns.set_context("poster")
init_notebook_mode(connected=True)
pio.templates.default = "plotly_dark"


class FeatureAnalyzer:
    """
    A class for feature analysis and selection.

    Parameters:
    -----------
    X : pandas.DataFrame
        The features matrix to analyze.

    y : pandas.DataFrame
        The target vector.

    model : sklearn.base.BaseEstimator
        A supervised learning model used to extract feature importances. Default is None.

    Methods:
    --------
    corr() -> pandas.DataFrame:
        Calculates the Pearson correlation coefficients between the features and the target.

    mutual_info() -> pandas.DataFrame:
        Calculates the mutual information between the features and the target.

    corr_matrix() -> pandas.DataFrame:
        Calculates the Pearson correlation matrix between the features.

    filter_threshold(df, column, threshold, greater=False) -> List[str]:
        Filters a DataFrame based on a given column and a threshold.

    filter_corr(threshold) -> List[str]:
        Filters the features based on the Pearson correlation coefficient.

    filter_mutual_info(threshold) -> List[str]:
        Filters the features based on the mutual information.

    filter_corr_matrix(threshold=0.3) -> List[str]:
        Filters the features based on the Pearson correlation matrix.

    identify_zero_variance() -> List[str]:
        Identifies the features with zero variance.

    identify_collinear(threshold) -> List[str]:
        Identifies the collinear features based on the VIF score.

    get_feature_importance() -> pandas.DataFrame:
        Extracts the feature importance from the model.

    identify_low_importance(threshold) -> List[str]:
        Identifies the features with low importance based on a threshold.

    combine_criteria(collinear_threshold=5, importance_threshold=0.01,
                     correlation_threshold=0.3, mutual_info_threshold=0.2) -> List[str]:
        Combines multiple feature selection criteria to select the best features.

    transform_X() -> pandas.DataFrame:
        Returns a new DataFrame with the selected features.

    summary(missing_threshold=0.1, collinear_threshold=5, importance_threshold=0.01,
            correlation_threshold=0.3, mutual_info_threshold=0.2) -> Dict[str, Dict[str, Union[List[str], int]]]:
        Returns a summary of the feature analysis and selection process.
    """

    def __init__(self, X: DataFrame, y: DataFrame, model: BaseEstimator = None) -> None:
        self.X: DataFrame = X
        self.y: DataFrame = y
        self.model: BaseEstimator = model

    def corr(self) -> DataFrame:
        return pd.DataFrame(
            np.corrcoef(np.column_stack((self.X, self.y)).T)[:-1, -1],
            columns=["pearson_corr"],
            index=self.X.columns,
        )

    def mutual_info(self) -> DataFrame:
        return pd.DataFrame(
            mutual_info_regression(self.X, self.y),
            columns=["mutual_info"],
            index=self.X.columns,
        )

    def corr_matrix(self) -> pd.DataFrame:
        return self.X.corr(method="pearson")

    def filter_threshold(
        self, df: DataFrame, column: str, threshold: float, greater: bool = False
    ) -> List[str]:
        mask = df[column] > threshold if greater else df[column] < threshold
        return df[mask].index.to_list()

    def filter_corr(self, threshold) -> List[str]:
        return self.filter_threshold(
            self.corr(), "pearson_corr", threshold, greater=False
        )

    def filter_mutual_info(self, threshold) -> List[str]:
        return self.filter_threshold(
            self.mutual_info(),
            "mutual_info",
            self.mutual_info().mutual_info.quantile(threshold),
            greater=False,
        )

    def filter_corr_matrix(self, threshold=0.3) -> list:
        corr_matrix: DataFrame = self.corr_matrix()
        np.fill_diagonal(corr_matrix.values, 0)
        stacked_corr_matrix = corr_matrix.abs().stack().reset_index()
        stacked_corr_matrix.columns = ["feature_1", "feature_2", "correlation"]
        filtered_corr_matrix = self.filter_threshold(
            stacked_corr_matrix, "correlation", threshold, greater=False
        )

        return list(
            set(filtered_corr_matrix["feature_1"].unique())
            | set(filtered_corr_matrix["feature_2"].unique())
        )

    def identify_missing(self, threshold: float) -> List[str]:
        return self.filter_threshold(
            self.X.isnull().mean().to_frame("missing_fraction"),
            "missing_fraction",
            threshold,
            greater=True,
        )

    def identify_zero_variance(self) -> List[str]:
        selector = VarianceThreshold(threshold=0)
        selector.fit(self.X)
        return list(self.X.columns[~selector.get_support()])

    def identify_collinear(self, threshold: float) -> List[str]:
        # Scale the features
        X_scaled = StandardScaler().fit_transform(self.X)
        vif_data = pd.DataFrame()
        vif_data["feature"] = self.X.columns
        vif_data["VIF"] = [
            variance_inflation_factor(X_scaled, i) for i in range(len(self.X.columns))
        ]
        return list(vif_data.loc[vif_data["VIF"] < threshold, "feature"])

    def get_feature_importance(self) -> pd.DataFrame:
        if self.model is None:
            raise ValueError("A model must be provided for this method.")

        if hasattr(self.model, "feature_importances_"):
            importances = self.model.feature_importances_
        elif hasattr(self.model, "coef_"):
            importances = np.abs(self.model.coef_)
        else:
            raise ValueError(
                "The provided model does not have the feature_importances_' or 'coef_' attribute."
            )
        feature_importance_df = pd.DataFrame(
            importances, columns=["importance"], index=self.X.columns
        )
        return feature_importance_df.sort_values(by="importance", ascending=False)

    def identify_low_importance(self, threshold: float) -> List[str]:
        if self.model is None:
            raise ValueError("A model must be provided for this method.")

        return self.filter_threshold(
            self.get_feature_importance(), "importance", threshold, greater=False
        )

    def combine_criteria(
        self,
        collinear_threshold=5,
        importance_threshold=0.01,
        correlation_threshold=0.3,
        mutual_info_threshold=0.2,
        intersection: bool = True,
    ) -> List[str]:
        criteria: List[List[str]] = [
            self.identify_collinear(collinear_threshold),
            self.filter_corr(correlation_threshold),
            self.filter_mutual_info(mutual_info_threshold),
        ]
        if self.model is not None:
            criteria.append(self.identify_low_importance(importance_threshold))
        if intersection:
            selected_features = set.intersection(*map(set, criteria)) - set(
                self.identify_zero_variance()
            )
        else:
            selected_features = set.union(*map(set, criteria)) - set(
                self.identify_zero_variance()
            )
        return list(selected_features)

    def transform_X(self) -> DataFrame:
        selected_features = set(self.combine_criteria())
        return self.X.loc[:, list(selected_features)]

    def summary(
        self,
        missing_threshold=0.1,
        collinear_threshold=5,
        importance_threshold=0.01,
        correlation_threshold=0.3,
        mutual_info_threshold=0.2,
    ) -> Dict[str, Dict[str, Union[List[str], int]]]:
        summary_dict = {
            "missing_values": {
                "features": self.identify_missing(missing_threshold),
                "count": len(self.identify_missing(missing_threshold)),
            },
            "zero_variance": {
                "features": self.identify_zero_variance(),
                "count": len(self.identify_zero_variance()),
            },
            "not_collinear": {
                "features": self.identify_collinear(collinear_threshold),
                "count": len(self.identify_collinear(collinear_threshold)),
            },
            "low_correlation": {
                "features": self.filter_corr(correlation_threshold),
                "count": len(self.filter_corr(correlation_threshold)),
            },
            "low_mutual_info": {
                "features": self.filter_mutual_info(mutual_info_threshold),
                "count": len(self.filter_mutual_info(mutual_info_threshold)),
            },
            "combined_criteria": {
                "features": self.combine_criteria(
                    collinear_threshold,
                    importance_threshold,
                    correlation_threshold,
                    mutual_info_threshold,
                ),
                "count": len(
                    self.combine_criteria(
                        collinear_threshold,
                        importance_threshold,
                        correlation_threshold,
                        mutual_info_threshold,
                    )
                ),
            },
        }

        if self.model is not None:
            summary_dict["low_importance"] = {
                "features": self.identify_low_importance(importance_threshold),
                "count": len(self.identify_low_importance(importance_threshold)),
            }

        return summary_dict
