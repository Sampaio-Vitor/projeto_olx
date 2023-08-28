# 1. Necessary package imports
import pandas as pd
from sklearn.pipeline import Pipeline, FunctionTransformer
import numpy as np
from joblib import dump
#import sys
#sys.path.append("C:/Users/vitor/OneDrive/Área de Trabalho/projetos/projeto_olx/")

expected_columns = [
    "TITLE",
    "LINK",
    "DATE_SCRAPE",
    "CITY",
    "CEP",
    "NEIGHBORHOOD",
    "CONDO",
    "TAX",
    "AREA",
    "ROOMS_NO",
    "BATH_NO",
    "PARKING_SPOTS",
    "APARTMENT_DETAILS",
    "PRICE",
    "REGION",
    "REGIONS",
    "DETAIL_Academia",
    "DETAIL_Ar condicionado",
    "DETAIL_Armários na cozinha",
    "DETAIL_Armários no quarto",
    "DETAIL_Churrasqueira",
    "DETAIL_Mobiliado",
    "DETAIL_Piscina",
    "DETAIL_Quarto de serviço",
    "DETAIL_Varanda",
    "DETAIL_Área de serviço",
    "LOG_AVG_PRICE_PER_SQMT_BY_REGION",
    "REGION_barreiro",
    "REGION_pampulha",
    "REGION_venda_nova",
    "REGION_zona_centro_sul",
    "REGION_zona_leste",
    "REGION_zona_nordeste",
    "REGION_zona_noroeste",
    "REGION_zona_norte",
    "REGION_zona_oeste",
    "LOG_AREA",
    "LOG_PRICE",
    "UTILS"
]



# 2. Importing utility functions
from src.utils.utils import (
    transform_currency_column_final,
    transform_area_column_updated,
    transform_condo_column_final,
    transform_tax_column_final,
    replace_nan_with_zero,
    replace_nan_in_condo_and_tax,
    drop_rows_with_zero_area,
    drop_rows_with_nan_area,
    transform_bath_no_column_updated,
    drop_rows_with_nan_bath_no,
    transform_parking_spots_column,
    drop_rows_with_nan_parking_spots,
    transform_rooms_no_column,
    drop_rows_with_nan_rooms_no,
    create_apartment_details_dummies,
    drop_duplicated_rows,
    drop_duplicated_links,
    drop_zero_values_in_columns,
    drop_low_price_values,
    drop_high_price_values,
    fill_avg_price_per_sqmt,  # Updated function import
    create_region_dummies,
    apply_log_transformations,
    create_utils_column,
    drop_non_log_columns,
    load_data,
    load_config,
    EnsureColumnsTransformer,
    ColumnOrderEnsurer,
    DropDuplicateColumns
)
config = load_config("config.yaml")
avg_price_dict = config['model']['avg_price_per_sqmt_dict']

# 3. Setting up the transformation pipeline
final_transformation_pipeline = Pipeline(steps=[
    ('ensure_columns', EnsureColumnsTransformer(expected_columns)),
    ('transform_condo', FunctionTransformer(func=transform_condo_column_final, validate=False)),
    ('transform_tax', FunctionTransformer(func=transform_tax_column_final, validate=False)),
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
    ('drop_low_price', FunctionTransformer(func=drop_low_price_values, validate=False)),
    ('drop_high_price', FunctionTransformer(func=drop_high_price_values, validate=False)),
    ('fill_avg_price_sqmt', FunctionTransformer(func=fill_avg_price_per_sqmt, 
                                                validate=False, 
                                                kw_args={'avg_price_dict': avg_price_dict})),  
    ('region_dummies', FunctionTransformer(func=create_region_dummies, validate=False)),
    ('log_transformations', FunctionTransformer(func=apply_log_transformations, validate=False)),
    ('create_utils', FunctionTransformer(func=create_utils_column, validate=False)),
    #('drop_non_log', FunctionTransformer(func=drop_non_log_columns, validate=False)),
    ('drop_duplicates', DropDuplicateColumns()),
    ('column_order_ensurer', ColumnOrderEnsurer(expected_columns=expected_columns)),
])

if __name__ == "__main__":
    # Load the data
    data = load_data("data/train_data/final_dataframe.csv")
    
    # Apply transformations using the pipeline
    transformed_data = final_transformation_pipeline.transform(data)
    
    # Save the processed data
    transformed_data.to_csv("data/processed_data.csv", index=False)

    # Save the transformation pipeline
    dump(final_transformation_pipeline, 'src/transformation/pipelines/final_transformation_pipeline.pkl')