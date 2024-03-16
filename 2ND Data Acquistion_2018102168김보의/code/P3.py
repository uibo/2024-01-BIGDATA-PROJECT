#!usr/bin/env python3
from bs4 import BeautifulSoup
import urllib.request
import ssl
import datetime


now = datetime.datetime.now().replace(microsecond=0)
now = now.strftime("%Y-%m-%d %H:%M:%S")

url = "https://finance.naver.com/marketindex/"
res = urllib.request.urlopen(url)
data = res.read()

soup = BeautifulSoup(data, 'html.parser')
price = (soup.select_one('#exchangeList > li.on > a.head.usd > div > span.value')).string


print("DATE: " + now + " 미국 USD: " + price)