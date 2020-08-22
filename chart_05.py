import os as os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import mpl_finance as mpf
from pprint import pprint
import datetime as dt
import numpy as np
import re
import pylab

#https://qiita.com/toyolab/items/1b5d11b5d376bd542022
#https://qiita.com/kjybinp1105/items/db4efd07e20000c22f4e

codes = [9101]
csv = "../../../source/repos/chart_gallery/stock_data/" + str(codes[0]) + ".csv"

def DataRead():
    with open(csv, 'r') as csv_file:
        df = pd.read_csv(csv_file, quotechar='"', header=1, index_col=0, skiprows=range(2, 7200))
        return df

def init():
    """
    初期化
    """
    global fig, ax
    fig = plt.figure()
    #fig = plt.figure(figsize=(24,10), dpi=300, facecolor='w')
    ax = plt.subplot()

def main():
    """
    main関数
    """
    global fig, ax
    ohlc = np.vstack((range(len(df)), df.values.T)).T
    mpf.candlestick_ohlc(ax, ohlc, width=0.7, colorup='red', colordown='green')
    w = dt.datetime.strptime(df.index[0], '%Y-%m-%d').weekday()
    xtick0 = (5 - w) % 5

    # グラフのx軸の日付の調整
    # plt.xticks(range(xtick0,len(df),5), [x.strftime('%Y-%m-%d') for x in df.index][xtick0::5])
    # plt.xticks(range(xtick0,len(df),5), [dt.datetime.strptime(x, '%Y-%m-%d') for x in df.index][xtick0::5])
    plt.xticks(range(xtick0, len(df), 5), [x for x in df.index][xtick0::5])

    term_5, term_7, term_10, term_20, term_60 = 5, 7, 10, 20, 60
    df['av_5'] = df['close'].rolling(window=term_5).mean()
    df['av_7'] = df['close'].rolling(window=term_7).mean()
    df['av_10'] = df['close'].rolling(window=term_10).mean()
    df['av_20'] = df['close'].rolling(window=term_20).mean()
    df['av_60'] = df['close'].rolling(window=term_60).mean()

def pointCross(status = '5_20', str = '', current_flag = 0, previous_flag = 1):
    """
    ゴールデンクロス/デッドクロスしたタイミングの抽出
    """
    if (status == '5_20'):
        ma = {'pointString':str+'_5_20', 1:'av_5', 2:'av_20'}
    elif (status == '20_60'):
        ma = {'pointString':str+'_20_60', 1:'av_20', 2:'av_60'}
    else:
        ma = {'pointString':str+'_5_20', 1:'av_5', 2:'av_20'}

    for i, price in df.iterrows():
        if (str == 'golden'):
            current_flag = 1 if (price[ma[1]] > price[ma[2]]) else 0
        else:
            current_flag = 1 if (price[ma[1]] < price[ma[2]]) else 0

        if (current_flag * (1 - previous_flag)):
            df.loc[i, ma['pointString']] = price[ma[2]]
        else:
            df.loc[i, ma['pointString']] = None

        previous_flag = current_flag

def plotMA():
    ax.plot(df.index, df['close'].rolling(5).mean(), color='r', label="MA(5)")
    ax.plot(df.index, df['close'].rolling(7).mean(), color='black', label="MA(7)", linestyle=':')
    ax.plot(df.index, df['close'].rolling(10).mean(), color='olive', label="MA(10)", linestyle=':')
    ax.plot(df.index, df['close'].rolling(20).mean(), color='g', label="MA(20)")
    ax.plot(df.index, df['close'].rolling(60).mean(), color='b', label="MA(60)")
    ax.plot(df.index, df['close'].rolling(75).mean(), color='y', label="MA(75)")
    ax.plot(df.index, df['close'].rolling(100).mean(), color='orange', label="MA(100)")
    ax.plot(df.index, df['close'].rolling(200).mean(), color='gold', label="MA(200)")
    ax.plot(df.index, df['close'].rolling(300).mean(), color='pink', label="MA(300)")
    # ax.plot(df.index, pd.Series(df['close']).rolling(5).mean(), color='g', label="MA(5)")

