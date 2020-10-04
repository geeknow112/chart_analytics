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

def pointCross(df, status = '5_20', str = '', current_flag = 0, previous_flag = 1):
    """ ゴールデンクロス/デッドクロスしたタイミングの抽出
    """
    if (status == '5_20'):
        ma = {'pointString':str+'_5_20', 1:'av_5', 2:'av_20'}
    elif (status == '20_60'):
        ma = {'pointString':str+'_20_60', 1:'av_20', 2:'av_60'}
    elif (status == '5_60'):
        ma = {'pointString': str + '_5_60', 1: 'av_5', 2: 'av_60'}
    elif (status == '5_100'):
        ma = {'pointString':str+'_5_100', 1:'av_5', 2:'av_100'}
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


def zone_color_golden_bk(df, np, ax):
    from datetime import datetime, date, timedelta
    for dt, price in df.iterrows():
        next_dt = (datetime.strptime(dt, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')
        if (price['av_5'] > price['av_20'] > price['av_60']): ax.axvline(x=dt, color='red', alpha=0.2, linewidth=5, linestyle="-")
        elif (price['av_5'] > price['av_60'] > price['av_20']): ax.axvline(x=dt, color='red', alpha=0.1, linewidth=4, linestyle="-")
        elif (price['av_5'] < price['av_20'] < price['av_60']): ax.axvline(x=dt, color='blue', alpha=0.2, linewidth=5, linestyle="-")
        elif (price['av_5'] < price['av_20'] > price['av_60']): ax.axvline(x=dt, color='blue', alpha=0.1, linewidth=4, linestyle="-")
        '''
        today_dt = datetime.strptime(dt, '%Y-%m-%d')
        next_dt = datetime.strptime(dt, '%Y-%m-%d') + timedelta(days=1)
        start_d = datetime(2019, 3, 4)
        end_d = datetime(2019, 3, 5)
        #if (price['av_5'] > price['av_20'] > price['av_60']):
        ax.axvspan('2020-08-24', '2020-08-31', facecolor='red', alpha=0.1)
        '''


def zone_color_golden(df, np, ax):
    """ PPPゾーンの表示
    """
    color = 'red'

    g5x20_dt = g20x60_dt = g5x60_dt = d5x20_dt = ''
    dts = []
    for dt, price in df.iterrows():
        if (np.isnan(df.loc[dt]['golden_5_20']) == False): dts.append({'g5x20': dt})
        if (np.isnan(df.loc[dt]['golden_20_60']) == False): dts.append({'g20x60': dt})
        if (np.isnan(df.loc[dt]['golden_5_60']) == False): dts.append({'g5x60': dt})
        if (np.isnan(df.loc[dt]['ded_5_20']) == False): dts.append({'d5x20': dt})
        if (np.isnan(df.loc[dt]['ded_5_60']) == False): dts.append({'d5x60': dt})
        if (np.isnan(df.loc[dt]['ded_20_60']) == False): dts.append({'d20x60': dt})

    dts.append({'end': 'none'})
    print(dts)

    import copy
    dts2 = copy.copy(dts)
    dts2.append({'end': 'none'})
    ret = list()
    i = 0
    for dic in dts:
        for k, v in dic.items():
            ret.append([list(dts[i].keys())[0], list(dts[i].values())[0], list(dts2[i+1].values())[0]])
        i = i + 1
    print(ret)

    for k, sdt, edt in ret:
        #print(k, sdt, edt)
        if (k is 'g5x20'): ax.axvspan(sdt, edt, facecolor='red', alpha=0.1)
        if (k is 'g5x60'): ax.axvspan(sdt, edt, facecolor='red', alpha=0.2)
        if (k is 'g20x60'): ax.axvspan(sdt, edt, facecolor='red', alpha=0.3)
        if (k is 'd5x20'): ax.axvspan(sdt, edt, facecolor='blue', alpha=0.1)
        if (k is 'd5x60'): ax.axvspan(sdt, edt, facecolor='blue', alpha=0.2)
        if (k is 'd20x60'): ax.axvspan(sdt, edt, facecolor='blue', alpha=0.3)

    #exit()


def zoneColor(df, np, ax, str = ''):
    """ PPPゾーンの表示
    """
    color = 'red' if str == 'golden' else 'blue'
    opp = 'ded' if str == 'golden' else 'golden' #opp = opposite = 反対

    g5x20_dt = g20x60_dt = g5x60_dt = ''
    d5x20_dt = d20x60_dt = d5x60_dt = ''
    for dt, price in df.iterrows():
        if (np.isnan(df.loc[dt][str+'_5_20']) == False): g5x20_dt = dt
        if (np.isnan(df.loc[dt][str+'_20_60']) == False): g20x60_dt = dt
        if (np.isnan(df.loc[dt][str+'_5_60']) == False): g5x60_dt = dt
        if (np.isnan(df.loc[dt][opp+'_5_20']) == False): d5x20_dt = dt
        if (np.isnan(df.loc[dt][opp+'_20_60']) == False): d20x60_dt = dt
        if (np.isnan(df.loc[dt][opp+'_5_60']) == False): d5x60_dt = dt

        if (g5x20_dt is not '' and d5x20_dt is not ''):
            ax.axvspan(g5x20_dt, d5x20_dt, facecolor=color, alpha=0.1)
            if (g5x60_dt and g20x60_dt): ax.axvspan(g5x60_dt, g20x60_dt, facecolor=color, alpha=0.1)
            if (g20x60_dt and d5x20_dt): ax.axvspan(g20x60_dt, d5x20_dt, facecolor=color, alpha=0.2)
            d5x20_dt = g20x60_dt = ''

def plotMA(ax, df):
    ax.plot(df.index, df['close'].rolling(3).mean(), color='magenta', label="MA(3)", linestyle=':', linewidth=1.0)
    ax.plot(df.index, df['close'].rolling(5).mean(), color='r', label="MA(5)")
    ax.plot(df.index, df['close'].rolling(7).mean(), color='black', label="MA(7)", linestyle=':')
    ax.plot(df.index, df['close'].rolling(10).mean(), color='olive', label="MA(10)", linestyle=':')
    ax.plot(df.index, df['close'].rolling(20).mean(), color='g', label="MA(20)")
    ax.plot(df.index, df['close'].rolling(25).mean(), color='g', label="MA(25)", linestyle=':')
    ax.plot(df.index, df['close'].rolling(60).mean(), color='b', label="MA(60)")
    ax.plot(df.index, df['close'].rolling(75).mean(), color='y', label="MA(75)")
    ax.plot(df.index, df['close'].rolling(100).mean(), color='orange', label="MA(100)")
    ax.plot(df.index, df['close'].rolling(200).mean(), color='gold', label="MA(200)")
    ax.plot(df.index, df['close'].rolling(300).mean(), color='pink', label="MA(300)")
    # ax.plot(df.index, pd.Series(df['close']).rolling(5).mean(), color='g', label="MA(5)")
    ax.plot(df.index, df['latest_max'], color='red', alpha=0.5, label="latest_max")
    ax.plot(df.index, df['latest_min'], color='blue', alpha=0.5, label="latest_min")

def scatterPoint(df, np, ax):
    #plt.scatter(50, 2500, s=100, marker="o",color='gold')
    ax.scatter(x= df.index,y = df['golden_5_20'],marker='o',color='gold', s=150, label="GC_5_20")
    ax.scatter(x= df.index,y = df['ded_5_20'],marker='o',color='black', s=150, label="DC_5_20")
    ax.scatter(x= df.index,y = df['golden_20_60'],marker='o',color='orange', s=150, label="GC_20_60")
    ax.scatter(x= df.index,y = df['ded_20_60'],marker='o',color='pink', s=150, label="DC_20_60")
    ax.scatter(x=df.index, y=df['golden_5_60'], marker='o', color='lime', s=150, label="GC_5_60")
    ax.scatter(x=df.index, y=df['ded_5_60'], marker='o', color='dodgerblue', s=150, label="DC_5_60")
    ax.scatter(x= df.index,y = df['golden_5_100'],marker='*',color='gold', s=150, label="GC_5_100")
    ax.scatter(x= df.index,y = df['ded_5_100'],marker='*',color='black', s=150, label="DC_5_100")

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

    #ax.scatter(x= df.index,y = df['latest_max'],marker='_',color='red', alpha=0.5, s=1000, label="latest_min")
    #ax.scatter(x= df.index,y = df['latest_min'],marker='_',color='blue', alpha=0.5, s=1000, label="latest_min")

    cnt9 = df['cnt9'].values
    #print(cnt9)
    for i, d in df.iterrows():
        #print(d.cnt9)
        marker = '$' + str(d.cnt9) + '$' if d.cnt9 is not np.nan else ""
        ax.scatter(x= i,y = d.hight + 25,marker=marker,color='black')
#        plt.scatter(x= df.index,y = df['hight'] + 75,marker='$' + str(9) + '$',color='black')

def set_signal(df, np):
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

        # 直近高値 # 直近安値
        now = df.index.get_loc(i)  # 行番号取得
        pre = now - 1 if now > 0 else 0
        now_dt, pre_dt = df.iloc[now].name, df.iloc[pre].name
        now_hight, pre_hight = df.loc[now_dt, 'hight'], df.loc[pre_dt, 'hight']
        now_low, pre_low = df.loc[now_dt, 'low'], df.loc[pre_dt, 'low']
        df.loc[i, 'latest_max'] = now_hight if now_hight > pre_hight else np.nan
        df.loc[i, 'latest_min'] = now_low if now_low < pre_low else np.nan
        # print(now, pre, now_dt, pre_dt, str(now_low) + ' < ' + str(pre_low))

    '''
    for i in df.index:
        now = df.index.get_loc(i)  # 行番号取得
        # 直近安値の次の陽線を抽出、その陽線の始値をA、
        # Aからの直近高値を抽出、その高値をB、
        # Bからの直近安値を抽出、その安値をC、
        # (B - C) / (B - A) = 30%以上の時、
        # B地点の高値を超える株価の時をエントリーポイントとする。
        latest_min = df.loc[i]['latest_min']
        post = now + 1
        post_dt = df.iloc[post].name
        post_op, post_cl = df.loc[post_dt, 'open'], df.loc[post_dt, 'close']
        if latest_min is not np.nan:
            if post < len(df):
                if hight(post_op, post_cl) is True:
                    A = df.loc[post_dt, 'open']
                    print('A:' + str(A))
    '''


def set_signal_shotgun(df, np):
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

def backtest(df, ax):
    for dt in df.index:
        df.loc[dt, 'uri'] = 0
        df.loc[dt, 'kai'] = 0
        df.loc[dt, 'total'] = 0
        now = df.index.get_loc(dt)  # 行番号取得
        pre = now - 1 if now > 0 else 0
        pre_uri = df.iloc[pre]['uri']
        pre_kai = df.iloc[pre]['kai']
        av5, av7, av10, av20, av60 = df['av_5'], df['av_7'], df['av_10'], df['av_20'], df['av_60']
        av5_p, av20_p, av60_p = df.iloc[pre]['av_5'], df.iloc[pre]['av_20'], df.iloc[pre]['av_60']
        op = df.loc[dt]['open']
        cl = df.loc[dt]['close']
        k_h = df.loc[dt]['k_hanshin']
        gk_h = df.loc[dt]['gk_hanshin']

        # 建玉 追加
        df.loc[dt, 'kai'] = int(pre_kai + 1) if k_h > 0 else int(pre_kai)
        df.loc[dt, 'uri'] = int(pre_uri + 1) if gk_h > 0 else int(pre_uri)

        # 建玉 決済
        gtrend = gain_trend(av5_p, av5[dt], av20_p, av20[dt], av60_p, av60[dt])
        if zone_PPP_1(av5[dt], av20[dt], av60[dt]) and gtrend is True and low(op, cl):
            df.loc[dt, 'total'] = int(pre_kai + df.iloc[now]['kai'])
            df.loc[dt, 'kai'] = 0
        else:
            df.loc[dt, 'total'] = int(pre_kai)

        dtrend = down_trend(av5_p, av5[dt], av20_p, av20[dt], av60_p, av60[dt])
        if zone_GPPP_1(av5[dt], av20[dt], av60[dt]) and dtrend is True and hight(op, cl):
            df.loc[dt, 'total'] = int(pre_uri + df.iloc[now]['uri'])
            df.loc[dt, 'uri'] = 0
        else:
            df.loc[dt, 'total'] = int(pre_uri)

        now_uri = df.iloc[now]['uri']
        now_kai = df.iloc[now]['kai']
        total = df.iloc[now]['total']
        if (now_uri != pre_uri or now_kai != pre_kai):
            ax.text(dt, op * 0.90, str(int(now_uri)) + '-' + str(int(now_kai)), size=10)
            ax.text(dt, 1200, str(int(total)), size=10)
    print(df)

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

def fetchDatas(code, start, end):
    conn = connectMysql()
    conn.ping(reconnect=True)
    # print(conn.is_connected())
    cur = conn.cursor()

    cnt_sql = "select count(id) From s" + str(code) + ";"
    cur.execute(cnt_sql)
    cnt_taple = cur.fetchone()
    cnt = cnt_taple[0]
    limit = 7600
    cnt = limit if cnt > limit else (cnt - 100) # 株価がlimit日数分ない場合、100日分を表示
    if start == 0 and end == 0:
        #where = " where id > " + str(cnt)
        where = " where date >= '2020-01-01' and date < '2021-01-01';"
    else:
        where = " where id > " + str(start) + " and id < " + str(end)

    sql = "select date, open, hight, low, close, power, End From s" + str(code) + where + ";"
    cur.execute(sql)
    rows = cur.fetchall()
    sdata = pd.read_sql(sql, conn, index_col='date')
    cur.close()
    conn.close()
    return sdata

def check_signal(df, code):
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

            ret.append(dt if df.iloc[now]['gk_hanshin'] > 0 and df.iloc[now]['akk'] > 0 else '')
            ret.append(dt if df.iloc[now]['gk_hanshin_2'] > 0 and df.iloc[now]['akk'] > 0 else '')
            #ret.append(dt if df.iloc[now]['gk_hanshin_5'] > 0 and df.iloc[now]['akk'] > 0 else '')
            #ret.append(dt if df.iloc[now]['gk_hanshin_6'] > 0 and df.iloc[now]['akk'] > 0 else '')
            break
    print(code, ret)
    if code == 9101 or code == 9104 or code == 9107:
        return code
    return code if ret.count('') < len(ret) else ''

def set_av(df):
    '''
    初期化
    :param df:
    :return:
    '''
    term_3, term_5, term_7, term_10, term_20, term_25, term_60, term_100 = 3, 5, 7, 10, 20, 25, 60, 100
    df['av_3'] = df['close'].rolling(window=term_3).mean()
    df['av_5'] = df['close'].rolling(window=term_5).mean()
    df['av_7'] = df['close'].rolling(window=term_7).mean()
    df['av_10'] = df['close'].rolling(window=term_10).mean()
    df['av_20'] = df['close'].rolling(window=term_20).mean()
    df['av_25'] = df['close'].rolling(window=term_25).mean()
    df['av_60'] = df['close'].rolling(window=term_60).mean()
    df['av_100'] = df['close'].rolling(window=term_100).mean()


def get_config():
    conf_file = "../../../source/repos/chart_gallery/stock_data/nikkei_225.csv"
    with open(conf_file, 'r') as config:
        cf = pd.read_csv(config, quotechar='"', header=38, index_col=0)
    return cf

def get_config_group():
    conf_file = "../../../source/repos/chart_gallery/stock_data/nikkei_225_group.csv"
    with open(conf_file, 'r') as config:
        cf = pd.read_csv(config, quotechar='"', header=0, index_col=0)
    return cf

def getCodeName(code):
    cf = get_config()
    i = cf.index.get_loc(code)
    gcode = cf.iloc[i]['gcode']
    gname = getGroupName(gcode)
    return gname + ':' + cf.iloc[i]['name']

def getGroupName(gcode):
    cfg = get_config_group()
    g = cfg.index.get_loc(gcode)
    return cfg.iloc[g]['gname']

def get_texts():
    plt.gcf().text(0.05, 0.55, "ylabel", rotation=90, backgroundcolor='yellow')
    plt.gcf().text(0.05, 0.90, "important", rotation=0, backgroundcolor='yellow')
    plt.gcf().text(0.45, 0.90, "xlabel", backgroundcolor='yellow')
    plt.gcf().text(0.40, 0.5, "arb text", backgroundcolor='yellow')

def set_bollinger_bands(df, ax, days=25):
    #https://engineeringnote.hateblo.jp/entry/python/finance/bollinger_bands
    x = df.index
    c = df['close']
    ma = c.rolling(window=days, min_periods=days-1).mean()
    vol = c.rolling(window=days, min_periods=days-1).std()
    bol1_p = pd.DataFrame(index=ma.index)
    bol1_p = ma + vol
    bol1_m = pd.DataFrame(index=ma.index)
    bol1_m = ma - vol

    bol2_p = pd.DataFrame(index=ma.index)
    bol2_p = ma + (vol * 2)
    bol2_m = pd.DataFrame(index=ma.index)
    bol2_m = ma - (vol * 2)

    ax.fill_between(x, bol1_p, bol1_m, color="turquoise", alpha=0.4, label="$1\sigma$")
    ax.fill_between(x, bol2_p, bol2_m, color="turquoise", alpha=0.3, label="$2\sigma$")

    #ax.plot(x, bol1_p, bol1_m, color='grey', alpha=0.3, label="1a", linestyle='-', linewidth=1.3)
    #ax.plot(x, bol2_p, bol2_m, color='black', alpha=0.3, label="2a", linestyle='-', linewidth=1.3)

def show_heatmap(codes):
    #codes = [9101, 9104, 9107, 4183, 9984, 6326]
    #codes = [9101, 9107, 6326, 1801, 1803, 2432, 3402, 3407, 4183, 4502, 5201, 5108, 5401, 5711, 5713, 6301, 6501, 6752, 6857, 7012, 7202, 7203, 7733, 8002, 8035, 8316, 8604, 8802, 9104, 9983, 9984]
    df0 = fetchDatas(9101, 0, 0)

    df = df0.copy()
    df = df.drop('open', axis=1)
    df = df.drop('hight', axis=1)
    df = df.drop('low', axis=1)
    df = df.drop('power', axis=1)
    df = df.drop('End', axis=1)
    # print(df_9101)%exit()

    for code in codes[201:225]:
        data = fetchDatas(code, 0, 0)
        df.insert(1, str(code), data['close'])

    corr_mat = df.corr(method='pearson')
    df.corr(method='pearson')

    import seaborn as sons
    sons.heatmap(corr_mat,
                vmin=-1.0,
                vmax=1.0,
                center=0,
                annot=True, # True:格子の中に値を表示
                fmt='.1f',
                xticklabels=corr_mat.columns.values,
                yticklabels=corr_mat.columns.values
               )
    plt.show()


