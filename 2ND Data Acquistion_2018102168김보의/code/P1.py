#!/usr/bin/env python3
import sys
import urllib.request
import urllib.parse

if len(sys.argv) <= 1:
    print("USAGE : download-forecast-argv <Region Number>")
    sys.exit()
regionNumber = sys.argv[1]

url = "http://www.kma.go.kr/weather/forecast/mid-term-rss3.jsp?stnId=" + str(regionNumber)
res = urllib.request.urlopen(url)
data = res.read()

text = data.decode("utf-8")
print(url)
print(text)