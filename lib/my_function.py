def pointCross(df, status = '5_20', str = '', current_flag = 0, previous_flag = 1):
    """ ゴールデンクロス/デッドクロスしたタイミングの抽出
    """
    if (status == '5_20'):
        ma = {'pointString':str+'_5_20', 1:'av_5', 2:'av_20'}
    elif (status == '20_60'):
        ma = {'pointString':str+'_20_60', 1:'av_20', 2:'av_60'}
    elif (status == '5_60'):
        ma = {'pointString': str + '_5_60', 1: 'av_5', 2: 'av_60'}
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

        '''
        if (g5x20_dt and g20x60_dt):
            #print(g5x20_dt, g20x60_dt)
            ax.axvspan(g5x20_dt, g20x60_dt, facecolor=color, alpha=0.1)
            if (g5x60_dt and g20x60_dt): ax.axvspan(g5x60_dt, g20x60_dt, facecolor=color, alpha=0.1)
            g5x20_dt = g5x60_dt = g20x60_dt = ''
        '''
        '''

        if (g20x60_dt and d5x20_dt):
            print(g20x60_dt, d5x20_dt)
            #ax.axvspan(g20x60_dt, d5x20_dt, facecolor='blue', alpha=0.3)
        '''
    dts.append({'end': 'none'})
    print(dts)
    '''
    i = 0
    for dic in dts:
        for k, v in dic.items():
            if (k is 'g5x20'):
                s_d, e_d = v, dts[i+1].get('g5x60')
                if (s_d and e_d): ax.axvspan(s_d, e_d, facecolor='red', alpha=0.1)
            elif (k is 'g5x60'):
                s_d, e_d = v, dts[i+1].get('g20x60')
                if (s_d and e_d): ax.axvspan(s_d, e_d, facecolor='red', alpha=0.2)
            elif (k is 'g20x60'):
                s_d, e_d = v, dts[i+1].get('d5x20')
                if (s_d and e_d): ax.axvspan(s_d, e_d, facecolor='red', alpha=0.3)
            elif (k is 'd5x20'):
                s_d, e_d = v, dts[i+1].get('d5x60')
                if (s_d and e_d): ax.axvspan(s_d, e_d, facecolor='blue', alpha=0.1)
            elif (k is 'd5x60'):
                s_d, e_d = v, dts[i+1].get('d20x60')
                if (s_d and e_d): ax.axvspan(s_d, e_d, facecolor='blue', alpha=0.2)
            elif (k is 'd20x60'):
                s_d, e_d = v, dts[i+1].get('g5x20')
                if (s_d and e_d): ax.axvspan(s_d, e_d, facecolor='blue', alpha=0.3)
            i = i+1
    '''
    import copy
    dts2 = copy.copy(dts)
    dts2.append({'end': 'none'})
    ret = list()
    i = 0
    for dic in dts:
        for k, v in dic.items():
            #print(list(dts[i].keys())[0], list(dts[i].values())[0], list(dts2[i+1].values())[0])
            ret.append([list(dts[i].keys())[0], list(dts[i].values())[0], list(dts2[i+1].values())[0]])
        i = i + 1
    print(ret)

    for k, sdt, edt in ret:
        print(k, sdt, edt)
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

