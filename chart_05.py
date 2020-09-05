import os as os
import pandas as pd
import matplotlib as mpl
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

def dataRead():
    cnt = 0
    with open(csv, 'r') as csv_file:
        for line in csv_file:
            cnt += 1
    skips = int(cnt * 0.98) # 銘柄csvの行数を集計しその80%をskiprowsにする
#    print(skips)
    with open(csv, 'r') as csv_file:
        df = pd.read_csv(csv_file, quotechar='"', header=1, index_col=0, skiprows=range(2, skips))
        return df

def init():
    """ 初期化
    """
    global fig, ax
    fig = plt.figure()
    #fig = plt.figure(figsize=(24,10), dpi=300, facecolor='w')
    ax = plt.subplot()

def main():
    """ main関数
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

    # 出来高のチャートをプロット
    ax2 = ax.twinx()
    mpf.volume_overlay(ax2, df['open'], df['close'], df['power'], width=0.5, colorup="yellow", colordown="yellow", alpha=0.3)
    ax2.set_xlim([0, df.shape[0]])

    # 出来高チャートは下側25%に収める
    ax2.set_ylim([0, df['power'].max() * 7])
    ax2.set_ylabel('power')

def pointCross(status = '5_20', str = '', current_flag = 0, previous_flag = 1):
    """ ゴールデンクロス/デッドクロスしたタイミングの抽出
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
    ax.scatter(x= df.index,y = df['golden_5_20'],marker='o',color='gold', s=200, label="GC_5_20")
    ax.scatter(x= df.index,y = df['ded_5_20'],marker='o',color='black', s=200, label="DC_5_20")
    ax.scatter(x= df.index,y = df['golden_20_60'],marker='o',color='orange', s=200, label="GC_20_60")
    ax.scatter(x= df.index,y = df['ded_20_60'],marker='o',color='pink', s=200, label="DC_20_60")

    ax.scatter(x= df.index,y = df['k_sgun'],marker='^',color='blue', label="K_sgun1")
    ax.scatter(x= df.index,y = df['gk_sgun'],marker='v',color='black', label="GK_sgun1")

    ax.scatter(x= df.index,y = df['k_hanshin'],marker='^',color='dodgerblue', label="K_1")
    ax.scatter(x= df.index,y = df['k_hanshin_2'],marker='^',color='cyan', label="K_2")
    ax.scatter(x= df.index,y = df['k_hanshin_5'],marker='^',color='chartreuse', label="K_5")
    ax.scatter(x= df.index,y = df['k_hanshin_6'],marker='^',color='darkviolet', label="K_6")
    ax.scatter(x= df.index,y = df['gk_hanshin'],marker='v',color='dodgerblue', label="GK_1")
    ax.scatter(x= df.index,y = df['gk_hanshin_2'],marker='v',color='cyan', label="GK_2")
    ax.scatter(x= df.index,y = df['gk_hanshin_5'],marker='v',color='chartreuse', label="GK_5")
    ax.scatter(x= df.index,y = df['gk_hanshin_6'],marker='v',color='darkviolet', label="GK_6")

    ax.scatter(x= df.index,y = df['kka'],marker='4',color='olive')
    ax.scatter(x= df.index,y = df['akk'],marker='4',color='olive')

    ax.scatter(x= df.index,y = df['kai_1'],marker='s',color='red', edgecolors='black', alpha=0.3, s=300, label="in-in-harami")
    ax.scatter(x= df.index,y = df['uri_1'],marker='s',color='blue', edgecolors='black', alpha=0.3, s=300, label="you-you-harami")

    ax.scatter(x= df.index,y = df['kai_2'],marker='o',color='red', alpha=0.3, s=400, label="idaki_you")
    ax.scatter(x= df.index,y = df['uri_2'],marker='o',color='blue', alpha=0.3, s=400, label="idaki_in")

    cnt9 = df['cnt9'].values
    #print(cnt9)
    for i, d in df.iterrows():
        #print(d.cnt9)
        marker = '$' + str(d.cnt9) + '$' if d.cnt9 is not np.nan else ""
        ax.scatter(x= i,y = d.hight + 25,marker=marker,color='black')
#        plt.scatter(x= df.index,y = df['hight'] + 75,marker='$' + str(9) + '$',color='black')

