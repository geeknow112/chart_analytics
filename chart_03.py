import os as os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import mpl_finance as mpf
from pprint import pprint
import datetime as dt
import numpy as np
import talib

csv = "./9104_2019.csv"
#print(os.path.exists(csv))
#exit()

def DataRead():
    with open(csv, "r") as csv_file:
        df = pd.read_csv(csv_file, quotechar='"', header=2, index_col=0)
#exit()

with open(csv, 'r') as csv_file:
    df = pd.read_csv(csv_file, quotechar='"', header=1, index_col=0)

df_ = df.copy()

new = [dt.datetime.strptime(i, '%Y-%m-%d') for i in df_.index]
df_.index = [mdates.date2num(i) for i in new]
#pprint(df_.index)%exit()

'''
st = "2019-1-1"
d = dt.datetime.strptime(st, '%Y-%m-%d')
dtime = dt.datetime(d.year, d.month, d.day)
pprint(mdates.date2num(dtime))%exit()
'''

#df_.index = mdates.date2num(df_.index)
data = df_.reset_index().values

''''''
#https://qiita.com/toyolab/items/1b5d11b5d376bd542022
#https://qiita.com/kjybinp1105/items/db4efd07e20000c22f4e
#https://www.quantnews.com/bollinger-bands-backtest-using-python-rest-api-part-1/
#https://engineeringnote.hateblo.jp/entry/python/finance/bollinger_bands
#https://nerimplo.hatenablog.com/entry/2018/08/01/113000
#https://qiita.com/ConnieWild/items/cb50f36425a683c914d2

fig = plt.figure()
ax = plt.subplot()
fig.patch.set_facecolor('white')
fig.patch.set_alpha(0.5)
ax.patch.set_facecolor('black')
ax.patch.set_alpha(1.0)

ohlc = np.vstack((range(len(df)), df.values.T)).T
mpf.candlestick_ohlc(ax, ohlc, width=0.7, colorup='r', colordown='g')

w = dt.datetime.strptime(df.index[0], '%Y-%m-%d').weekday()
#pprint(w)%exit()

xtick0 = (5-w)%5
#pprint(xtick0)%exit()

#plt.xticks(range(xtick0,len(df),5), [x.strftime('%Y-%m-%d') for x in df.index][xtick0::5])
plt.xticks(range(xtick0,len(df),5), [dt.datetime.strptime(x, '%Y-%m-%d') for x in df.index][xtick0::5])

short_term = 5
long_term = 20

df['av_short'] = df['close'].rolling(window=short_term).mean()
df['av_long'] = df['close'].rolling(window=long_term).mean()

df['golden_flag'] = 0
current_flag=0
previous_flag=1
for i,price in df.iterrows():
    if(price['av_short']>price['av_long']):
        current_flag = 1
    else:
        current_flag = 0
    if(current_flag*(1-previous_flag)):
        df.loc[i,'golden_flag']=price['av_long']
    else:
        df.loc[i,'golden_flag']= None
    previous_flag = current_flag

#df.plot(style=['-'])

ax.plot(df.index, df['close'].rolling(5).mean(), color='r', label="Moving Ave(5)")
ax.plot(df.index, df['close'].rolling(20).mean(), color='g', label="Moving Ave(20)")
ax.plot(df.index, df['close'].rolling(60).mean(), color='b', label="Moving Ave(60)")
ax.plot(df.index, df['close'].rolling(75).mean(), color='y', label="Moving Ave(75)")
ax.plot(df.index, df['close'].rolling(100).mean(), color='orange', label="Moving Ave(100)")
ax.plot(df.index, df['close'].rolling(200).mean(), color='gold', label="Moving Ave(200)")
ax.plot(df.index, df['close'].rolling(300).mean(), color='pink', label="Moving Ave(300)")
#ax.plot(df.index, pd.Series(df['close']).rolling(5).mean(), color='g', label="Moving Ave(5)")
#plt.scatter(50, 2500, s=100, marker="o",color='gold')
plt.scatter(x= df.index,y = df['golden_flag'],marker='o',color='gold')


#BollingerBand
df.sort_index(ascending=True, inplace=True)
close = np.array(df['close'])
output = close.copy()
cols = ['close']

for arr in talib.BBANDS(df['close'], timeperiod=25, nbdevup=1, nbdevdn=1, matype=0): output = np.c_[output, arr]
cols += ['BBANDS_upperband', 'BBANDS_middleband', 'BBANDS_lowerband']
d1 = pd.DataFrame(output, index=df.index, columns=cols)
ax.plot(df.index, d1['BBANDS_upperband'], color='lightpink', label="bbands_upp_1")
ax.plot(df.index, d1['BBANDS_lowerband'], color='lightpink', label="bbands_low_1")

df.sort_index(ascending=True, inplace=True)
close = np.array(df['close'])
output = close.copy()
cols = ['close']

for arr in talib.BBANDS(df['close'], timeperiod=25, nbdevup=2, nbdevdn=2, matype=0): output = np.c_[output, arr]
cols += ['BBANDS_upperband', 'BBANDS_middleband', 'BBANDS_lowerband']
d2 = pd.DataFrame(output, index=df.index, columns=cols)
ax.plot(df.index, d2['BBANDS_upperband'], color='lightgreen', label="bbands_upp_2")
ax.plot(df.index, d2['BBANDS_lowerband'], color='lightgreen', label="bbands_low_2")
#pprint(d)%exit()

#grid
ax.grid()
ax.set_xlim(-1, len(df))
fig.autofmt_xdate()
''''''
#exit()
'''
fig = plt.figure(figsize=(12, 4))
ax = fig.add_subplot(1, 1, 1)

mpf.candlestick_ohlc(ax, data, width=1.0, alpha=1.0, colorup='r', colordown='g')
#ax.plot(df.index, df['close'].rolling(5).mean(),color='g',label="Moving Ave(5)")
#ax.plot(df.index, df['close'].rolling(25).mean(),color='m',label="Moving Ave(25)")
#ax.plot(df.index, df['close'].rolling(50).mean(),color='r',label="Moving Ave(50)")
#plt.scatter(x, y, s=100, marker="v",color='k')

ax.grid()
locator = mdates.AutoDateLocator()
ax.xaxis.set_major_locator(locator)
ax.xaxis.set_major_formatter(mdates.AutoDateFormatter(locator))
'''

plt.legend()
plt.show()
