from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import time
import warnings
import re
import os
import yaml

warnings.filterwarnings('ignore')

class DataScraper:

    def __init__(self, config):
        self.links_filename = os.path.join('data', config['scraper']['links_filename'])
        self.detailed_filename = os.path.join('data', config['scraper']['detailed_filename'])
        self.sleep_time = config['scraper']['sleep_time']
        self.options = Options()
        self.options.add_argument("--headless")
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument('--ignore-ssl-errors')
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(options=self.options)
        self.error_count = 0

    def fetch_data_from_ad(self, url, region):
        try:
            self.driver.get(url)
            WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h1[class="ad__sc-45jt43-0 htAiPK sc-hSdWYo bYQcLm"]')))
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')

            # Your existing scraping logic
            all_spans = soup.find_all('span', {'class': 'ad__sc-1f2ug0x-1 cpGpXB sc-hSdWYo gwYTWo'})
            details = soup.find('span', text=re.compile('Detalhes do imóvel'))
            rooms_elem = soup.find('span', text='Quartos')
            rooms_no = rooms_elem.find_next_sibling('div').a.text if rooms_elem and rooms_elem.find_next_sibling('div') else 'N/A'
            price_text = soup.find_all('h2', {'class': 'ad__sc-12l420o-1 haeKsn sc-hSdWYo grMlBs'})[1].text.replace('.', '')
            price = int(price_text) if price_text != 'N/A' else None

            data = {
                'TITLE': soup.find('h1', {'class': 'ad__sc-45jt43-0 htAiPK sc-hSdWYo bYQcLm'}).text,
                'LINK': url,
                'DATE_SCRAPE': datetime.today().strftime('%Y-%m-%d'),
                'CEP': all_spans[0].text if len(all_spans) > 0 else 'N/A',
                'CITY': all_spans[1].text if len(all_spans) > 1 else 'N/A',
                'NEIGHBORHOOD': all_spans[2].text if len(all_spans) > 2 else 'N/A',
                'CONDO': all_spans[4].text if len(all_spans) > 4 else 'N/A',
                'TAX': all_spans[5].text if len(all_spans) > 5 else 'N/A',
                'AREA': all_spans[6].text if len(all_spans) > 6 else 'N/A',
                'ROOMS_NO': rooms_no,
                'BATH_NO': all_spans[7].text if len(all_spans) > 7 else 'N/A',
                'PARKING_SPOTS': all_spans[8].text if len(all_spans) > 8 else 'N/A',
                'APARTMENT_DETAILS': details.find_next_sibling().text if details and details.find_next_sibling() else 'N/A',
                'PRICE': price,
                'REGION': region
            }
            return data

        except TimeoutException:
            print(f"TimeoutException occurred for URL: {url}. Moving on to the next link.")
            self.error_count += 1
            return {}

    def scrape_data(self):
        # Load links from CSV
        df_links = pd.read_csv(self.links_filename)

        all_data = []

        for _, row in df_links.iterrows():
            url = row['link']
            region = row['REGION']

            data = self.fetch_data_from_ad(url, region)
            if data:
                all_data.append(data)  # Use a list to store data

            time.sleep(self.sleep_time)

        df_detailed = pd.DataFrame(all_data)  # Convert list to DataFrame
        df_detailed.to_csv(self.detailed_filename, index=False)

    def quit_driver(self):
        self.driver.quit()

if __name__ == "__main__":
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    scraper = DataScraper(config)
    scraper.scrape_data()
    scraper.quit_driver()
    print(f"Scraping completed with {scraper.error_count} errors.")
