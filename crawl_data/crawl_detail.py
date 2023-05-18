#%%
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
import warnings
warnings.filterwarnings('ignore')
import os
from threading import Thread, Barrier
import logging
import argparse
parser = argparse.ArgumentParser()

parser.add_argument('--chrome_driver_path', type=str, default=os.path.join(os.path.expanduser("~"), "chromedriver", "113", "chromedriver"), help='path to chrome driver')
parser.add_argument('--sample_size', type=int, default=10000, help='number of sample to crawl')
parser.add_argument('--number_of_threads', type=int, default=20, help='number of threads to crawl')

args = parser.parse_args()

CHROME_DRIVER_PATH = args.chrome_driver_path  # use your chrome driver path

#%%
logger = logging.getLogger()
logger.setLevel(logging.INFO)
# ensure crawl_detail.log is empty or not exist before run
file_handler = logging.FileHandler('crawl_detail.log')
file_handler.setLevel(logging.INFO)
logger.addHandler(file_handler)



#%%
def crawl_detail(details, offset, limit):
    """offset start from 0""" 
    opts = webdriver.ChromeOptions()
    opts.headless = True
    browser_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.30'
    opts.add_argument(f'user-agent={browser_agent}')
    driver = webdriver.Chrome(CHROME_DRIVER_PATH, options=opts)
    for i in range(offset, offset + limit if offset + limit < len(details) else len(details)):
        url = details[i]['Product Link']
        logger.info(f'Working on {url=}, {i=}')
        driver.get(url)
        time.sleep(5)
        detail_soup = BeautifulSoup(driver.page_source, 'html.parser')
        price_tag = detail_soup.find('a', {'class': "group bg-lm-darkOrange hover:bg-lm-darkBlue rounded-md text-white text-center cursor-pointer flex xl:flex-col xl:h-24"})
        if price_tag:
            p1 = price_tag.find('span').text
            p2 = price_tag.find('sup').tet
            details[i]['Detail price'] = f'{p1}.{p2}'
        for div in detail_soup.find_all('div', {'class': 'lm-gpu-model'}):
            details[i][div.find('ul').find('li').text] = div.find('ul').find('li').find_next('li').text
        feature_label = detail_soup.find('li', {'class': 'font-bold w-max'}, text='Features')
        if not feature_label:
            continue
        container = feature_label.parent.parent
        for ul in container.find_all('ul'):
            details[i][ul.find('li').text] = ul.find('li').find_next('li').text
        logger.info(f'Done {url=}, {i=}')
    logger.info(f'Done {offset=}, {limit=}')
    driver.quit()

#%%

if __name__ == '__main__':
    
    df = pd.read_csv('laptop_basic.csv')
    # convert df to dictionary
    details = df.to_dict('records')

    sample_size = args.sample_size
    if sample_size != 10000:
        number_of_threads = args.number_of_threads
        limit_each_thread = sample_size // number_of_threads
        limit_first_thread = limit_each_thread + sample_size % number_of_threads
        threads = []
        for i in range(number_of_threads):
            if i == 0:
                t = Thread(target=crawl_detail, args=(details, i*limit_each_thread, limit_first_thread))
            else:
                t = Thread(target=crawl_detail, args=(details, i*limit_each_thread, limit_each_thread))
            t.start()
            threads.append(t)
        for t in threads:
            t.join()
        df = pd.DataFrame(details[:sample_size])
        df.to_csv(f'laptop_detail_{sample_size}_sample.csv')
    
    else: 
        if not os.path.exists('.crawl_cache'):
            os.mkdir('.crawl_cache')

        for part in range(100):
            if os.path.exists(f'.crawl_cache/{part}.csv'):
                continue
            number_of_threads = args.number_of_threads
            threads = []
            for i in range(number_of_threads):
                # modify offset and limit if change number_of_threads
                # a part must working on 100 item, so for example if you change number_of_thread to 5, the offset must change to i*20, and limit = 20
                t = Thread(target=crawl_detail, args=(details, part*100 + i*5, 5)) 
                t.start()
                threads.append(t)
            for t in threads:
                t.join()
            part_data = pd.DataFrame(details[part*100:part*100 + 100])
            part_data.to_csv(f'.crawl_cache/{part}.csv')

        csvs = os.listdir('.crawl_cache')
        csvs.sort(key=lambda x: int(x.split('.')[0]))
        csvs = list(map(lambda x: os.path.join('.','.crawl_cache', x), csvs))
        df = pd.read_csv(csvs[0])
        for file in csvs[1:]:
            df = pd.concat([df, pd.read_csv(file)])
        df.to_csv('laptop_detail.csv')
