import pandas as pd
from joblib import load
from src.utils.utils import load_config

config = load_config("config.yaml")
features_predict  = config['model']['features']
if __name__ == "__main__":

    # Load your new data, the trained model, and the preprocessing pipeline
    new_data = pd.read_csv("data/dados_detalhados_olx.csv")
    preprocessing_pipeline = load("src/transformation/pipelines/final_transformation_pipeline.pkl")
    trained_model = load("models/best_model.pkl")  
    
    # Apply the pipeline to preprocess the new data
    preprocessed_data = preprocessing_pipeline.transform(new_data)
    nan_counts_by_region = preprocessed_data[preprocessed_data['LOG_AVG_PRICE_PER_SQMT_BY_REGION'].isna()]['REGION'].value_counts()
    print(nan_counts_by_region)

    # Now, score the preprocessed data
    predictions = trained_model.predict(preprocessed_data[features_predict])
    
    # You can add these predictions to your preprocessed_data dataframe or save them separately.
    # This line appends predictions as a new column:
    preprocessed_data['Predictions'] = predictions
    
    # Save or process scored data as needed
    preprocessed_data.to_csv("data/scored_data.csv", index=False)
