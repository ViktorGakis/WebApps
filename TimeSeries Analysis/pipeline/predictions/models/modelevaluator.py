from warnings import filterwarnings

from .learning_curve import LearningCurve

filterwarnings("ignore")
from typing import Any, Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.graph_objs as go
import plotly.io as pio
import seaborn as sns
from plotly.offline import init_notebook_mode
from sklearn.base import BaseEstimator
from sklearn.model_selection import GridSearchCV, cross_val_score, learning_curve

sns.set(style="darkgrid")
plt.style.use("dark_background")
plt.rcParams.update({"grid.linewidth": 0.5, "grid.alpha": 0.5})
plt.rc("figure", figsize=(16, 10))
plt.rc("lines", markersize=4)
plt.rcParams["figure.autolayout"] = True
sns.set_context("poster")
init_notebook_mode(connected=True)
pio.templates.default = "plotly_dark"


class ModelEvaluator(LearningCurve):
    """
    A class for evaluating machine learning models using grid search cross-validation and learning curves.

    Parameters
    ----------
    model : BaseEstimator
        A scikit-learn estimator object to be evaluated.
    data_preparer : DataPreparer
        A DataPreparer object containing the training and testing data.

    Attributes
    ----------
    model : BaseEstimator
        The best-performing estimator found by grid search.
    data_preparer : DataPreparer
        The DataPreparer object used to prepare the training and testing data.
    cv_scores : array-like
        Cross-validated scores of the model.
    predictions : DataFrame
        Predictions of the model on the testing data.
    best_score : float
        Best cross-validated score achieved by the model.
    best_params : dict
        Parameters of the best-performing estimator found by grid search.

    Methods
    -------
    gridcv_tune(param_grid=None, scoring='r2', cv=5)
        Tune the hyperparameters of the model using grid search cross-validation.
    plot_learning_curve()
        Plot the learning curve of the model.
    plot()
        Plot the predictions of the model on the training and testing data.
    """

    def __init__(self, model, data_preparer) -> None:
        self.model = model
        self.data_preparer = data_preparer
        self.cv_scores = None
        self.predictions = None

    def gridcv_tune(
        self,
        param_grid: Optional[dict[str, Any]] = None,
        scoring: str = "r2",
        cv: int = 5,
    ):
        if param_grid is None:
            param_grid = {
                # default parameter grid, can be updated based on the model
            }
        self.cv: int = cv

        # Perform grid search cross-validation
        self.grid_search = GridSearchCV(
            self.model, param_grid, cv=self.cv, scoring=scoring
        )
        self.grid_search.fit(self.data_preparer.X_train, self.data_preparer.y_train)
        self.model: BaseEstimator = self.grid_search.best_estimator_

        # Add logic for different model types to extract coefficients/feature importances
        self.best_params = self.grid_search.best_params_

        # Get the best score
        self.best_score: float = self.grid_search.best_score_
        print(f"Best cross-validated score: {self.best_score:.2f}")

        # Make predictions on the test set
        self.predictions = pd.DataFrame(
            self.model.predict(self.data_preparer.X_test),
            index=self.data_preparer.y_test.index,
            columns=[self.data_preparer.target_col],
        )

        # Calculate cross-validated R-squared scores
        self.cv_scores = cross_val_score(
            self.model,
            self.data_preparer.X,
            self.data_preparer.y,
            cv=self.cv,
            scoring=scoring,
        )

    def extract_features(self, threshold=0):
        if not hasattr(self, "grid_search"):
            raise ValueError("No grid search object found.")
        filtered_coef = None
        if hasattr(self.model, "coef_"):
            # Extract feature coefficients above the threshold
            self.coef_ = self.model.coef_
            coef = pd.DataFrame(
                self.model.coef_.T,
                index=self.data_preparer.X_train.columns,
                columns=["Coefficients"],
            )
            filtered_coef = coef[abs(coef["Coefficients"]) >= threshold]
        elif hasattr(self.model, "feature_importances_"):
            # Extract feature importances above the threshold
            self.feature_importances = self.model.feature_importances_
            importances = pd.DataFrame(
                self.model.feature_importances_,
                index=self.data_preparer.X_train.columns,
                columns=["Importances"],
            )
            filtered_coef = importances[importances["Importances"] >= threshold]
        else:
            raise ValueError(
                "The specified model does not have feature coefficients or importances."
            )

        return filtered_coef

    def plot(self) -> go.Figure:
        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=self.predictions.index,
                y=self.predictions[self.data_preparer.target_col],
                mode="lines",
                name=f"Predictions",
            )
        )

        fig.add_trace(
            go.Scatter(
                x=self.data_preparer.X_train.index,
                y=self.data_preparer.y_train[self.data_preparer.target_col],
                mode="lines",
                name=f"Train Data {1 - self.data_preparer.testsize}%",
            )
        )
        fig.add_trace(
            go.Scatter(
                x=self.data_preparer.X_test.index,
                y=self.data_preparer.y_test[self.data_preparer.target_col],
                mode="lines",
                name=f"Test Data {self.data_preparer.testsize}%",
            )
        )

        fig.update_layout(
            title=f"Train and Test Data",
            xaxis_title="Index",
            yaxis_title=self.data_preparer.target_col,
        )
        return fig
