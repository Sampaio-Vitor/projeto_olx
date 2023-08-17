import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline, FunctionTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, mean_absolute_percentage_error
import yaml
import joblib
from sklearn.model_selection import train_test_split
from utils.utils import load_config, save_model, load_data, evaluate_model
import matplotlib.pyplot as plt



# Import necessary functions from utils
from utils.utils import select_features_and_target, train_model, load_config, save_model, load_data, evaluate_model



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

# Instead of making training a part of pipeline, we use the pipeline for transformations and prediction
modeling_pipeline = Pipeline(steps=[
    ('model', best_regressor)
])

if __name__ == "__main__":
    # Load the data
    data = load_data("data/processed_data.csv")

    # Splitting data to train and test sets
    X, y = select_features_and_target(data, features, target)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train the model using the pipeline
    trained_pipeline = modeling_pipeline.fit(X_train, y_train)
    
    # Save the trained model
    save_model(trained_pipeline, "models/best_model.pkl")  # Save the entire pipeline

    # Evaluate the model
    predictions = trained_pipeline.predict(X_test)
    

    
     # Evaluate the model
    evaluate_model(trained_pipeline, X_test, y_test)

         # Convert predictions and true target values to linear scale
    predictions_linear = np.exp(predictions)
    y_test_linear = np.exp(y_test)

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.scatter(y_test_linear, predictions_linear, alpha=0.5)
    plt.plot([min(y_test_linear), max(y_test_linear)], [min(y_test_linear), max(y_test_linear)], linestyle='--', color='red')  # Diagonal line
    plt.title("Predicted vs True Values")
    plt.xlabel("True Values")
    plt.ylabel("Predicted Values")
    plt.show()

    # Evaluate the model
    evaluate_model(trained_pipeline, X_test, y_test)