def scatterPoint():
    #plt.scatter(50, 2500, s=100, marker="o",color='gold')
    plt.scatter(x= df.index,y = df['golden_5_20'],marker='o',color='gold', s=200, label="GC_5_20")
    plt.scatter(x= df.index,y = df['ded_5_20'],marker='o',color='black', s=200, label="DC_5_20")
    plt.scatter(x= df.index,y = df['golden_20_60'],marker='o',color='orange', s=200, label="GC_20_60")
    plt.scatter(x= df.index,y = df['ded_20_60'],marker='o',color='pink', s=200, label="DC_20_60")

    plt.scatter(x= df.index,y = df['k_hanshin'],marker='^',color='dodgerblue', label="K_1")
    plt.scatter(x= df.index,y = df['k_hanshin_2'],marker='^',color='cyan', label="K_2")
    plt.scatter(x= df.index,y = df['k_hanshin_5'],marker='^',color='chartreuse', label="K_5")
    plt.scatter(x= df.index,y = df['k_hanshin_6'],marker='^',color='darkviolet', label="K_6")
    plt.scatter(x= df.index,y = df['gk_hanshin'],marker='v',color='dodgerblue', label="GK_1")
    plt.scatter(x= df.index,y = df['gk_hanshin_2'],marker='v',color='cyan', label="GK_2")
    plt.scatter(x= df.index,y = df['gk_hanshin_5'],marker='v',color='chartreuse', label="GK_5")
    plt.scatter(x= df.index,y = df['gk_hanshin_6'],marker='v',color='darkviolet', label="GK_6")

    plt.scatter(x= df.index,y = df['kka'],marker='4',color='olive')
    plt.scatter(x= df.index,y = df['akk'],marker='4',color='olive')

    cnt9 = df['cnt9'].values
    print(cnt9)
    for i, d in df.iterrows():
        #print(d.cnt9)
        marker = '$' + str(d.cnt9) + '$' if d.cnt9 is not np.nan else ""
        plt.scatter(x= i,y = d.hight + 25,marker=marker,color='black')
#        plt.scatter(x= df.index,y = df['hight'] + 75,marker='$' + str(9) + '$',color='black')

def zoneColor(str = '', start_dt = '', end_dt = '', dt_20_60 = ''):
    """
    PPPゾーンの表示
    """
    color = 'red' if (str == 'golden') else 'blue'
    if (str == 'golden'):
        opposite = 'ded'
    else:
        opposite = 'golden'

    for dt, price in df.iterrows():
        start_flag = df.loc[dt][str+'_5_20']
        end_flag = df.loc[dt][opposite+'_5_20']
        status_20_60 = df.loc[dt][str+'_20_60']
        if (np.isnan(start_flag) == False):
            start_dt = dt
            # pprint(dt)
            #pprint(start_dt)

        if (np.isnan(end_flag) == False):
            end_dt = dt
            # pprint(dt)
            #pprint(end_dt)

        if (np.isnan(status_20_60) == False):
            dt_20_60 = dt
            # pprint(dt)
            #pprint(dt_20_60)

        if (start_dt and end_dt):
            ax.axvspan(start_dt, end_dt, facecolor=color, alpha=0.1)
            if (dt_20_60 and end_dt):
                ax.axvspan(dt_20_60, end_dt, facecolor=color, alpha=0.2)
            strat_dt = ''
            end_dt = ''
            dt_20_60 = ''

df = DataRead()
df_ = df.copy()

new = [dt.datetime.strptime(i, '%Y-%m-%d') for i in df_.index]
df_.index = [mdates.date2num(i) for i in new]

#df_.index = mdates.date2num(df_.index)
data = df_.reset_index().values

init()
main()

#cnt9 初期化
cnt = 1
for i in df.index:
    df.loc[i, 'cnt9'] = np.nan

