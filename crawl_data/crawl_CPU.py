import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
import warnings
import argparse
from tqdm import tqdm
import os
warnings.filterwarnings('ignore')

# parser = argparse.ArgumentParser()

# parser.add_argument('--chrome_driver_path', type=str, default=os.path.join(os.path.expanduser("~"), "chromedriver", "113", "chromedriver"), help='path to chrome driver')
# parser.add_argument('--sample_size', type=int, default=10000, help='number of sample to crawl')
# parser.add_argument('--input_file_path', type=str, default='laptop_detail.csv', help='path to file input that contain basic data')

# args = parser.parse_args()

# bar = tqdm(total=args.sample_size)


# Khởi tạo trình điều khiển cho Chrome
driver = webdriver.Chrome('chromedriver.exe')

df = pd.DataFrame(columns=['Rank', 'CPU', 'Cinebench23'])


# Mở trang web cần lấy dữ liệu
url = 'https://laptopmedia.com/top-laptop-cpu-ranking/'
driver.get(url)
# wait for page to load completely
time.sleep(15)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')


tbody = soup.find('tbody')
# save tbody to html file

    
for tr in tbody.find_all(
        'tr', class_='cpu-row w-full grid text-left px-2 py-3 items-center justify-start gap-x-2'):
    try:
        detail = {}
        td = tr.find_all('td')
        detail['Rank'] = td[0].text
        detail['CPU'] = td[1].text
        detail['Cinebench23'] = td[2].text
        df = pd.concat([df, pd.DataFrame([detail])], ignore_index=True)
    except Exception as e:
        print('Error: ', e)
        pass


driver.quit()
df.to_csv('raw/cpuben.csv', index=False)
print("Crawl CPU Done")
# print df size
print("Data shape:", df.shape)
