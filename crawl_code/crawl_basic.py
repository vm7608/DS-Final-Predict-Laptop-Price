import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
import warnings
from tqdm import tqdm
import argparse
import os
warnings.filterwarnings('ignore')

parser = argparse.ArgumentParser()

parser.add_argument('--chrome_driver_path', type=str, default=os.path.join(os.path.expanduser("~"), "chromedriver", "113", "chromedriver"), help='path to chrome driver')
parser.add_argument('--sample_size', type=int, default=10, help='number of sample to crawl')
parser.add_argument('--out', type=str, default='raw/laptop_basic.csv', help='output file path')

args = parser.parse_args()

# Khởi tạo trình điều khiển cho Chrome
driver = webdriver.Chrome(args.chrome_driver_path)
bar = tqdm(total = args.sample_size)
page = 100
df = pd.DataFrame(columns=['Product Name', 'Product Link'])


def crawl(sample_size, df):
    total_sample = 0
    for i in range(1, page+1):
        # Mở trang web cần lấy dữ liệu
        # url = 'https://laptopmedia.com/specs/?size=n_100_n'
        url = f'https://laptopmedia.com/specs/?current=n_{i}_n&size=n_100_n'
        driver.get(url)
        # wait for page to load completely
        time.sleep(5)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        for li in soup.find_all(
                'li', class_='flex items-center gap-2 list-none border-b py-1 mb-2'):
            try:
                if total_sample == sample_size:
                    return df
                detail = {}
                detail['Product Name'] = li.find('h2').text
                detail['Product Link'] = li.find('a')['href']
                dt = li.find_all('dt')
                dd = li.find_all('dd')
                for i in range(len(dt)):
                    detail[dt[i].text] = dd[i].text

                detail['Price'] = li.find('span', class_='text-lm-darkBlue').text
                # detail['SupPrice'] = li.find('sup').text
                # df = df.append(detail, ignore_index=True)
                df = pd.concat((df, pd.DataFrame(detail, index=[0])), ignore_index=True)
                bar.update(1)
                total_sample+=1
            except:
                print('Error')
                pass

        # save data to csv file
        # Đóng trình duyệt
        # print(f'Page {i} done')
        time.sleep(5)
    driver.quit()

df = crawl(args.sample_size, df)
df.to_csv(args.out, index=False)


print("Crawl Basic Done")
# print df size
print("Data shape:", df.shape)
