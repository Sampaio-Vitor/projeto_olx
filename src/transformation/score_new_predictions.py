import pandas as pd
from joblib import load
from utils.utils import load_config
import numpy as np
import sys
sys.path.append("C:/Users/vitor/OneDrive/Área de Trabalho/projetos/projeto_olx/")





config = load_config("config.yaml")
features_predict  = config['model']['features']
if __name__ == "__main__":

    # Load your new data, the trained model, and the preprocessing pipeline
    new_data = pd.read_csv("data/dados_detalhados_olx.csv")
    preprocessing_pipeline = load("src/transformation/pipelines/final_transformation_pipeline.pkl")
    trained_model = load("models/best_model.pkl")  
    
    # Apply the pipeline to preprocess the new data
    preprocessed_data = preprocessing_pipeline.transform(new_data)
    nan_counts = preprocessed_data.isnull().sum()
    for column, nan_count in nan_counts.items():
        if nan_count > 0:
            print(f"Column: {column}, NaN Count: {nan_count}")
    region_counts = preprocessed_data['REGION'].value_counts()
    print(region_counts)





    # Now, score the preprocessed data
    predictions = trained_model.predict(preprocessed_data[features_predict])

    # Convert predictions from log scale to linear scale
    predictions_linear = np.exp(predictions)

    # Add the predictions in linear scale to your DataFrame
    preprocessed_data['Predictions'] = predictions_linear
    
    # Save or process scored data as needed
    preprocessed_data.to_csv("data/scored_data.csv", index=False)
