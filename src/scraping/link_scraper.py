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

class LinkScraper:
    
    def __init__(self, config):
        self.regions = config['scraper']['regions']
        self.csv_filename = config['scraper']['csv_filename']
        self.sleep_time = config['scraper']['sleep_time']
        self.options = Options()
        #self.options.add_argument("--headless")
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument('--ignore-ssl-errors')
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(options=self.options)
        self.seen_links = set()
        
    def fetch_data_from_page(self, url):
        self.driver.get(url)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')

        data = []

        try:
            links_elements = self.driver.find_elements(By.XPATH, '//*[@id="main-content"]/div[16]/section/a')
            links = [link_elem.get_attribute('href') for link_elem in links_elements]

            dates_elements = self.driver.find_elements(By.XPATH, '//*[@id="main-content"]/div[15]/section/div[2]/div[2]/div/div[2]/p[2]')
            dates = [date_elem.text for date_elem in dates_elements]

            for link, date in zip(links, dates):
                print(f"Found link: {link} with date: {date}")  # Debug print
                if "Hoje" in date and link not in self.seen_links:
                    self.seen_links.add(link)
                    row = {
                        'link': link,
                        'date': datetime.now()
                    }
                    data.append(row)
        except Exception as e:
            print(f"Error while scraping page {url}: {e}")

        return data[4:]

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
