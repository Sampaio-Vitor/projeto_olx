import numpy as np
import pandas as pd
import yaml
from sklearn.pipeline import Pipeline, FunctionTransformer
from utils.utils import load_config

from utils.utils import (transform_condo_column_final, transform_tax_column_final, replace_nan_in_condo_and_tax,
                   transform_area_column_updated, drop_rows_with_nan_area, transform_bath_no_column_updated,
                   drop_rows_with_nan_bath_no, transform_parking_spots_column, drop_rows_with_nan_parking_spots,
                   transform_rooms_no_column, drop_rows_with_nan_rooms_no, create_apartment_details_dummies,
                   drop_duplicated_rows, drop_duplicated_links, drop_zero_values_in_columns, create_utils_column,
                   create_region_dummies, apply_log_area, score_new_data, fill_avg_price_per_sqmt, load_config)

config = load_config("config.yaml")
best_params = config['model']['best_params']
avg_price_per_sqmt_dict = config['model']['avg_price_per_sqmt_dict']


# Define the scoring pipeline
scoring_pipeline = Pipeline(steps=[
    ('transform_condo', FunctionTransformer(func=transform_condo_column_final, validate=False)),
    ('transform_tax', FunctionTransformer(func=transform_tax_column_final, validate=False)),
    ('fill_avg_price', FunctionTransformer(func=fill_avg_price_per_sqmt, kw_args={'avg_price_dict': avg_price_per_sqmt_dict}, validate=False)),
    ('replace_nan', FunctionTransformer(func=replace_nan_in_condo_and_tax, validate=False)),
    ('transform_area', FunctionTransformer(func=transform_area_column_updated, validate=False)),
    ('drop_nan_area', FunctionTransformer(func=drop_rows_with_nan_area, validate=False)),
    ('transform_bath_no', FunctionTransformer(func=transform_bath_no_column_updated, validate=False)),
    ('drop_nan_bath_no', FunctionTransformer(func=drop_rows_with_nan_bath_no, validate=False)),
    ('transform_parking_spots', FunctionTransformer(func=transform_parking_spots_column, validate=False)),
    ('drop_nan_parking_spots', FunctionTransformer(func=drop_rows_with_nan_parking_spots, validate=False)),
    ('transform_rooms_no', FunctionTransformer(func=transform_rooms_no_column, validate=False)),
    ('drop_nan_rooms_no', FunctionTransformer(func=drop_rows_with_nan_rooms_no, validate=False)),
    ('details_dummies', FunctionTransformer(func=create_apartment_details_dummies, validate=False)),
    ('drop_duplicates', FunctionTransformer(func=drop_duplicated_rows, validate=False)),
    ('drop_duplicate_links', FunctionTransformer(func=drop_duplicated_links, validate=False)),
    ('drop_zero_values', FunctionTransformer(func=drop_zero_values_in_columns, validate=False)),
    ('create_utils', FunctionTransformer(func=create_utils_column, validate=False)),
    ('region_dummies', FunctionTransformer(func=create_region_dummies, validate=False)),
    ('log_transformations', FunctionTransformer(func=apply_log_area, validate=False)),
])


if __name__ == "__main__":
    # Load your new data and model
    new_data = pd.read_csv("path_to_new_data.csv")
    trained_model = "path_to_serialized_model.pkl"  # Load the model using joblib or pickle
    
    # Apply the pipeline and score
    preprocessed_data = scoring_pipeline.transform(new_data)
    scored_data = score_new_data(preprocessed_data, trained_model, scoring_pipeline)
    
    # Save or process scored data as needed
    scored_data.to_csv("scored_data.csv", index=False)
