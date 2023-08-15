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
        self.start_url = config['scraper']['start_url']
        self.csv_filename = config['scraper']['csv_filename']
        self.sleep_time = config['scraper']['sleep_time']
        self.options = Options()
        self.options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(options=self.options)
        
    def fetch_data_from_page(self, url):
        self.driver.get(url)
        WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h2[class="horizontal title sc-ifAKCX hUnWqk"]')))
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')

        titles = soup.find_all('h2', attrs={'class': 'horizontal title sc-ifAKCX hUnWqk'})
        links = soup.find_all('a', attrs={'data-ds-component': 'DS-NewAdCard-Link'})
        dates = soup.find_all('p', attrs={'data-ds-component': 'DS-Text', 'data-testid': 'ds-adcard-date'})

        data = []

        # Ignorar os 4 primeiros anúncios impulsionados
        for title, link, date in zip(titles[4:], links[4:], dates[4:]):
            if "Ontem" in date.text:
                return None
            
            row = {
                'titulo': title.text,
                'link': link['href'],
                'date': datetime.now()
            }

            data.append(row)

        return data


    def save_to_csv(self, data, mode='w'):
        df = pd.DataFrame(data)
        df.to_csv(self.csv_filename, mode=mode, header=not os.path.exists(self.csv_filename), index=False)
        
    def scrape_links(self):
        page = 1

        while True:
            if page == 1:
                url = f'{self.start_url}?sf=1'
            else:
                url = f'{self.start_url}?o={page}&sf=1'
            
            new_data = self.fetch_data_from_page(url)
            
            if not new_data:  # Se encontrarmos um anúncio de "Ontem"
                print("An ad from 'Yesterday' found. Exiting scraper.")
                break

            print(f"Page number: {page}")
            print(f"Length of DataFrame: {len(new_data)}")

            # Save after every page
            self.save_to_csv(new_data, mode='a')

            page += 1
            time.sleep(self.sleep_time)  # Pause for a few seconds between requests

        self.driver.quit()

if __name__ == "__main__":
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    scraper = LinkScraper(config)
    scraper.scrape_links()
