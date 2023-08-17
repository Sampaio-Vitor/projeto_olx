import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import yaml
import joblib
from sklearn.metrics import mean_squared_error, mean_absolute_error

def load_config(config_path):
    """
    Load the configuration from a YAML file.

    Args:
    - config_path (str): Path to the configuration YAML file.

    Returns:
    - dict: Configuration dictionary.
    """
    with open(config_path, 'r', encoding='utf-8') as config_file:
        config = yaml.safe_load(config_file)
    return config



# Atualizando a função para tratar valores inadequados antes da transformação
def transform_currency_column_final(data, column_name):
    data_copy = data.copy()
    
    # Ensure the column exists
    if column_name not in data_copy.columns:
        print(f"{column_name} column does not exist in the provided data.")
        return data_copy

    # Convert the entire column to string type before applying string operations
    data_copy[column_name] = data_copy[column_name].astype(str)

    # Then perform the string replacements
    data_copy[column_name] = data_copy[column_name].str.replace('R$ ', '', regex=False)
    data_copy[column_name] = data_copy[column_name].str.replace('.', '', regex=False).str.replace(',', '.', regex=False)

    # Convert to numeric
    data_copy[column_name] = pd.to_numeric(data_copy[column_name], errors='coerce')

    return data_copy
# Atualizando a função para tratar valores inadequados na coluna AREA
def transform_area_column_updated(data):
    data_copy = data.copy()
    
    # Ensure the 'AREA' column exists
    if 'AREA' not in data_copy.columns:
        print("AREA column does not exist in the provided data.")
        return data_copy

    # Convert the entire 'AREA' column to string type before applying string operations
    data_copy['AREA'] = data_copy['AREA'].astype(str)

    # Then perform the string replacements
    data_copy['AREA'] = data_copy['AREA'].str.replace('m²', '', regex=False)

    # Convert to numeric
    data_copy['AREA'] = pd.to_numeric(data_copy['AREA'], errors='coerce')

    return data_copy

# Atualizando as funções encapsuladas
def transform_condo_column_final(data):
    return transform_currency_column_final(data, 'CONDO')

def transform_tax_column_final(data):
    return transform_currency_column_final(data, 'TAX')



# Função para substituir NaN por 0 nas colunas especificadas
def replace_nan_with_zero(data, column_names):
    data_copy = data.copy()
    for col in column_names:
        data_copy[col] = data_copy[col].fillna(0)
    return data_copy

# Função encapsulada para o pipeline
def replace_nan_in_condo_and_tax(data):
    return replace_nan_with_zero(data, ['CONDO', 'TAX'])


# Função para remover linhas onde AREA é 0
def drop_rows_with_zero_area(data):
    return data[data['AREA'] != 0]


# Função para remover linhas onde AREA é NaN
def drop_rows_with_nan_area(data):
    return data.dropna(subset=['AREA'])

# Atualizando a função para tratar valores inadequados na coluna BATH_NO
def transform_bath_no_column_updated(data):
    data_copy = data.copy()

    # Substituindo '5 ou mais' por '5'
    data_copy['BATH_NO'] = data_copy['BATH_NO'].replace('5 ou mais', '5')

    # Tentando converter para int e substituindo valores inválidos por NaN
    data_copy['BATH_NO'] = pd.to_numeric(data_copy['BATH_NO'], errors='coerce', downcast='integer')

    return data_copy

# Função para remover linhas onde BATH_NO é NaN
def drop_rows_with_nan_bath_no(data):
    return data.dropna(subset=['BATH_NO'])

# Função para tratar a coluna PARKING_SPOTS
def transform_parking_spots_column(data):
    data_copy = data.copy()

    # Substituindo '5 ou mais' por '5'
    data_copy['PARKING_SPOTS'] = data_copy['PARKING_SPOTS'].replace('5 ou mais', '5')

    # Tentando converter para int e substituindo valores inválidos por NaN
    data_copy['PARKING_SPOTS'] = pd.to_numeric(data_copy['PARKING_SPOTS'], errors='coerce', downcast='integer')

    return data_copy

# Função para remover linhas onde PARKING_SPOTS é NaN
def drop_rows_with_nan_parking_spots(data):
    return data.dropna(subset=['PARKING_SPOTS'])

# Função para tratar a coluna ROOMS_NO
def transform_rooms_no_column(data):
    data_copy = data.copy()

    # Substituindo '5 ou mais' por '5'
    data_copy['ROOMS_NO'] = data_copy['ROOMS_NO'].replace('5 ou mais', '5')

    # Tentando converter para int e substituindo valores inválidos por NaN
    data_copy['ROOMS_NO'] = pd.to_numeric(data_copy['ROOMS_NO'], errors='coerce', downcast='integer')

    return data_copy