for i in df.index:
    op = df['open']
    cl = df['close']
    av5 = df['av_5']
    av7 = df['av_7']
    av10 = df['av_10']
    av20 = df['av_20']
    av60 = df['av_60']

    #print(i)
    #print(op[i])
    now = df.index.get_loc(i) #行番号取得
    pre = now - 1
    av5_p = df.iloc[pre]['av_5']
    av20_p = df.iloc[pre]['av_20']
    av60_p = df.iloc[pre]['av_60']

    test = list()
    test.append(i)
    test.append('〇') if av5[i] > av20[i] > av60[i] and av5_p < av5[i] and av20_p < av20[i] and av60_p < av60[i] else 'false'
    print(test)

    # シグナル[下半身、逆下半身]の表示
    center = op[i] + ((cl[i] - op[i]) * 0.5) # ローソク足の中心値
    graph_position_up = df['low'][i] * 0.98 #グラフで見やすいようにポジションをずらす
    graph_position_down = df['hight'][i] * 1.02 #グラフで見やすいようにポジションをずらす
    k_hn = graph_position_up if cl[i] > av5[i] and center > av5[i] and cl[i] > op[i] else np.nan
    '''
    df.loc[i, 'k_hanshin'] = k_hn if av5[i] > av20[i] > av60[i] and av5_p < av5[i] and av20_p < av20[i] and av60_p < av60[i] else np.nan
    df.loc[i, 'k_hanshin_2'] = k_hn if av20[i] > av5[i] > av60[i] and av5_p < av5[i] and av20_p < av20[i] and av60_p < av60[i] else np.nan
    df.loc[i, 'k_hanshin_5'] = k_hn if av60[i] > av5[i] > av20[i] and av5_p < av5[i] and av20_p < av20[i] and av60_p < av60[i] else np.nan
    df.loc[i, 'k_hanshin_6'] = k_hn if av5[i] > av60[i] > av20[i] and av5_p < av5[i] and av20_p < av20[i] and av60_p < av60[i] else np.nan
    '''
    df.loc[i, 'k_hanshin'] = k_hn if av5[i] > av20[i] > av60[i] and av5_p < av5[i] and av20_p < av20[i] else np.nan
    df.loc[i, 'k_hanshin_2'] = k_hn if av20[i] > av5[i] > av60[i] and av5_p < av5[i] and av20_p < av20[i] else np.nan
    df.loc[i, 'k_hanshin_5'] = k_hn if av60[i] > av5[i] > av20[i] and av5_p < av5[i] and av20_p < av20[i] else np.nan
    df.loc[i, 'k_hanshin_6'] = k_hn if av5[i] > av60[i] > av20[i] and av5_p < av5[i] and av20_p < av20[i] else np.nan

    gk_hn = graph_position_down if cl[i] < av5[i] and center < av5[i] and cl[i] < op[i] else np.nan
    '''
    df.loc[i, 'gk_hanshin'] = gk_hn if av5[i] < av20[i] < av60[i] and av5_p > av5[i] and av20_p > av20[i] and av60_p > av60[i] else np.nan
    df.loc[i, 'gk_hanshin_2'] = gk_hn if av20[i] < av5[i] < av60[i] and av5_p > av5[i] and av20_p > av20[i] and av60_p > av60[i] else np.nan
    df.loc[i, 'gk_hanshin_5'] = gk_hn if av60[i] < av5[i] < av20[i] and av5_p > av5[i] and av20_p > av20[i] and av60_p > av60[i] else np.nan
    df.loc[i, 'gk_hanshin_6'] = gk_hn if av5[i] < av60[i] < av20[i] and av5_p > av5[i] and av20_p > av20[i] and av60_p > av60[i] else np.nan
    '''
    #ch_gain = lambda a, b: 'true' if a > b else 'false'
    df.loc[i, 'gk_hanshin'] = gk_hn if av5[i] < av20[i] < av60[i] and av5_p > av5[i] and av20_p > av20[i] else np.nan
    df.loc[i, 'gk_hanshin_2'] = gk_hn if av20[i] < av5[i] < av60[i] and av5_p > av5[i] and av20_p > av20[i] else np.nan
    df.loc[i, 'gk_hanshin_5'] = gk_hn if av60[i] < av5[i] < av20[i] and av5_p > av5[i] and av20_p > av20[i] else np.nan
    df.loc[i, 'gk_hanshin_6'] = gk_hn if av5[i] < av60[i] < av20[i] and av5_p > av5[i] and av20_p > av20[i] else np.nan

    # 指標[9の法則]の表示
    cl_pre = df.iloc[pre]['close']
    cl_pre2 = df.iloc[pre - 1]['close'] # 2営業前の終値
    if cl_pre2 < cl_pre < cl[i] or av5[i] < cl[i]:
        df.loc[i, 'cnt9'] = str(cnt)
        cnt += 1

    else:
        cnt = 1
        df.loc[i, 'cnt9'] = np.nan

    # 指標[草黒赤]の表示
    print(av5[i], av7[i], av10[i])
    df.loc[i, 'kka'] = av5[i] * 0.97 if av5[i] > av7[i] > av10[i] else np.nan
    df.loc[i, 'akk'] = av5[i] * 1.03 if av5[i] < av7[i] < av10[i] else np.nan

#シグナル点灯有無確認
pprint('=====is np.nan?')
for dt in df.index:
    #if dt in ['2020-08-21', '2020-08-20', '2020-08-19', '2020-08-18', '2020-08-17', '2020-08-16']:
    if dt in ['2020-08-21', '2020-08-20', '2020-08-19', '2020-08-18', '2020-08-17', '2020-08-16']:
        now = df.index.get_loc(dt)  # 行番号取得
        pprint(df.iloc[now]['k_hanshin_6'])
        ret = dt if df.iloc[now]['k_hanshin_6'] > 0 else np.nan
        break
pprint(ret)
#exit()


df['golden_5_20'] = 0
df['golden_20_60'] = 0
df['ded_5_20'] = 0
df['ded_20_60'] = 0
pointCross('5_20', 'golden')
pointCross('20_60', 'golden')
pointCross('5_20', 'ded')
pointCross('20_60', 'ded')

# 移動平均線表示
plotMA()

#シグナル表示
scatterPoint()

ax.grid()
ax.set_xlim(-1, len(df))
fig.autofmt_xdate()

# PPPゾーンの表示
ppp = np.array( [] )
zoneColor('golden')
zoneColor('ded')

# base
plt.legend()
plt.show()
#plt.savefig('test.png')

