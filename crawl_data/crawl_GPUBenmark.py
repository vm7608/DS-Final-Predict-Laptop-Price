import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
import warnings
warnings.filterwarnings('ignore')

# Khởi tạo trình điều khiển cho Chrome
driver = webdriver.Chrome('chromedriver.exe')

df = pd.DataFrame(columns=['Rank', 'GPU', '3DMark Time Spy (G)'])


# Mở trang web cần lấy dữ liệu
url = 'https://laptopmedia.com/top-laptop-graphics-ranking/'
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
        detail['GPU'] = td[1].text
        detail['3DMark Time Spy (G)'] = td[2].text
        df = pd.concat([df, pd.DataFrame([detail])], ignore_index=True)
    except Exception as e:
        print('Error: ', e)
        pass


driver.quit()
df.to_csv('gpuben.csv', index=False)
print("Done")
# print df size
print(df.shape)