def zoneColor(str = ''):
    """ PPPゾーンの表示
    """
    color = 'red' if str == 'golden' else 'blue'
    opposite = 'ded' if str == 'golden' else 'golden'

    gc_5_20_dt = dc_5_20_dt = gc_20_60 = gc_20_60_dt = ''
    for dt, price in df.iterrows():
        gc_5_20 = df.loc[dt][str+'_5_20']
        dc_5_20 = df.loc[dt][opposite+'_5_20']
        gc_20_60 = df.loc[dt][str+'_20_60']
        if (np.isnan(gc_5_20) == False): gc_5_20_dt = dt
        if (np.isnan(dc_5_20) == False): dc_5_20_dt = dt
        if (np.isnan(gc_20_60) == False): gc_20_60_dt = dt

        if (gc_5_20_dt is not '' and dc_5_20_dt is not ''):
            ax.axvspan(gc_5_20_dt, dc_5_20_dt, facecolor=color, alpha=0.1)
            if (gc_20_60_dt and dc_5_20_dt): ax.axvspan(gc_20_60_dt, dc_5_20_dt, facecolor=color, alpha=0.2)
            strat_dt = dc_5_20_dt = gc_20_60_dt = ''

def set_signal():
    """ シグナルの表示
    """
    # cnt9 初期化
    cnt = 1
    for i in df.index:
        df.loc[i, 'cnt9'] = np.nan

    for i in df.index:
        op, cl, av5, av7, av10, av20, av60 = df['open'], df['close'], df['av_5'], df['av_7'], df['av_10'], df['av_20'], \
                                             df['av_60']
        now = df.index.get_loc(i)  # 行番号取得
        pre = now - 1
        av5_p, av20_p, av60_p = df.iloc[pre]['av_5'], df.iloc[pre]['av_20'], df.iloc[pre]['av_60']

        # シグナル[下半身、逆下半身]の表示
        center = op[i] + ((cl[i] - op[i]) * 0.5)  # ローソク足の中心値
        graph_position_up = df['low'][i] * 0.98  # グラフで見やすいようにポジションをずらす
        graph_position_down = df['hight'][i] * 1.02  # グラフで見やすいようにポジションをずらす
        k_hn = graph_position_up if hight(av5[i], cl[i]) and hight(av5[i], center) and hight(op[i], cl[i]) else np.nan
        gtrend = gain_trend(av5_p, av5[i], av20_p, av20[i], av60_p, av60[i])
        df.loc[i, 'k_hanshin'] = k_hn if zone_PPP_1(av5[i], av20[i], av60[i]) and gtrend is True else np.nan
        df.loc[i, 'k_hanshin_2'] = k_hn if zone_PPP_2(av5[i], av20[i], av60[i]) and gtrend is True else np.nan
        df.loc[i, 'k_hanshin_5'] = k_hn if zone_PPP_5(av5[i], av20[i], av60[i]) and gtrend is True else np.nan
        df.loc[i, 'k_hanshin_6'] = k_hn if zone_PPP_6(av5[i], av20[i], av60[i]) and gtrend is True else np.nan

        gk_hn = graph_position_down if low(av5[i], cl[i]) and low(av5[i], center) and low(op[i], cl[i]) else np.nan
        # gain = lambda a, b: 'true' if a > b else 'false'
        dtrend = down_trend(av5_p, av5[i], av20_p, av20[i], av60_p, av60[i])
        df.loc[i, 'gk_hanshin'] = gk_hn if zone_GPPP_1(av5[i], av20[i], av60[i]) and dtrend is True else np.nan
        df.loc[i, 'gk_hanshin_2'] = gk_hn if zone_GPPP_2(av5[i], av20[i], av60[i]) and dtrend is True else np.nan
        df.loc[i, 'gk_hanshin_5'] = gk_hn if zone_GPPP_5(av5[i], av20[i], av60[i]) and dtrend is True else np.nan
        df.loc[i, 'gk_hanshin_6'] = gk_hn if zone_GPPP_6(av5[i], av20[i], av60[i]) and dtrend is True else np.nan

        # 指標[9の法則]の表示
        cl_pre = df.iloc[pre]['close']
        cl_pre2 = df.iloc[pre - 1]['close']  # 2営業前の終値
        if cl_pre2 < cl_pre < cl[i] or av5[i] < cl[i]:
            df.loc[i, 'cnt9'] = str(cnt)
            cnt += 1
        else:
            cnt = 1
            df.loc[i, 'cnt9'] = np.nan

        # 指標[草黒赤]の表示
        df.loc[i, 'kka'] = av5[i] * 0.97 if index_kka(av5[i], av7[i], av10[i]) else np.nan
        df.loc[i, 'akk'] = av5[i] * 1.03 if index_akk(av5[i], av7[i], av10[i]) else np.nan

        op_pre, cl_pre, op, cl = df.iloc[pre]['open'], df.iloc[pre]['close'], df.iloc[now]['open'], df.iloc[now][
            'close']
        # シグナル[買い: 陰の陰はらみ: 底値示唆]の表示
        # df.loc[i, 'kai_1'] = graph_position_up * 0.97 if op_pre > cl_pre and op > cl and op_pre > op and cl_pre < cl else np.nan
        df.loc[i, 'kai_1'] = cl if low(op_pre, cl_pre) and low(op, cl) and down(op_pre, op) and gain(cl_pre,
                                                                                                     cl) else np.nan
        # シグナル[売り: 陽の陽はらみ: 利益確定タイミング]の表示
        df.loc[i, 'uri_1'] = cl if hight(op_pre, cl_pre) and hight(op, cl) and gain(op_pre, op) and down(cl_pre,
                                                                                                         cl) else np.nan

        # 陽の抱き線
        df.loc[i, 'kai_2'] = cl if idaki_sen_you(op_pre, cl_pre, op, cl) is True else np.nan
        # 陰の抱き線
        df.loc[i, 'uri_2'] = cl if idaki_sen_in(op_pre, cl_pre, op, cl) is True else np.nan


