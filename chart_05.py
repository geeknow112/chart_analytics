import os as os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import mpl_finance as mpf
from pprint import pprint
import datetime as dt
import numpy as np

csv = "../stock_data/9101_2019.csv"
#csv = "D://Users/z112/source/repos/ConsoleApp2/stock_data/9104_2019.csv"
#csv = "C:/Users/r2d2/source/repos/chart_gallery/stock_data/9101_2019.csv"
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

#df_.index = mdates.date2num(df_.index)
data = df_.reset_index().values

''''''
#https://qiita.com/toyolab/items/1b5d11b5d376bd542022
#https://qiita.com/kjybinp1105/items/db4efd07e20000c22f4e

fig = plt.figure()
ax = plt.subplot()

ohlc = np.vstack((range(len(df)), df.values.T)).T
mpf.candlestick_ohlc(ax, ohlc, width=0.7, colorup='red', colordown='green')

w = dt.datetime.strptime(df.index[0], '%Y-%m-%d').weekday()
#pprint(w)%exit()

xtick0 = (5-w)%5
#pprint(xtick0)%exit()

#グラフのx軸の日付の調整
#plt.xticks(range(xtick0,len(df),5), [x.strftime('%Y-%m-%d') for x in df.index][xtick0::5])
#plt.xticks(range(xtick0,len(df),5), [dt.datetime.strptime(x, '%Y-%m-%d') for x in df.index][xtick0::5])
plt.xticks(range(xtick0,len(df),5), [x for x in df.index][xtick0::5])

term_5 = 5
term_20 = 20
term_60 = 60

df['av_5'] = df['close'].rolling(window=term_5).mean()
df['av_20'] = df['close'].rolling(window=term_20).mean()
df['av_60'] = df['close'].rolling(window=term_60).mean()

# ゴールデンクロスしたタイミングの抽出
def pointGoldenCross(status = '5_20', current_flag = 0, previous_flag = 1):
    if (status == '5_20'):
        ma = {'pointString':'golden_5_20', 1:'av_5', 2:'av_20'}
    elif (status == '20_60'):
        ma = {'pointString':'golden_20_60', 1:'av_20', 2:'av_60'}
    else:
        ma = {'pointString':'golden_5_20', 1:'av_5', 2:'av_20'}

    for i, price in df.iterrows():
        if (price[ma[1]] > price[ma[2]]):
            current_flag = 1
        else:
            current_flag = 0

        if (current_flag * (1 - previous_flag)):
            df.loc[i, ma['pointString']] = price[ma[2]]
        else:
            df.loc[i, ma['pointString']] = None

        previous_flag = current_flag

df['golden_5_20'] = 0
pointGoldenCross('5_20')

df['golden_20_60'] = 0
pointGoldenCross('20_60')
#pprint(df['golden_20-60'])
#exit()

# デッドクロスのタイミングの抽出
def pointDedCross(status = '5_20', current_flag = 0, previous_flag = 1):
    if (status == '5_20'):
        ma = {'pointString':'ded_5_20', 1:'av_5', 2:'av_20'}
    elif (status == '20_60'):
        ma = {'pointString':'ded_20_60', 1:'av_20', 2:'av_60'}
    else:
        ma = {'pointString':'ded_5_20', 1:'av_5', 2:'av_20'}

    for i, price in df.iterrows():
        if (price[ma[1]] < price[ma[2]]):
            current_flag = 1
        else:
            current_flag = 0

        if (current_flag * (1 - previous_flag)):
            df.loc[i, ma['pointString']] = price[ma[2]]
        else:
            df.loc[i, ma['pointString']] = None

        previous_flag = current_flag

df['ded_5_20'] = 0
pointDedCross('5_20')

df['ded_20_60'] = 0
pointDedCross('20_60')

#pprint(df['ded_5_20'])

#df.plot(style=['-'])

ax.plot(df.index, df['close'].rolling(5).mean(), color='r', label="MA(5)")
ax.plot(df.index, df['close'].rolling(20).mean(), color='g', label="MA(20)")
ax.plot(df.index, df['close'].rolling(60).mean(), color='b', label="MA(60)")
ax.plot(df.index, df['close'].rolling(75).mean(), color='y', label="MA(75)")
ax.plot(df.index, df['close'].rolling(100).mean(), color='orange', label="MA(100)")
ax.plot(df.index, df['close'].rolling(200).mean(), color='gold', label="MA(200)")
ax.plot(df.index, df['close'].rolling(300).mean(), color='pink', label="MA(300)")
#ax.plot(df.index, pd.Series(df['close']).rolling(5).mean(), color='g', label="MA(5)")
#plt.scatter(50, 2500, s=100, marker="o",color='gold')
plt.scatter(x= df.index,y = df['golden_5_20'],marker='o',color='gold')
plt.scatter(x= df.index,y = df['ded_5_20'],marker='o',color='black')
plt.scatter(x= df.index,y = df['golden_20_60'],marker='o',color='orange')
plt.scatter(x= df.index,y = df['ded_20_60'],marker='o',color='pink')
ax.grid()
ax.set_xlim(-1, len(df))
fig.autofmt_xdate()
''''''
#exit()

#axvspan
#PPPゾーンの表示
ppp = np.array( [] )
start_dt = ''
end_dt = ''
golden_20_60_dt = ''
for dt, price in df.iterrows():
    golden_5_20 = df.loc[dt]['golden_5_20']
    end_flag = df.loc[dt]['ded_5_20']
    golden_20_60 = df.loc[dt]['golden_20_60']
    if (np.isnan(golden_5_20) == False):
        start_dt = dt
        #pprint(dt)
        pprint(start_dt)

    if (np.isnan(end_flag) == False):
        end_dt = dt
        #pprint(dt)
        pprint(end_dt)

    if (np.isnan(golden_20_60) == False):
        golden_20_60_dt = dt
        #pprint(dt)
        pprint(golden_20_60_dt)

    if (start_dt and end_dt):
        ax.axvspan(start_dt, end_dt, facecolor = "red", alpha=0.1)
        if (golden_20_60_dt and end_dt):
            ax.axvspan(golden_20_60_dt, end_dt, facecolor = "red", alpha=0.2)
        strat_dt = ''
        end_dt = ''
        golden_20_60_dt = ''

ppp = np.array( [] )
start_dt = ''
end_dt = ''
ded_20_60_dt = ''
for dt, price in df.iterrows():
    start_flag = df.loc[dt]['ded_5_20']
    end_flag = df.loc[dt]['golden_5_20']
    ded_20_60 = df.loc[dt]['ded_20_60']
    if (np.isnan(start_flag) == False):
        start_dt = dt
        #pprint(dt)
        pprint(start_dt)

    if (np.isnan(end_flag) == False):
        end_dt = dt
        #pprint(dt)
        pprint(end_dt)

    if (np.isnan(ded_20_60) == False):
        ded_20_60_dt = dt
        #pprint(dt)
        pprint(ded_20_60_dt)

    if (start_dt and end_dt):
        ax.axvspan(start_dt, end_dt, facecolor = "blue", alpha=0.1)
        if (ded_20_60_dt and end_dt):
            ax.axvspan(ded_20_60_dt, end_dt, facecolor = "blue", alpha=0.2)
        strat_dt = ''
        end_dt = ''
        ded_20_60_dt = ''
        #break

#ax.axvspan(start_dt, end_dt, facecolor = "red", alpha=0.2)

plt.legend()
plt.show()
