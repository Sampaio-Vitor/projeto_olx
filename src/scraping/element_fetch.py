from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import numpy as np
import yaml
from utils.utils import find_content_by_regex, extract_apartment_details, extract_parking_spots, extract_baths, extract_rooms, extract_area, extract_tax, extract_condo, extract_neighborhood, extract_cep, page_not_found, extract_price_using_xpath, extract_title_using_xpath
import re
from selenium.common.exceptions import NoSuchElementException
import os
import csv
from fake_useragent import UserAgent

ua = UserAgent()

output_path = 'data/dados_detalhados_olx.csv'
file_exists = os.path.isfile(output_path)

if not file_exists:
    with open(output_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['LINK','TITLE', 'PRICE', 'CEP', 'NEIGHBORHOOD', 'CONDO', 'TAX', 'AREA', 'ROOMS_NO', 'BATH_NO', 'PARKING_SPOTS', 'APARTMENT_DETAILS','REGION', 'CITY', 'DATE_SCRAPE'])
        writer.writeheader()

if __name__ == "__main__":
    with open('config.yaml', 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    # Set Chrome options
    options = Options()
    options.add_argument("--headless")  # Uncomment this if you want to run Chrome in headless mode
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument(f"user-agent={ua.random}")


    # Set up the Selenium driver with the options
    driver = webdriver.Chrome(options=options)
    # Load links from CSV
    df = pd.read_csv('data/new_links_olx.csv')

    prices = []
    ceps = []
    neighborhoods = []
    condos = []
    taxes = []
    areas = []
    rooms_numbers = []
    bath_numbers = []
    parking_spots_list = []
    apartment_details_list = []
    titles = []



    for link in df['link']:
        driver.get(link)

        # Check for the "Page not found" message
        if page_not_found(driver):
            print(f"Skipping URL {link} because page not found.")
            continue
        
        # Wait for the page to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        
        # Extract price using the refined regex pattern
        regex_pattern = r'R\$ (\d{1,3}(?:\.\d{3})+)'
        price_matches = find_content_by_regex(driver, regex_pattern)
        
        price = extract_price_using_xpath(driver)
        if price:
            prices.append(price)
            #print(f"Found price: {price} for link: {link}")
        else:
            prices.append(None)
        
        title = extract_title_using_xpath(driver)
        titles.append(title if title else np.nan)  
        
            # Extract CEP
        cep = extract_cep(driver)
        #if cep:
            #print(f"Found CEP: {cep} for link: {link}")
        ceps.append(cep)

            # Extract Neighborhood
        neighborhood = extract_neighborhood(driver)
        #if neighborhood:
            #print(f"Found Neighborhood: {neighborhood} for link: {link}")
        neighborhoods.append(neighborhood)
            # Extract Condo
        condo = extract_condo(driver)
        #if condo:
            #print(f"Found Condo: {condo} for link: {link}")
        condos.append(condo)

        # Extract Tax
        tax = extract_tax(driver)
        #if tax:
            #print(f"Found Tax: {tax} for link: {link}")
        taxes.append(tax)

            # Extract Area
        area = extract_area(driver)
        #if area:
            #print(f"Found Area: {area} for link: {link}")
        areas.append(area)

        # Extract Rooms Number
        rooms_no = extract_rooms(driver)
        #if rooms_no:
            #print(f"Found Rooms Number: {rooms_no} for link: {link}")
        rooms_numbers.append(rooms_no)

        # Extract Bath Number
        bath_no = extract_baths(driver)
        #if bath_no:
            #print(f"Found Bath Number: {bath_no} for link: {link}")
        bath_numbers.append(bath_no)

        # Extract Parking Spots
        parking_spots = extract_parking_spots(driver)
        #if parking_spots:
            #print(f"Found Parking Spots: {parking_spots} for link: {link}")
        parking_spots_list.append(parking_spots)

        # Extract Apartment Details
        apt_details = extract_apartment_details(driver)
        #if apt_details:
            #print(f"Found Apartment Details: {apt_details} for link: {link}")
        apartment_details_list.append(apt_details)
        
        #Extract region from original df
        region = df[df['link'] == link]['REGION'].iloc[0]



        data = {    
        'LINK': link,
        'TITLE': titles,
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
        'DATE_SCRAPE': datetime.now()  # Adjust if you have another method of capturing the scrape date
        }

        # Append the data to the CSV
        with open(output_path, 'a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=data.keys())
            writer.writerow(data)


    driver.quit()

