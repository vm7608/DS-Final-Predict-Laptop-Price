import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
import warnings
warnings.filterwarnings('ignore')

# Khởi tạo trình điều khiển cho Chrome
driver = webdriver.Chrome('chromedriver.exe')
page = 100
df = pd.DataFrame(columns=['Product Name', 'Product Link'])


for i in range(1, page+1):
    # Mở trang web cần lấy dữ liệu
    # url = 'https://laptopmedia.com/specs/?size=n_100_n'
    url = f'https://laptopmedia.com/specs/?current=n_{i}_n&size=n_100_n'
    driver.get(url)
    # wait for page to load completely
    time.sleep(15)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    for li in soup.find_all(
            'li', class_='flex items-center gap-2 list-none border-b py-1 mb-2'):
        try:
            detail = {}
            detail['Product Name'] = li.find('h2').text
            detail['Product Link'] = li.find('a')['href']
            dt = li.find_all('dt')
            dd = li.find_all('dd')
            for i in range(len(dt)):
                detail[dt[i].text] = dd[i].text

            detail['Price'] = li.find('span', class_='text-lm-darkBlue').text
            # detail['SupPrice'] = li.find('sup').text
            df = df.append(detail, ignore_index=True)
        except:
            print('Error')
            pass

    # save data to csv file
    # Đóng trình duyệt
    print(f'Page {i} done')
    time.sleep(15)
    
driver.quit()
df.to_csv('laptop_basic.csv', index=False)
print("Done")
# print df size
print(df.shape)