def set_signal_shotgun():
    """ シグナルの表示
    """
    for i in df.index:
        op, cl, av5, av7, av10, av20, av60 = df['open'], df['close'], df['av_5'], df['av_7'], df['av_10'], df['av_20'], df['av_60']
        now = df.index.get_loc(i)  # 行番号取得
        pre = now - 1
        av5_p, av20_p, av60_p = df.iloc[pre]['av_5'], df.iloc[pre]['av_20'], df.iloc[pre]['av_60']

        # シグナル[下半身、逆下半身]の表示
        center = op[i] + ((cl[i] - op[i]) * 0.5)  # ローソク足の中心値
        graph_position_up = df['low'][i] * 0.95  # グラフで見やすいようにポジションをずらす
        graph_position_down = df['hight'][i] * 1.05  # グラフで見やすいようにポジションをずらす
        k_hn = graph_position_up if hight(av5[i], cl[i]) and hight(av5[i], center) and hight(op[i], cl[i]) else np.nan
        gtrend = gain_trend(av5_p, av5[i], av20_p, av20[i], av60_p, av60[i])
        #df.loc[i, 'k_sgun'] = k_hn if zone_PPP_1(av5[i], av20[i], av60[i]) and gtrend is True else np.nan
        df.loc[i, 'k_sgun'] = k_hn if hight(av5[i], center) and gain(av5_p, av5[i]) else np.nan

        gk_hn = graph_position_down if low(av5[i], cl[i]) and low(av5[i], center) and low(op[i], cl[i]) else np.nan
        dtrend = down_trend(av5_p, av5[i], av20_p, av20[i], av60_p, av60[i])
        #df.loc[i, 'gk_sgun'] = gk_hn if zone_GPPP_1(av5[i], av20[i], av60[i]) and dtrend is True else np.nan
        df.loc[i, 'gk_sgun'] = gk_hn if av5[i] > center else np.nan

def idaki_sen_you(op_pre, cl_pre, op, cl): # 陽の抱き線の抽出
    return True if low(op_pre, cl_pre) and gain(op_pre, cl) and down(cl_pre, op) and hight(op, cl) else np.nan

def idaki_sen_in(op_pre, cl_pre, op, cl): # 陰の抱き線の抽出
    return True if hight(op_pre, cl_pre) and gain(cl_pre, op) and down(op_pre, cl) and low(op, cl) else np.nan

def index_9count(df):
    return np.nan

def index_kka(av5, av7, av10): # 指標[草黒赤]の表示
    return True if av5 > av7 > av10 else False

def index_akk(av5, av7, av10): # 指標[赤黒草]の表示
    return True if av5 < av7 < av10 else False

def gain_trend(av5_p, av5, av20_p, av20, av60_p, av60): # 全体の傾きからトレンドを判定
    #return True if gain(av5_p, av5) and gain(av20_p, av20) and gain(av60_p, av60) else False
    return True if gain(av5_p, av5) and gain(av20_p, av20) else False

