from warnings import filterwarnings

filterwarnings("ignore")

import numpy as np
from sklearn.linear_model import ElasticNet
from sklearn.metrics import mean_absolute_error, mean_squared_error

from .modelevaluator import ModelEvaluator


class ElasticNetRegressor(ModelEvaluator):
    def __init__(self, data_preparer) -> None:
        super().__init__(ElasticNet(), data_preparer)

    def evaluate(self):
        mae = mean_absolute_error(self.data_preparer.y_test, self.predictions)
        mse = mean_squared_error(self.data_preparer.y_test, self.predictions)

        print(
            f"""Mean Absolute Error (MAE): {mae:.2f}
        Mean Squared Error (MSE): {mse:.2f}
        Cross-validated R-squared scores: {self.cv_scores}
        Average cross-validated R-squared score: {np.mean(self.cv_scores):.2f}"""
        )
        return (mae, mse, self.cv_scores, np.mean(self.cv_scores))

    def get_summary_dict(self, threshold) -> dict:
        filtered_coef = self.extract_features(threshold)
        summary_dict = {
            "model": type(self.model).__name__,
            "target_variable": self.data_preparer.target_col,
            "num_input_features": self.data_preparer.X_train.shape[1],
            "cv_folds": self.cv,
            "best_params": self.best_params,
            "best_cv_score": self.best_score,
            "cv_scores": self.cv_scores,
            "coefficients": self.coef_,
            "filtered_coef": filtered_coef.sort_values(by="Coefficients").rename(
                {"Coefficients": ""}, axis=1
            ),
            "MAE": mean_absolute_error(self.data_preparer.y_test, self.predictions),
            "MSE": mean_squared_error(self.data_preparer.y_test, self.predictions),
            "Average cross-validated R-squared score": np.mean(self.cv_scores),
        }
        return summary_dict

    def summarize(self, threshold=0) -> str:
        self.threshold = threshold
        summary_dict = self.get_summary_dict(threshold)
        return f"""Model summary:
    Model: {summary_dict['model']}
    Target variable: {summary_dict['target_variable']}
    Number of input features: {summary_dict['num_input_features']}
    Cross-validation fold: {summary_dict['cv_folds']}
Evaluation:    
    Best_params: {summary_dict['best_params']}
    Best cross-validated score: {summary_dict['best_cv_score']:.2f}
    Mean Absolute Error (MAE): {summary_dict['MAE']:.2f}
    Mean Squared Error (MSE): {summary_dict['MSE']:.2f}
    Cross-validated R-squared scores: {summary_dict['cv_scores']}
Filtered_coef>{self.threshold}: {summary_dict['filtered_coef']}"""


ElasticNetParams = {
        "cv": {
            "default":5,
            "type": "number"
        },
        "threshold": {
            "default":0,
            "type": "number",
            "step": 0.01,
        },
        "alpha": {
            "default":1,
            "grid_values":[0.001, 0.01, 0.1, 1, 10, 100],
            "type": "number",
            "step": 0.01,
            "min": 0.001,
            "max": 100
        },
        "l1_ratio": {
            "default":0.5,
            "min": 0,
            "max": 1,
            "step": 0.01,            
            "grid_values": [0.1, 0.3, 0.5, 0.7, 0.9],
            "type": "range"
        },
        "max_iter": {
            "default":1000,
            "min": 1000,
            "step": 100,              
            "grid_values": [1000, 2000, 5000],
            "type": "number"
        },
        "tol": {
            "default":1e-4,
            "grid_values": [1e-6, 1e-5, 1e-4],
            "type": "number",
            "step": 1e-6,
        },
        "selection": {
            "options":['cyclic', 'random'],
            "default":"cyclic",
            "grid_values":['cyclic', 'random'],
        }
}