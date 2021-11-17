'''
Created on Jan 12, 2020

@author: leon
'''
from plot.util import histogram, pnltimeseries, plottimeseries,pnltotaltimeseries,pnldistribution,plotcategory,pnldistributionagg,plotpie,pnlma,plottimeseriesmultiline

def compute_stat(trades, plot,dss):
    
    win_count = 0.0
    lose_count = 0.0  
    neutual_cnt = 0.0
    pnl = 0.0
    win_pull_back_distribution = []
    for ds in dss:
        if trades[ds]['pnl'] == 0:
            neutual_cnt = neutual_cnt + 1
        elif trades[ds]['pnl'] < 0:
            lose_count =lose_count + 1
        else:
            win_count =win_count + 1
            win_pull_back_distribution.append(trades[ds]['in_market_low'])
        pnl = pnl + trades[ds]['pnl']

    win_rate = float(win_count) / (float(win_count) + float(lose_count)+float(neutual_cnt))
    win_rate_exclude_neutral = float(win_count) / (float(win_count) + float(lose_count))
    e_daily_10_contract = pnl / (float(win_count) + float(lose_count)+float(neutual_cnt)) / 2 *1000
    monthly = e_daily_10_contract * 20
    
    
    

    
    
    
    pnldic = pnltimeseries(trades)
    pnlaggdic = pnltotaltimeseries(trades)
    pnlma_20 = pnlma(pnldic,20)
    pnlma_10 = pnlma(pnldic,10)
    pnlma_5 = pnlma(pnldic,5)
    dis = pnldistribution(trades)
    disagg = pnldistributionagg(trades)
    if plot:
        plottimeseries(pnldic,'daily pnl')
        plottimeseries(pnlaggdic,'pnl agg')
        # plottimeseries(pnlma_20,'ma20 pnl')
        # plottimeseries(pnlma_10,'ma10 pnl')
        # plottimeseries(pnlma_5,'ma5 pnl')
        plottimeseriesmultiline({'ma20':pnlma_20['ma'],'ma10':pnlma_10['ma'],'ma5':pnlma_5['ma']},'ma pnl')
        plottimeseriesmultiline({'rate20':pnlma_20['rate'],'rate10':pnlma_10['rate'],'rate5':pnlma_5['rate']},'ma pnl')
    
        # plotcategory(dis)
        # plotcategory(disagg)
        plotpie(dis, 'change')
        plotpie(disagg, 'amount of money')
        print(pnlma_20['ma'])
#         a = sum(list(pnlma_20['ma'].values())) / len(list(pnlma_20['ma'].values()))
#         print(win_pull_back_distribution)
#         histogram(win_pull_back_distribution)
    pnl_ma_20_avg=0
    rate_ma_20_avg=0

    if len(list(pnlma_20['ma'].values())) is not 0:
       pnl_ma_20_avg=sum(list(pnlma_20['ma'].values())) / len(list(pnlma_20['ma'].values())),
    if len(list(pnlma_20['rate'].values())) is not 0:
        rate_ma_20_avg=sum(list(pnlma_20['rate'].values())) / len(list(pnlma_20['rate'].values())),
#     if len(list(pnlma_20['ma'].values())) is not 0:  
#         pnl_ma_20_positive_rate=rate_of_positive(pnlma_20['ma'].values(), 0),
#     if len(list(pnlma_20['ma'].values())) is not 0:
#         rate_ma_20_positive_rate=rate_of_positive(pnlma_20['rate'].values(), 0.5),
    
    return {
        
        'avg_monthly_gain':monthly,
        'win_rate':win_rate,
        'win_rate_exclude_neutral':win_rate_exclude_neutral,
        'win':win_count,
        'lose':lose_count,
        'neutual':neutual_cnt,
        'pnl':pnl,
        'daily_balance_10_contract':e_daily_10_contract,
        
        
        'pnl_ma_20_avg': pnl_ma_20_avg,
        'rate_ma_20_avg':rate_ma_20_avg,
          
        'pnl_ma_20_positive_rate':rate_of_positive(pnlma_20['ma'].values(), 0),
        'rate_ma_20_positive_rate':rate_of_positive(pnlma_20['rate'].values(), 0.5),
    }

def rate_of_positive(data, positive):
    if len(data) is 0:
        return 0
    count = 0
    for x in data:
        if x > positive:
            count = count + 1
    return count / len(data)
        