def down_trend(av5_p, av5, av20_p, av20, av60_p, av60): # 全体の傾きからトレンドを判定
    #return True if down(av5_p, av5) and down(av20_p, av20) and down(av60_p, av60) else False
    return True if down(av5_p, av5) and down(av20_p, av20) else False

def zone_PPP_1(av5, av20, av60): # ゾーン[PPP1類]の判定 # av5 > av 20 > av60
    return True if gain(av20, av5) and gain(av60, av20) else False

def zone_PPP_2(av5, av20, av60): # ゾーン[PPP2類]の判定 # av20 > av5 > av60
    return True if gain(av5, av20) and gain(av60, av5) else False

def zone_PPP_5(av5, av20, av60): # ゾーン[PPP5類]の判定 # av60 > av5 > av20
    return True if gain(av5, av60) and gain(av20, av5) else False

def zone_PPP_6(av5, av20, av60): # ゾーン[PPP6類]の判定 # av5 > av60 > av20
    return True if gain(av60, av5) and gain(av20, av60) else False

def zone_GPPP_1(av5, av20, av60):  # ゾーン[逆PPP1類]の判定 # av5 < av 20 < av60
    return True if down(av20, av5) and down(av60, av20) else False

def zone_GPPP_2(av5, av20, av60):  # ゾーン[逆PPP2類]の判定 # av20 < av 5 < av60
    return True if down(av5, av20) and down(av60, av5) else False

def zone_GPPP_5(av5, av20, av60):  # ゾーン[逆PPP5類]の判定 # av60 < av 5 < av20
    return True if down(av5, av60) and down(av20, av5) else False

def zone_GPPP_6(av5, av20, av60):  # ゾーン[逆PPP6類]の判定 # av5 < av 60 < av20
    return True if down(av60, av5) and down(av20, av60) else False

def hight(op, cl): # 陽線の確認
    return True if op < cl else False

def low(op, cl): # 陰線の確認
    return True if op > cl else False

def gain(pre, now): # 移動平均線が前日より上昇しているかどうかの判定
    return True if pre < now else False

def down(pre, now): # 2項の比較で下落している場合、真
    return True if pre > now else False

def check_signal():
    """シグナル点灯有無確認
    """

    # 日付取得
    from datetime import datetime, date, timedelta
    days = list()
    today = datetime.today()
    for i in range(3): # 直近n日のシグナル有無を確認する
        days.append(datetime.strftime(today - timedelta(days=i), '%Y-%m-%d'))
    #print(days)%exit()

    ret = list()
    for dt in df.index:
        #if dt in ['2020-08-21', '2020-08-20', '2020-08-19', '2020-08-18', '2020-08-17', '2020-08-16']:
        if dt in days:
            now = df.index.get_loc(dt)  # 行番号取得
            #pprint(df.iloc[now]['k_hanshin_6'])
            ret.append(dt if df.iloc[now]['k_hanshin'] > 0 and df.iloc[now]['kka'] > 0 else '')
            ret.append(dt if df.iloc[now]['k_hanshin_2'] > 0 and df.iloc[now]['kka'] > 0 else '')
            #ret.append(dt if df.iloc[now]['k_hanshin_5'] > 0 and df.iloc[now]['kka'] > 0 else '')
            #ret.append(dt if df.iloc[now]['k_hanshin_6'] > 0 and df.iloc[now]['kka'] > 0 else '')

            #ret.append(dt if df.iloc[now]['gk_hanshin'] > 0 and df.iloc[now]['akk'] > 0 else '')
            #ret.append(dt if df.iloc[now]['gk_hanshin_2'] > 0 and df.iloc[now]['akk'] > 0 else '')
            #ret.append(dt if df.iloc[now]['gk_hanshin_5'] > 0 and df.iloc[now]['akk'] > 0 else '')
            #ret.append(dt if df.iloc[now]['gk_hanshin_6'] > 0 and df.iloc[now]['akk'] > 0 else '')
            break
    print(code, ret)
    if code == 9101 or code == 9104 or code == 9107:
        return code
    return code if ret.count('') < len(ret) else ''

def getCodeName(code):
    i = cf.index.get_loc(code)
    return cf.iloc[i]['name']

def connectMysql():
    import mysql.connector as mydb

    # コネクションの作成
    conn = mydb.connect(
        host='localhost',
        port='3306',
        user='root',
        password='rage5557',
        database='stocks'
    )
    return conn

