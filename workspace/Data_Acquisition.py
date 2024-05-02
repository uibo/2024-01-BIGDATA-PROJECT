from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import pandas as pd
import numpy as np

url = "https://m.bunjang.co.kr/search/products?q=%EC%95%84%EC%9D%B4%ED%8F%B0%2014"
driver = webdriver.Chrome()
driver.get(url)
product_names= driver.find_elements(By.XPATH, '//*[@id="root"]/div/div/div[4]/div/div[4]/div/div//a/div[2]/div[1]')
prices = driver.find_elements(By.XPATH, '//*[@id="root"]/div/div/div[4]/div/div[4]/div/div//a/div[2]/div[2]')
regions = driver.find_elements(By.XPATH, '//*[@id="root"]/div/div/div[4]/div/div[4]/div/div//a/div[3]')

data = list()
for title, price_date, region in zip(product_names, prices, regions):
    temp = (price_date.text).split('\n')
    temp[0] = int(temp[0].replace(',',''))
    temp.insert(0,title.text)
    temp.append(region.text)
    data.append(tuple(temp))
driver.quit()

data = pd.DataFrame(data)
data.to_csv('./workspace/data/data.csv')
print("Data Accquisition finishing")










