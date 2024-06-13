from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import pandas as pd
import numpy as np

driver = webdriver.Chrome()
product_urls = open("iphone_daangn_urls.txt", "w") # 제품 이름_daangn_urls.txt

# range 1000페이지까지만 존재
for i in range(1, 1001):
    # 제품 url - 현재 아이폰
    url = f'https://www.daangn.com/search/%EC%95%84%EC%9D%B4%ED%8F%B0/more/flea_market?next_page={i}'
    driver.get(url)
    driver.implicitly_wait(100)
    for j in range(1, 7): # 당근마켓 1페이지당 6개 제품
        link_xpath = f'/html/body/article[{j}]/a'
        link = driver.find_element(By.XPATH, link_xpath)
        product_link = link.get_attribute("href")
        product_urls.write(product_link + '\n')
        print(f"{(i - 1) * 6 + j}번째 제품 완료")
        driver.implicitly_wait(100)

driver.quit()
product_urls.close()