def fetchDatas(code):
    conn = connectMysql()
    conn.ping(reconnect=True)
    # print(conn.is_connected())
    cur = conn.cursor()

    cnt_sql = "select count(id) From s" + str(code) + ";"
    cur.execute(cnt_sql)
    cnt_taple = cur.fetchone()
    cnt = cnt_taple[0]
    limit = 7550
    cnt = limit if cnt > limit else (cnt - 200) # 株価がlimit日数分ない場合、200日分を表示
    where = " where id > " + str(cnt)
    #where = " where id > 7350 and id < 7550"

    sql = "select date, open, hight, low, close, power, End From s" + str(code) + where + ";"
    cur.execute(sql)
    rows = cur.fetchall()
    sdata = pd.read_sql(sql, conn, index_col='date')
    cur.close()
    conn.close()
    return sdata

def set_av():
    term_5, term_7, term_10, term_20, term_60 = 5, 7, 10, 20, 60
    df['av_5'] = df['close'].rolling(window=term_5).mean()
    df['av_7'] = df['close'].rolling(window=term_7).mean()
    df['av_10'] = df['close'].rolling(window=term_10).mean()
    df['av_20'] = df['close'].rolling(window=term_20).mean()
    df['av_60'] = df['close'].rolling(window=term_60).mean()

def drow_graph(code):
    init()  # グラフ初期化
    main()  # グラフメイン関数
    fig.suptitle(str(code) + ':' + getCodeName(code), fontname="MS Gothic")  # title 表示

    df['golden_5_20'] = df['golden_20_60'] = df['ded_5_20'] = df['ded_20_60'] = 0
    pointCross('5_20', 'golden')
    pointCross('20_60', 'golden')
    pointCross('5_20', 'ded')
    pointCross('20_60', 'ded')

    plotMA()  # 移動平均線表示
    scatterPoint()  # シグナル表示

    ax.grid()
    ax.set_xlim(-1, len(df))
    # ax.text(20, 2000, 'test', size=20)
    fig.autofmt_xdate()

    zoneColor('golden')  # PPPゾーンの表示
    zoneColor('ded')  # PPPゾーンの表示

def backtest():
    bt = pd.DataFrame({'uri': 0,
                       'kai': 0,
                       'total': 0},
                      index=df.index)
    for dt in df.index:
        o = df.loc[dt]['open']
        c = df.loc[dt]['close']
        if df.loc[dt]['k_hanshin'] > 0:
            bt.loc[dt]['kai'] += 1
        if low(o, c) is True:
            #if bt.loc[dt]['kai_sum'] > 0 and low(o, c) is True:
            #bt.loc[dt]['kai'] = bt.loc[dt]['kai_sum'] = 0
            print(o)
        bt.loc[dt]['total'] = bt['kai'].sum()
    print(bt)

conf_file = "../../../source/repos/chart_gallery/stock_data/nikkei_225.csv"
with open(conf_file, 'r') as config:
    cf = pd.read_csv(config, quotechar='"', header=38, index_col=0)
codes = list()
codes = [code for code in cf.index]
#print(getCodeName(1332))%exit()

mpl.rcParams['figure.figsize'] = [20.0, 10.0]
#codes = [9101]
codes = [9101, 9104, 9107, 6326, 4183]
#codes = [9101, 9104, 9107, 4021, 4183, 4005, 4188, 4911, 3407, 4042, 6988, 3405, 4061, 4208, 4272, 4004, 4631, 4043, 4901, 4452, 4063, 8630, 8750, 8795, 8725, 8766, 8697, 8253, 8830, 8804, 8801, 3289, 8802, 9022, 9021, 9020, 9009, 9005, 9007, 9008, 9001, 9062, 9064]
ret_codes = list()
for code in codes:
    sdata = fetchDatas(code) # DBから株価データ取得

    df = sdata.copy()
    df_ = df.copy()

    new = [dt.datetime.strptime(i, '%Y-%m-%d') for i in df_.index]
    df_.index = [mdates.date2num(i) for i in new]

    #df_.index = mdates.date2num(df_.index)
    data = df_.reset_index().values

    set_av() # 移動平均線設定
    set_signal() # シグナルの表示
    set_signal_shotgun() # シグナルの表示
    ret_code = check_signal() # シグナル点灯確認
    if ret_code is not '':
        drow_graph(ret_code)
        plt.savefig('./charts/' + str(ret_code) + '.png')

    #backtest() # シグナル発生時に建玉操作をシミュレーションする

print(ret_codes)
# base
#plt.legend()
#plt.show()

