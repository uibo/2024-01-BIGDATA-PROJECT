#!/usr/bin/env python3
from bs4 import BeautifulSoup
import re
html = """
<ul>
    <li><a href="hoge.html">hoge</li>
    <li><a href="https://example.com/fuga">fuga*</li>
    <li><a href="https://example.com/foo">foo*</li>
    <li><a href="http://example.com/aaa">aaa</li>
</ul>
"""

soup = BeautifulSoup(html, "html.parser")
href = re.compile(r"^https://")

atags = soup.find_all("a")


for atag in atags:
    ahref = atag.attrs['href']
    if (href.match(ahref)):
        print(ahref)
        print(atag.string)