# Função para remover linhas onde ROOMS_NO é NaN
def drop_rows_with_nan_rooms_no(data):
    return data.dropna(subset=['ROOMS_NO'])

def create_apartment_details_dummies(data):
    data_copy = data.copy()

    # Removendo espaços em branco entre as vírgulas
    data_copy['APARTMENT_DETAILS'] = data_copy['APARTMENT_DETAILS'].apply(lambda x: ','.join(item.strip() for item in x.split(',')) if isinstance(x, str) else x)

    # Criando variáveis dummy para cada detalhe do apartamento
    dummies = data_copy['APARTMENT_DETAILS'].str.get_dummies(sep=',')

    # Renomeando as colunas das dummies
    dummies = dummies.rename(lambda x: 'DETAIL_' + x, axis='columns')

    # Concatenando o dataframe original com as colunas dummy
    data_copy = pd.concat([data_copy, dummies], axis=1)

    return data_copy

def drop_duplicated_rows(data):
    return data.drop_duplicates()

def drop_duplicated_links(data):
    return data.drop_duplicates(subset=['LINK'])

def drop_zero_values_in_columns(data):
    filtered_data = data[(data['ROOMS_NO'] != 0) & (data['AREA'] != 0) & (data['PRICE'] != 0) & (data['BATH_NO'] != 0)]
    return filtered_data

def drop_low_price_values(data):
    return data[data['PRICE'] >= 50000]

def drop_high_price_values(data):
    return data[data['PRICE'] <= 5000000]

def compute_avg_price_per_sqmt_by_region(data):
    data_copy = data.copy()

    # Calculando o preço médio por m² para cada bairro usando a coluna REGION
    avg_price_per_sqmt_by_region = data_copy.groupby('REGION').apply(lambda x: x['PRICE'].sum() / x['AREA'].sum()).to_dict()

    # Mapeando os valores médios para os registros no conjunto de dados
    data_copy['AVG_PRICE_PER_SQMT_BY_REGION'] = data_copy['REGION'].map(avg_price_per_sqmt_by_region)

    return data_copy



def create_region_dummies(data):
    data_copy = data.copy()

    # Criando variáveis dummy para a coluna REGION e garantindo que elas sejam inteiros
    dummies = pd.get_dummies(data_copy['REGION'], prefix='REGION', drop_first=False, dtype=int)

    # Concatenando o dataframe original com as colunas dummy
    data_copy = pd.concat([data_copy, dummies], axis=1)

    return data_copy

def apply_log_transformations(data):
    data_copy = data.copy()
    data_copy['LOG_AREA'] = np.log1p(data_copy['AREA'])
    data_copy['LOG_PRICE'] = np.log1p(data_copy['PRICE'])
    data_copy['LOG_AVG_PRICE_PER_SQMT_BY_REGION'] = np.log1p(data_copy['LOG_AVG_PRICE_PER_SQMT_BY_REGION'])
    return data_copy

# Function to create the UTILS column by adding TAX and CONDO columns
def create_utils_column(data):
    data_copy = data.copy()
    data_copy['UTILS'] = data_copy['TAX'] + data_copy['CONDO']
    return data_copy

def drop_non_log_columns(data):
    data_copy = data.copy()
    columns_to_drop = ['AREA', 'AVG_PRICE_PER_SQMT_BY_REGION']
    data_copy = data_copy.drop(columns=columns_to_drop)
    return data_copy

# Function to split the data into train and test
def split_data(data, test_size=0.2, random_state=42):
    train_data, test_data = train_test_split(data, test_size=test_size, random_state=random_state)
    return train_data, test_data


def select_features_and_target(data, features_columns, target):
    X = data[features_columns]  # todas as colunas exceto 'LOG_PRICE'
    y = data['LOG_PRICE']
    return X, y

def train_model(X, y, regressor):
    """
    Treina o modelo com os dados fornecidos.

    Args:
    - X (pd.DataFrame): dataframe de características.
    - y (pd.Series): série alvo.
    - regressor (estimator): modelo a ser treinado.

    Returns:
    - regressor: modelo treinado.
    """
    regressor.fit(X, y)
    return regressor

def mean_absolute_percentage_error(y_true, y_pred):
    """
    Calculate Mean Absolute Percentage Error
    """
    # Ensure arrays
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    
    # Avoid division by zero
    non_zero_indices = y_true != 0  
    
    return np.mean(np.abs((y_true[non_zero_indices] - y_pred[non_zero_indices]) / y_true[non_zero_indices])) * 100

