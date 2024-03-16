#!/usr/bin/env python3
# coding: utf-8

from bs4 import BeautifulSoup
import requests

def main ():

    url = "https://www.kma.go.kr/weather/forecast/mid-term-rss3.jsp"
    res = requests.get(url)

    soup = BeautifulSoup(res.text, 'lxml')

    cities = soup.select("location")
    
    for city in cities:
        cityname = city.select_one('city').string
        date = city.select_one('data > tmef').string
        weather = city.select_one('data > wf').string
        print(f"[ {date} ] {cityname} : {weather}")


if __name__ == "__main__":
    main()





"""     cities = soup.find_all('location')

    for city in cities:
        date = city.findChild("tmef").string
        cityname = city.findChild('city').string
        weather = city.findChild('wf').string
        print(f"[ {date} ] {cityname} : {weather}")
 """