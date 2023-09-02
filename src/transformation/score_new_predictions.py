import pandas as pd
from joblib import load
from src.utils.utils import load_config
import numpy as np
import boto3
import io
from io import StringIO
import os
#import sys
#sys.path.append("C:/Users/vitor/OneDrive/Área de Trabalho/projetos/projeto_olx/")

s3 = boto3.client('s3',
                  aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
                  aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
                  region_name=os.environ.get('AWS_REGION', 'sa-east-1')) 
bucket_name = 'bucketolx'

def save_to_s3(df, file_name):
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    s3.put_object(Body=csv_buffer.getvalue(), Bucket=bucket_name, Key=file_name)

def read_from_s3(file_name):
    obj = s3.get_object(Bucket=bucket_name, Key=file_name)
    return pd.read_csv(io.BytesIO(obj['Body'].read()))



config = load_config("config.yaml")
features_predict  = config['model']['features']
if __name__ == "__main__":

    # Load your new data, the trained model, and the preprocessing pipeline
    new_data = read_from_s3("data/dados_detalhados_olx.csv")
    preprocessing_pipeline = load("src/transformation/pipelines/final_transformation_pipeline.pkl")
    trained_model = load("models/best_model.pkl")  
    
    # Apply the pipeline to preprocess the new data
    preprocessed_data = preprocessing_pipeline.transform(new_data)
    

    # Now, score the preprocessed data
    predictions = trained_model.predict(preprocessed_data[features_predict])

    # Convert predictions from log scale to linear scale
    predictions_linear = np.exp(predictions)

    # Add the predictions in linear scale to your DataFrame
    preprocessed_data['Predictions'] = predictions_linear
    
    # Save or process scored data as needed
    save_to_s3(preprocessed_data, "data/scored_data.csv")