def log_to_linear(values):
    return np.expm1(values)

def evaluate_model(model, X, y):
    """
    Evaluate the model using RMSE, MAE, and MAPE.
    """
    predictions = model.predict(X)
    
    # Calculate RMSE and MAE in log scale
    rmse_log = np.sqrt(mean_squared_error(y, predictions))
    mae_log = mean_absolute_error(y, predictions)
    
    print("Log Scale:")
    print(f"RMSE: {rmse_log}")
    print(f"MAE: {mae_log}")

    # Convert predictions and true target values to linear scale
    predictions_linear = log_to_linear(predictions)
    y_true_linear = log_to_linear(y)

    # Calculate MAPE on the linear scale
    mape_linear = mean_absolute_percentage_error(y_true_linear, predictions_linear)

    print("\nLinear Scale:")
    print(f"MAPE: {mape_linear}%")
    
    return rmse_log, mae_log, mape_linear


    
def score_new_data(new_data, model, pipeline, features_predict):
    """
    Pontua novos dados usando o modelo treinado e o pipeline de transformação.

    Args:
    - new_data (pd.DataFrame): Novos dados para pontuar.
    - model (estimator): Modelo treinado.
    - pipeline (Pipeline): Pipeline de transformação.
    - features_predict (list): List of features to use for prediction.

    Returns:
    - scored_data (pd.DataFrame): DataFrame with model predictions and transformed data.
    """
    # Transform the data
    transformed_data = pipeline.transform(new_data)
    
    # Save a copy of the transformed data
    transformed_copy = transformed_data.copy()
    
    # Select only the desired features
    transformed_data = transformed_data[features_predict]
    
    # Make predictions
    predictions = model.predict(transformed_data)
    
    # Create a copy of the original DataFrame with a new "predictions" column
    transformed_copy["predictions"] = np.exp(predictions) - 1
        
    return transformed_copy

def fill_avg_price_per_sqmt(new_data, avg_price_dict):
    # Assumindo que sua coluna de bairro nos novos dados também é chamada de "REGION"
    new_data['LOG_AVG_PRICE_PER_SQMT_BY_REGION'] = new_data['REGION'].map(avg_price_dict)
    return new_data

def apply_log_area (data):
    data_copy = data.copy()
    data_copy['LOG_AREA'] = np.log1p(data_copy['AREA'])
    return data_copy


def fill_avg_price_per_sqmt(new_data, avg_price_dict):
    # Assumindo que sua coluna de bairro nos novos dados também é chamada de "REGION"
    new_data['LOG_AVG_PRICE_PER_SQMT_BY_REGION'] = new_data['REGION'].map(avg_price_dict)
    return new_data

def apply_log_area (data):
    data_copy = data.copy()
    data_copy['LOG_AREA'] = np.log1p(data_copy['AREA'])
    return data_copy

def save_model(model, filename="best_model.pkl"):
    """
    Salva o modelo em um arquivo .pkl

    Args:
    - model (estimator): Modelo treinado.
    - filename (str): Nome do arquivo para salvar o modelo.
    """
    joblib.dump(model, filename)
    print(f"Model saved as {filename}")

# Loading data from CSV
def load_data(filepath):
    return pd.read_csv(filepath)

def calculate_mape(y_true, y_pred):
    errors = np.abs((y_true - y_pred) / y_true)
    mape = np.mean(errors) * 100
    return mape

def drop_non_string_rows_multi_columns(data, column_names):
    """
    Drop rows from a DataFrame where values in specific columns are not of string type.

    Args:
    - data (pd.DataFrame): The input DataFrame.
    - column_names (list): The list of columns in which to check for non-string values.

    Returns:
    - pd.DataFrame: A DataFrame with rows dropped where the specified columns had non-string values.
    """
    mask = np.all([data[column].apply(lambda x: isinstance(x, str)) for column in column_names], axis=0)
    return data[mask]

import pandas as pd

def transform_string_currency_column_final(data, column_name):
    data_copy = data.copy()
    
    # Ensure the column exists
    if column_name not in data_copy.columns:
        print(f"{column_name} column does not exist in the provided data.")
        return data_copy

    # Convert the entire column to string type before applying string operations
    data_copy[column_name] = data_copy[column_name].astype(str)

    # Then perform the string replacements
    data_copy[column_name] = data_copy[column_name].str.replace('R$ ', '', regex=False)
    data_copy[column_name] = data_copy[column_name].str.replace('.', '', regex=False).str.replace(',', '.', regex=False)

    # Convert to numeric
    data_copy[column_name] = pd.to_numeric(data_copy[column_name], errors='coerce')

    return data_copy
