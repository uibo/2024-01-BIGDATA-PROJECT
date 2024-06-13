from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import numpy as np
import time

# element XPATH 모음
xpath_title = '//*[@id="root"]/div/div/div[4]/div[1]/div/div[2]/div/div[2]/div/div[1]/div[1]/div[1]'
xpath_context = '//*[@id="root"]/div/div/div[4]/div[1]/div/div[5]/div[1]/div/div[1]/div[2]/div[1]/p'
xpath_price = '//*[@id="root"]/div/div/div[4]/div[1]/div/div[2]/div/div[2]/div/div[1]/div[1]/div[2]/div[1]'
xpath_date = '//*[@id="root"]/div/div/div[4]/div[1]/div/div[2]/div/div[2]/div/div[1]/div[2]/div[1]/div/div[3]'
xpath_location = '//*[@id="root"]/div/div/div[4]/div[1]/div/div[5]/div[1]/div/div[1]/div[2]/div[2]/div[1]/div[2]/div/span'
xpath_condition = '//*[@id="root"]/div/div/div[4]/div[1]/div/div[2]/div/div[2]/div/div[1]/div[2]/div[2]/div' # + '/div[2]'
xpath_imgUrl = '//*[@id="root"]/div/div/div[4]/div[1]/div/div[2]/div/div[1]/div/div[1]/img[1]'
xpath_style = '//*[@id="root"]/div/div/div[4]/div/div/div[2]/div' # Productsstyle = [Product, SoldoutProduct, FailedProduct]
xpath_soldout = '//*[@id="root"]/div/div/div[4]/div[1]/div/div[2]/div[1]/a'

# Chrome driver 옵션 설정
chrome_options = Options()
chrome_options.add_argument("--headless")  # GUI 없이 실행
chrome_options.add_argument("--no-sandbox")  # 샌드박스 모드 비활성화
chrome_options.add_argument("--disable-dev-shm-usage")  # /dev/shm 사용 비활성화
chrome_options.add_argument("--log-level=3") # 로그 수준을 낮춰 warning message 출력 제한

# element CSV 파일에 저장
def data_acq(status, url):
    title = driver.find_element(By.XPATH, xpath_title).text
    context = driver.find_element(By.XPATH, xpath_context).text
    price = driver.find_element(By.XPATH, xpath_price).text
    upload_date = driver.find_element(By.XPATH, xpath_date).text
    location = driver.find_element(By.XPATH, xpath_location).text
    # condition 기재되지 않은 상품 존재
    if driver.find_element(By.XPATH, xpath_condition).get_attribute('style') == 'height: 18px;':
        condition = '-'
    else:
        condition = driver.find_element(By.XPATH, xpath_condition + '/div[2]').text
    imgUrl = driver.find_element(By.XPATH, xpath_imgUrl).get_attribute('src')
    # 번개장터 가격: 000,000원 -> 가격: 000000 으로 변환
    price = int(price[:-1].replace(',', ''))
    # 번개장터 날짜: 11달 전 -> 2024.05.26 으로 변환
    ago = upload_date[-3:]
    now = datetime.now()
    if ago == "분 전":
        n = int(upload_date[:-3])
        upload_date = (now - relativedelta(minutes=n)).date().strftime('%Y.%m.%d')
    elif ago == "간 전":
        n = int(upload_date[:-4])
        upload_date = (now - relativedelta(hours=n)).date().strftime('%Y.%m.%d')
    elif ago == "일 전":
        n = int(upload_date[:-3])
        upload_date = (now - relativedelta(days=n)).date().strftime('%Y.%m.%d')
    elif ago == "주 전":
        n = int(upload_date[:-3])
        upload_date = (now - relativedelta(weeks=n)).date().strftime('%Y.%m.%d')
    elif ago == "달 전":
        n = int(upload_date[:-3])
        upload_date = (now - relativedelta(months=n)).date().strftime('%Y.%m.00')
    elif ago == "년 전":
        n = int(upload_date[:-3])
        upload_date = (now - relativedelta(years=n)).date().strftime('%Y.00.00')
    else:
        upload_date = ''

    data = []
    data.append({
        'title' : title,
        'context' : context,
        'price' : price,
        'upload_date' : upload_date,
        'location' : location,
        'status' : status,
        'imgUrl' : imgUrl,
        'url': url,
        'condition' : condition
    })

    df = pd.DataFrame(data)
    # 제품이름_bunjang.csv
    df.to_csv('iphone13_bunjang.csv', index=False, mode='a', header=False)

f = open('iphone13_bunjang_urls.txt', 'r') # 제품 URL 모음 txt 파일
driver = webdriver.Chrome(options=chrome_options)

i = 0
while True:
    url = f.readline()
    if url == '': break
    driver.get(url)
    driver.implicitly_wait(90)

    i += 1
    print(i)
    try:
        # 삭제된 게시글 passing 및 status 구별
        style = driver.find_element(By.XPATH, xpath_style).get_attribute('class')
        if style == 'Productsstyle__FailedProductWrapper-sc-13cvfvh-32 fNIjUb':
            continue
        elif style == 'Productsstyle__SoldoutProductWrapper-sc-13cvfvh-33 ewWeeg':
            status = 1 # 1 = 판매완료
            url_ = driver.find_element(By.XPATH, xpath_soldout).get_attribute('href')
            driver.get(url_)
            data_acq(status, url_)
        else:
            status = 0 # 0 = 판매 중
            data_acq(status, url)
    except Exception as e:
        print(f"{e}\nRestart after 2 seconds")
        time.sleep(2)
        # 삭제된 게시글 passing 및 status 구별
        style = driver.find_element(By.XPATH, xpath_style).get_attribute('class')
        if style == 'Productsstyle__FailedProductWrapper-sc-13cvfvh-32 fNIjUb':
            continue
        elif style == 'Productsstyle__SoldoutProductWrapper-sc-13cvfvh-33 ewWeeg':
            status = 1  # 1 = 판매완료
            url_ = driver.find_element(By.XPATH, xpath_soldout).get_attribute('href')
            driver.get(url_)
            data_acq(status, url_)
        else:
            status = 0  # 0 = 판매 중
            data_acq(status, url)

f.close()
driver.quit()
