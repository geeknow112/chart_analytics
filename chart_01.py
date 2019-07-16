import os as os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import mpl_finance as mpf
from pprint import pprint
import datetime as dt
import numpy as np

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

fig = plt.figure()
ax = plt.subplot()

ohlc = np.vstack((range(len(df)), df.values.T)).T
mpf.candlestick_ohlc(ax, ohlc, width=0.7, colorup='r', colordown='b')

w = dt.datetime.strptime(df.index[0], '%Y-%m-%d').weekday()
#pprint(w)%exit()

xtick0 = (5-w)%5
#pprint(xtick0)%exit()

#plt.xticks(range(xtick0,len(df),5), [x.strftime('%Y-%m-%d') for x in df.index][xtick0::5])
plt.xticks(range(xtick0,len(df),5), [dt.datetime.strptime(x, '%Y-%m-%d') for x in df.index][xtick0::5])

#pprint(df['close'])%exit()
ax.plot(df.index, df['close'].rolling(5).mean(), color='r', label="Moving Ave(5)")
ax.plot(df.index, df['close'].rolling(20).mean(), color='g', label="Moving Ave(20)")
ax.plot(df.index, df['close'].rolling(60).mean(), color='b', label="Moving Ave(60)")
ax.plot(df.index, df['close'].rolling(75).mean(), color='y', label="Moving Ave(75)")
ax.plot(df.index, df['close'].rolling(100).mean(), color='orange', label="Moving Ave(100)")
ax.plot(df.index, df['close'].rolling(200).mean(), color='gold', label="Moving Ave(200)")
ax.plot(df.index, df['close'].rolling(300).mean(), color='pink', label="Moving Ave(300)")
#ax.plot(df.index, pd.Series(df['close']).rolling(5).mean(), color='g', label="Moving Ave(5)")
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
