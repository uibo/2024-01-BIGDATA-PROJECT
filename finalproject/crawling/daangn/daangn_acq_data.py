from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import numpy as np
import time

# element XPATH 모음
xpath_title = '//*[@id="article-title"]'
xpath_context = '//*[@id="article-detail"]'
xpath_price = '/html/body/article/section[3]/p[5]'
xpath_date = '//*[@id="article-category"]/time'
xpath_location = '//*[@id="region-name"]'
xpath_noimg = '/html/body/article/section[1]'
xpath_imgslider = '/html/body/article/section[1]/div/div/div/div/div/div'
xpath_imgUrl1 = '//*[@id="slick-slide00"]/div/a/div/div/img'
xpath_imgUrl0 = '//*[@id="image-slider"]/div/div/div/div/div/div/a/div/div/img'


# element CSV 파일에 저장
def data_acq(status, url):
    price = driver.find_element(By.XPATH, xpath_price)
    # 나눔 제외
    if price.get_attribute('id') == 'article-price':
        title = driver.find_element(By.XPATH, xpath_title).text
        context = driver.find_element(By.XPATH, xpath_context).text
        price = price.text
        upload_date = driver.find_element(By.XPATH, xpath_date).text
        location = driver.find_element(By.XPATH, xpath_location).text
        # 이미지 없는 게시물 처리
        noimg = driver.find_element(By.XPATH, xpath_noimg).get_attribute('id')
        if noimg == 'article-images':
            img = driver.find_element(By.XPATH, xpath_imgslider).get_attribute('class')
            if img == 'slick-slide slick-cloned':
                imgUrl = driver.find_element(By.XPATH, xpath_imgUrl1).get_attribute('src')
            elif img == 'slick-slide slick-current slick-active':
                imgUrl = driver.find_element(By.XPATH, xpath_imgUrl0).get_attribute('src')
            else:
                imgUrl = ''
        else:
            imgUrl = ''
        # 당근마켓 가격: 000,000원, 000만원 -> 가격: 000000 으로 변환
        if price[-2:] == "만원":
            price = int(price[:-2].replace(',','')) * 10000
        elif price[-2:] == "억원":
            price = ''
        elif price[-1:] == "원":
            price = int(price[:-1].replace(',', '').replace('만 ','').replace('억 ',''))
        else:
            price = ''
        # 당근마켓 날짜: 11달 전 -> 2024.05.26 으로 변환
        ago = upload_date[-3:]
        now = datetime.now()
        if ago == "분 전":
            n = int(upload_date[:-3].replace('끌올 ',''))
            upload_date = (now - relativedelta(minutes=n)).date().strftime('%Y.%m.%d')
        elif ago == "간 전":
            n = int(upload_date[:-4].replace('끌올 ',''))
            upload_date = (now - relativedelta(hours=n)).date().strftime('%Y.%m.%d')
        elif ago == "일 전":
            n = int(upload_date[:-3].replace('끌올 ',''))
            upload_date = (now - relativedelta(days=n)).date().strftime('%Y.%m.%d')
        elif ago == "주 전":
            n = int(upload_date[:-3].replace('끌올 ',''))
            upload_date = (now - relativedelta(weeks=n)).date().strftime('%Y.%m.%d')
        elif ago == "달 전":
            n = int(upload_date[:-3].replace('끌올 ',''))
            upload_date = (now - relativedelta(months=n)).date().strftime('%Y.%m.00')
        elif ago == "년 전":
            n = int(upload_date[:-3].replace('끌올 ',''))
            upload_date = (now - relativedelta(years=n)).date().strftime('%Y.00.00')
        else:
            upload_date = ''

        data = [{
            'title': title,
            'context': context,
            'price': price,
            'upload_date': upload_date,
            'location': location,
            'status': status,
            'imgUrl': imgUrl,
            'url': url,
        }]
        df = pd.DataFrame(data)
        df.to_csv('iphone_daangn.csv', index=False, mode='a', header=False)  # 제품이름_daangn.csv


f = open('iphone_daangn_urls.txt', 'r') # 제품 URL 모음 txt 파일
driver = webdriver.Chrome()

i = 0
while True:
    url = f.readline()
    if url == '':
        break
    driver.get(url)
    driver.implicitly_wait(100)

    i += 1
    print(i)

    hide = driver.find_element(By.XPATH, '//*[@id="content"]').text
    if hide == '숨겨져 있는 게시글은 볼 수 없습니당 :(':
        continue
    elif hide == '게시글이 삭제되었거나 존재하지 않습니당 :(':
        continue
    nanum = driver.find_element(By.XPATH, "/html/body/article/section[2]").get_attribute('id')
    if nanum == 'article-profile':
        status = 0  # 0 = 판매 중, 당근마켓은 판매 중인 제품만 표시됨
        data_acq(status, url)

f.close()
driver.quit()
