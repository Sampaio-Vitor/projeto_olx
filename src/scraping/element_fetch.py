from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import numpy as np
import yaml
import boto3
import io
from io import StringIO
from selenium.common.exceptions import TimeoutException
import os

#import sys
#sys.path.append('C:\\Users\\vitor\\OneDrive\\Área de Trabalho\\projetos\\projeto_olx')

s3 = boto3.client('s3',
                  aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
                  aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
                  region_name=os.environ.get('AWS_REGION', 'sa-east-1'))

bucket_name = 'bucketolx'

from src.utils.utils import (find_content_by_regex, extract_apartment_details, extract_parking_spots, 
                         extract_baths, extract_rooms, extract_area, extract_tax, extract_condo, 
                         extract_neighborhood, extract_cep, page_not_found, extract_price_using_xpath, 
                         extract_title_using_xpath)
import os
import csv
from fake_useragent import UserAgent

# Função para salvar no S3
def save_to_s3(df, file_name):
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    s3.put_object(Body=csv_buffer.getvalue(), Bucket=bucket_name, Key=file_name)

# Função para ler do S3
def read_from_s3(file_name):
    obj = s3.get_object(Bucket=bucket_name, Key=file_name)
    return pd.read_csv(io.BytesIO(obj['Body'].read()))
  
ua = UserAgent()

output_path = 'data/dados_detalhados_olx.csv'
file_exists = os.path.isfile(output_path)

if not file_exists:
    with open(output_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['LINK', 'TITLE', 'PRICE', 'CEP', 'NEIGHBORHOOD', 'CONDO', 
                                                  'TAX', 'AREA', 'ROOMS_NO', 'BATH_NO', 'PARKING_SPOTS', 
                                                  'APARTMENT_DETAILS', 'REGION', 'CITY', 'DATE_SCRAPE'])
        writer.writeheader()
      
existing_data = read_from_s3('data/dados_detalhados_olx.csv')

scraped_data = pd.DataFrame(columns=['LINK', 'TITLE', 'PRICE', 'CEP', 'NEIGHBORHOOD', 'CONDO', 
                                         'TAX', 'AREA', 'ROOMS_NO', 'BATH_NO', 'PARKING_SPOTS', 
                                         'APARTMENT_DETAILS', 'REGION', 'CITY', 'DATE_SCRAPE'])


if __name__ == "__main__":
    with open('config.yaml', 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    options = Options()
    options.add_argument("--headless")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument(f"user-agent={ua.random}")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    
    driver = webdriver.Chrome(options=options)
    df = read_from_s3('data/new_links_olx.csv')
    df = df[df['is_new'] == 1]

    for index, row in df.iterrows():
        link = row['link']
        try:
            driver.get(link)
        except TimeoutException:
            print(f"Timeout while loading {link}. Moving to the next link.")
            continue


        if page_not_found(driver):
            print(f"Skipping URL {link} because page not found.")
            continue
        
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        
        price = extract_price_using_xpath(driver)
        print(price)
        title = extract_title_using_xpath(driver)
        cep = extract_cep(driver)
        print(cep)
        neighborhood = extract_neighborhood(driver)
        print(neighborhood)
        condo = extract_condo(driver)
        print(condo)
        tax = extract_tax(driver)
        print("tax = " + " " +tax)
        area = extract_area(driver)
        print(area)
        rooms_no = extract_rooms(driver)
        print(rooms_no)
        bath_no = extract_baths(driver)
        print (bath_no)
        parking_spots = extract_parking_spots(driver)
        print(parking_spots)
        apt_details = extract_apartment_details(driver)
        print(apt_details)
        region = df[df['link'] == link]['REGION'].iloc[0]

        data = {    
            'LINK': link,
            'TITLE': title,
            'PRICE': price,
            'CEP': cep,
            'NEIGHBORHOOD': neighborhood,
            'CONDO': condo,
            'TAX': tax,
            'AREA': area,
            'ROOMS_NO': rooms_no,
            'BATH_NO': bath_no,
            'PARKING_SPOTS': parking_spots,
            'APARTMENT_DETAILS': apt_details,
            'REGION': region,
            'CITY': "Belo Horizonte",
            'DATE_SCRAPE': datetime.now()
        }
      
        scraped_data = pd.concat([scraped_data, pd.DataFrame([data])], ignore_index=True)

        # After scraping details of the link successfully, mark it as not new
        df.at[index, 'is_new'] = 0
      
    combined_data = pd.concat([existing_data, scraped_data], ignore_index=True)

    # Save the updated DataFrame back to the csv after the loop
    df.to_csv('data/new_links_olx.csv', index=False)
    save_to_s3(df, 'data/new_links_olx.csv')
    save_to_s3(combined_data, 'data/dados_detalhados_olx.csv')

    driver.quit()
