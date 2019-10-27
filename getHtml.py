#https://qiita.com/matsu0238/items/edf7dbba9b0b0246ef8f
import csv
import requests
from bs4 import BeautifulSoup

uri = 'https://kabuoji3.com/stock/'
num = ['9101', '9104', '9107']

dic = dict()
for i in num:
    l = list()
    d = list()
    url = uri + i + '/'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    tr = soup.find_all('tr')[1]
    td = tr.find_all('td')
    l.append(td)
    for j in l:
        for k in j:
            d.append(k.text)
    dic[i] = d

#print(dic)%exit()

filepath = './9104_2019.csv'
with open(filepath, 'a') as f:
    writer = csv.writer(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL)
    writer.writerow(dic['9104'])
    #print(dic['9104'], file=f)


