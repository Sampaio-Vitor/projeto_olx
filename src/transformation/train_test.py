import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline, FunctionTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error
import yaml
import joblib


# Import necessary functions from utils
from utils.utils import select_features_and_target, train_model, load_config, save_model



config = load_config("config.yaml")
features = config['model']['features']
target = config['model']['target']
best_params = config['model']['best_params']

# Define the best regressor with the provided parameters
best_regressor = RandomForestRegressor(
    n_estimators=int(best_params[0]),
    max_depth=int(best_params[1]) if best_params[1] is not None else None,
    min_samples_split=int(best_params[2]),
    min_samples_leaf=int(best_params[3]),
    random_state=42
)

# Create the pipeline
modeling_pipeline = Pipeline(steps=[
    ('select_columns', FunctionTransformer(func=select_features_and_target, validate=False, kw_args={"features": features, "target": target})),
    ('train_model', FunctionTransformer(func=train_model, validate=False, kw_args={"regressor": best_regressor})),
])

if __name__ == "__main__":
    # Assuming you have a load_data function or similar to get your dataset
    data = load_data("path_to_your_data.csv")
    
    # Splitting data to train and test sets
    X_train, X_test, y_train, y_test = train_test_split(data[features], data[target], test_size=0.2, random_state=42)
    
    # Train the model
    trained_pipeline = modeling_pipeline.fit(X_train, y_train)
    
    # Evaluate the model
    evaluate_model(trained_pipeline, X_test, y_test)  # Assuming evaluate_model is in utils.py or imported
