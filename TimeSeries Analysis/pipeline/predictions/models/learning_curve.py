from warnings import filterwarnings

filterwarnings("ignore")

import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
import plotly.graph_objs as go
import plotly.io as pio
import seaborn as sns
from plotly.offline import init_notebook_mode
from sklearn.model_selection import (
    learning_curve,
)

sns.set(style="darkgrid")
plt.style.use("dark_background")
plt.rcParams.update({"grid.linewidth": 0.5, "grid.alpha": 0.5})
plt.rc("figure", figsize=(16, 10))
plt.rc("lines", markersize=4)
plt.rcParams["figure.autolayout"] = True
sns.set_context("poster")
init_notebook_mode(connected=True)
pio.templates.default = "plotly_dark"


class LearningCurve:
    def calculate_learning_curve(self, train_sizes=None, cv=None):
        if not hasattr(self, "model"):
            raise ValueError("There is no model available.")
        if train_sizes is None:
            train_sizes = np.linspace(0.1, 1.0, 10)
        if self.cv is None:
            self.cv = cv
        # Compute the learning curve
        (
            self.train_sizes_abs,
            self.train_scores,
            self.val_scores,
            self.fit_times,
            _,
        ) = learning_curve(
            self.model,
            self.data_preparer.X,
            self.data_preparer.y,
            train_sizes=train_sizes,
            cv=self.cv,
            scoring="neg_root_mean_squared_error",
            n_jobs=-1,
            verbose=1,
            return_times=True,
        )
        # Compute the mean and standard deviation of the scores
        self.train_scores_mean = -np.mean(self.train_scores, axis=1)
        self.train_scores_std = -np.std(self.train_scores, axis=1)
        self.val_scores_mean = -np.mean(self.val_scores, axis=1)
        self.val_scores_std = -np.std(self.val_scores, axis=1)

        # Compute the mean fit time
        self.fit_times_mean = np.mean(self.fit_times, axis=1)

    def calculate_optimal_size(self):
        optimal_idx = np.argmin(self.val_scores_mean)
        self.optimal_size = self.train_sizes_abs[optimal_idx]
        self.optimal_size_pct = round(self.optimal_size / dp.X.shape[0], 2)

    def plot_learning_curve(self) -> go.Figure:
        fig = go.Figure()

        # Plot the training scores
        fig.add_trace(
            go.Scatter(
                x=self.train_sizes_abs,
                y=self.train_scores_mean,
                mode="lines+markers",
                name="Training score",
                line=dict(color="blue"),
                error_y=dict(
                    type="data", array=self.train_scores_std, visible=True, color="blue"
                ),
            )
        )

        # Plot the validation scores
        fig.add_trace(
            go.Scatter(
                x=self.train_sizes_abs,
                y=self.val_scores_mean,
                mode="lines+markers",
                name="Validation score",
                line=dict(color="green"),
                error_y=dict(
                    type="data", array=self.val_scores_std, visible=True, color="green"
                ),
            )
        )

        # Add a vertical line for the optimal training set size
        fig.add_shape(
            type="line",
            x0=self.optimal_size,
            x1=self.optimal_size,
            y0=0,
            y1=1,
            yref="paper",
            xref="x",
            line=dict(color="red", dash="dash"),
        )

        # Add a secondary y-axis for the training time
        fig.update_layout(
            yaxis2=dict(
                title="Training Time (s)", overlaying="y", side="right", showgrid=False
            ),
            title="Learning Curve",
            xaxis_title="Training Set Size",
            yaxis_title="Error (RMSE)",
        )

        # Plot the training time
        fig.add_trace(
            go.Scatter(
                x=self.train_sizes_abs,
                y=self.fit_times_mean,
                mode="lines+markers",
                name="Training Time",
                line=dict(color="orange"),
                yaxis="y2",
            )
        )

        # Add a text box with the model performance metric
        fig.add_annotation(
            x=0.05,
            y=0.95,
            xref="paper",
            yref="paper",
            text="Performance Metric: RMSE",
            showarrow=False,
            font=dict(size=12),
        )

        # Add a text box with the optimal training set size
        fig.add_annotation(
            x=self.optimal_size,
            y=0.05,
            xref="x",
            yref="paper",
            text=f"Optimal Size: {self.optimal_size}({self.optimal_size_pct}%)",
            showarrow=True,
            arrowhead=1,
            arrowcolor="red",
            font=dict(size=12),
        )

        return fig


