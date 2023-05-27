from .featureanalyzer import FeatureAnalyzer
from .preprocess import InputVariables, DataPreparer

PreprocessParams = {
        "ticker": {
            "default":"MSFT",
            "type": "text"
        },
        "target_col": {
            "default":"Close",
            "type": "text",
        },
        "test_size": {
            "default":0.2,
            "type": "range",
            "step": 0.01,
            "min": 0.01,
            "max": 1
        },
}