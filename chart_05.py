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
from lib import my_function as myf


def init():
    """ 初期化
    """
    global fig, ax
    fig = plt.figure()
    #fig = plt.figure(figsize=(24,10), dpi=300, facecolor='w')
    ax = plt.subplot()


def main(code):
    """ main関数
    """
    global fig, ax
    ohlc = np.vstack((range(len(df)), df.values.T)).T
    mpf.candlestick_ohlc(ax, ohlc, width=0.7, colorup='red', colordown='green')
    print(code)
    w = dt.datetime.strptime(df.index[0], '%Y-%m-%d').weekday()
    xtick0 = (5 - w) % 5

    # グラフのx軸の日付の調整
    # plt.xticks(range(xtick0,len(df),5), [x.strftime('%Y-%m-%d') for x in df.index][xtick0::5])
    # plt.xticks(range(xtick0,len(df),5), [dt.datetime.strptime(x, '%Y-%m-%d') for x in df.index][xtick0::5])
    plt.xticks(range(xtick0, len(df), 5), [x for x in df.index][xtick0::5])

    # 出来高のチャートをプロット
    ax2 = ax.twinx()
    mpf.volume_overlay(ax2, df['open'], df['close'], df['power'],
                       width=0.5, colorup="yellow", colordown="yellow", alpha=0.3)
    ax2.set_xlim([0, df.shape[0]])

    # 出来高チャートは下側25%に収める
    ax2.set_ylim([0, df['power'].max() * 7])
    ax2.set_ylabel('power')


def drow_graph(code):
    init()  # グラフ初期化
    main(code)  # グラフメイン関数
    # fig.suptitle(str(code) + ':' + myf.getCodeName(code), fontname="MS Gothic")  # title 表示
    fig.suptitle(str(code))  # title 表示

    df['golden_5_20'] = df['golden_20_60'] = df['golden_5_60'] = df['golden_5_100'] = df['ded_5_20'] = df['ded_20_60'] = df['ded_5_60'] = df['ded_5_100'] = 0
    myf.pointCross(df, '5_20', 'golden')
    myf.pointCross(df, '20_60', 'golden')
    myf.pointCross(df, '5_60', 'golden')
    myf.pointCross(df, '5_100', 'golden')
    myf.pointCross(df, '5_20', 'ded')
    myf.pointCross(df, '20_60', 'ded')
    myf.pointCross(df, '5_60', 'ded')
    myf.pointCross(df, '5_100', 'ded')

    # myf.plotMA(ax, df)  # 移動平均線表示
    myf.plotMA2(ax, df, code)  # 移動平均線表示
    myf.scatterPoint(df, np, ax)  # シグナル表示

    ax.grid()
    ax.set_xlim(-1, len(df))
    # ax.text(20, 2000, 'test', size=20) # text表示
    fig.autofmt_xdate()

    myf.zone_color_golden(df, np, ax)
    # myf.zoneColor(df, np, ax, 'golden')  # PPPゾーンの表示
    # myf.zoneColor(df, np, ax, 'ded')  # PPPゾーンの表示


cf = myf.get_config()
codes = list()
codes = [code for code in cf.index]
# print(myf.getCodeName(1332))%exit()
# myf.show_heatmap(codes)%exit()

mpl.rcParams['figure.figsize'] = [20.0, 10.0]
#codes = [9101]
#codes = [9101, 9104, 9107]
codes = [9101, 9104, 9107, 6326, 4183]
#codes = [9101, 9104, 9107, 4021, 4183, 4005, 4188, 4911, 3407, 4042, 6988, 3405, 4061, 4208, 4272, 4004, 4631, 4043, 4901, 4452, 4063, 8630, 8750, 8795, 8725, 8766, 8697, 8253, 8830, 8804, 8801, 3289, 8802, 9022, 9021, 9020, 9009, 9005, 9007, 9008, 9001, 9062, 9064]
#codes = [1801, 1803, 2432, 3402, 3407, 4183, 4502, 5012, 5201, 5108, 5401, 5711, 5713, 6301, 6501, 6752, 6857, 7012, 7202, 7203, 7733, 8002, 8035, 8316, 8591, 8604, 8802, 9104, 9983, 9984]
ret_codes = list()
for code in codes:
    start, end = 0, 0
    #start, end = 7400, 7600
    #start, end = 7500, 7700
    start, end = 8050, 8250
    sdata = myf.fetchDatas(code, start, end)  # DBから株価データ取得

    df = sdata.copy()
    df_ = df.copy()

    new = [dt.datetime.strptime(i, '%Y-%m-%d') for i in df_.index]
    df_.index = [mdates.date2num(i) for i in new]

    #df_.index = mdates.date2num(df_.index)
    data = df_.reset_index().values

    myf.set_av(df)  # 移動平均線設定
    myf.set_signal(df, np)  # シグナルの表示
    myf.set_signal_shotgun(df, np)  # シグナルの表示
    # ret_code = myf.check_signal(df, code) # シグナル点灯確認
    ret_code = code
    if ret_code is not '':
        drow_graph(ret_code)
        #plt.savefig('./charts.tmp/20200912/' + str(ret_code) + '.png')
        img_name = str(ret_code) + '_' + str(start) + '-' + \
            str(end) if start != 0 and end != 0 else str(ret_code)
        #img_name = img_name + '_' + myf.getCodeName(code).replace(':', '_')
        # myf.get_texts()
        ax.legend()
        #myf.set_bollinger_bands(df, ax, 25)
        latest_dir = '/var/www/tmp/git_repo/chart_analytics/charts/20220901/'
        if os.path.exists(latest_dir) == False:
            # print(latest_dir)%exit()
            os.mkdir(latest_dir)
        plt.savefig(latest_dir + img_name + '.png',
                    facecolor='azure', bbox_inches='tight', pad_inches=0)
        #plt.savefig('./charts/20220621/' + img_name + '.png', facecolor='azure', bbox_inches='tight', pad_inches=0)

    # myf.backtest() # シグナル発生時に建玉操作をシミュレーションする

print(ret_codes)
# base
#ax.text('2020-09-07', 2800, str('test'), size=10)
# plt.legend()
# plt.show()
