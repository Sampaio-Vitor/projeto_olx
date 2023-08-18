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
        self.options.add_argument("--headless")
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument('--ignore-ssl-errors')
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(options=self.options)
        self.seen_links = set()
        
    def fetch_data_from_page(self, url):
        self.driver.get(url)
        WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h2[class="horizontal title sc-ifAKCX hUnWqk"]')))
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')

        links = soup.find_all('a', attrs={'data-ds-component': 'DS-NewAdCard-Link'})
        dates = soup.find_all('p', attrs={'data-ds-component': 'DS-Text', 'data-testid': 'ds-adcard-date'})

        data = []

        # Coletar todos os anúncios da página
        for link, date in zip(links, dates):
            if "Hoje" in date.text and link['href'] not in self.seen_links:
                self.seen_links.add(link['href'])  # Adicione o link ao conjunto de links vistos
                row = {
                    'link': link['href'],
                    'date': datetime.now()
                }
                data.append(row)


        # Ignorar os 4 primeiros anúncios impulsionados
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
                
                if not new_data:  # Break if we find an ad with "Ontem" or the page doesn't contain more data
                    break

                print(f"Scraping region: {region_name} - Page number: {page}")
                print(f"Length of DataFrame: {len(new_data)}")

                # Save after every page
                self.save_to_csv(new_data, region_name, mode='a')

                page += 1
                time.sleep(self.sleep_time)  # Pause for a few seconds between requests

        self.driver.quit()

if __name__ == "__main__":
    with open("config.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    
    scraper = LinkScraper(config)
    scraper.scrape_links()
