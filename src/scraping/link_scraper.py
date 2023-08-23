from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import time
import yaml
import os
import re

class LinkScraper:
    
    def __init__(self, config):
        self.regions = config['scraper']['regions']
        self.csv_filename = config['scraper']['csv_filename']
        self.sleep_time = config['scraper']['sleep_time']
        self.links_per_region = 50 #Just for collecting the 50 first as a baseline
        self.options = Options()
        self.options.add_argument("--headless")
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument('--ignore-ssl-errors')
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(options=self.options)
        self.seen_links = set()
        
    def fetch_data_from_page(self, url):
        self.driver.get(url)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        
        page_source = self.driver.page_source

        # Using regex to find all links starting with the pattern
        link_pattern = r'https://mg\.olx\.com\.br/belo-horizonte-e-regiao/imoveis/[a-zA-Z0-9\-]+'
        found_links = list(set(re.findall(link_pattern, page_source)))

        data = []

        for link in found_links:
            if link not in self.seen_links:
                self.seen_links.add(link)
                row = {
                    'link': link,
                    'date': datetime.now()
                }
                data.append(row)

        return data

    def save_to_csv(self, data, region, mode='w'):
        df = pd.DataFrame(data)
        df['REGION'] = region
        df.to_csv(self.csv_filename, mode=mode, header=not os.path.exists(self.csv_filename), index=False)

    def scrape_links(self):
        for region in self.regions:
            page = 1
            region_name = region['name']
            base_url = region['url']
            
            while True:
                if page == 1:
                    url = base_url
                else:
                    url = f'{base_url}&o={page}'

                new_data = self.fetch_data_from_page(url)
                
                if not new_data:
                    break

                print(f"Scraping region: {region_name} - Page number: {page}")
                print(f"Length of DataFrame: {len(new_data)}")

                # Save after every page
                self.save_to_csv(new_data, region_name, mode='a')

                page += 1
                time.sleep(self.sleep_time)
                print(f"{len(new_data)} links found on this page.")

if __name__ == "__main__":
    with open("config.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    
    scraper = LinkScraper(config)
    scraper.scrape_links()
