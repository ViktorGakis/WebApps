from .elasticnet import ElasticNetRegressor


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