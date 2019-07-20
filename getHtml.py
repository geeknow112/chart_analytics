#https://qiita.com/matsu0228/items/edf7dbba9b0b0246ef8f
import requests
from bs4 import BeautifulSoup

url = 'https://info.finance.yahoo.co.jp/search/?query=%E5%95%86%E8%88%B9%E4%B8%89%E4%BA%95'

r = requests.get(url)
soup = BeautifulSoup(r.text, 'lxml')

for a in soup.find_all('a'):
    print(a.get('href'))
