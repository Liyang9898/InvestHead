import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from version_master.version import (
    t_20210420_ema21_ma50_gap_per_ticker
)

path = t_20210420_ema21_ma50_gap_per_ticker + 'merge/all_trades_all_entry.csv'
df_all = pd.read_csv(path)
fig = px.histogram(df_all, x="best_potential_pnl_percent")
fig.show()

tickers = df_all.ticker.unique()

ticker = 'AAPL'
df = df_all[df_all['ticker'] == ticker]


def best_profit_analysis(df, plot=True):
    df_best_pnl = df['best_potential_pnl_percent'].to_list()
    df_best_pnl.sort(reverse=True)

    percentile_dic = {}
    for percentile in range(0,100,1):
        idx = int(percentile*1.0/100.0*len(df_best_pnl))
        val = df_best_pnl[idx]
        percentile_dic[percentile] = val
        
    if plot:
        trace1 = go.Histogram(
            x=df_best_pnl, 
            histnorm='percent',
            xbins=dict(
                start=0.0,
                end=1,
                size=0.005
            ),
        )
        fig = go.Figure(data=[trace1])
        fig.show()
    
    return percentile_dic
    

def percentile_4p(percentile_threshold, percentile_dic):
    p = 0
    for k, v in percentile_dic.items():
        if v < percentile_threshold:
            return p
        p = k
    return -999
        
        
def all_ticker_4p_percentile(df_all):
    res = {}
#     p90_res = {}
#     p95_res = {}
    p83_res = {}
    tickers = df_all.ticker.unique()
    for ticker in tickers:
        df = df_all[df_all['ticker'] == ticker]
        percentile_dic = best_profit_analysis(df, False)
        p83 = percentile_dic[int(81.0/100.0*len(percentile_dic))]
#         p95 = percentile_dic[int(95.0/100.0*len(percentile_dic))]
#         p90 = percentile_dic[int(90.0/100.0*len(percentile_dic))]
        p = percentile_4p(0.04, percentile_dic)
        res[ticker] = p
        p83_res[ticker] = p83
#         p90_res[ticker] = p90
#         p95_res[ticker] = p95
    return {
        '4p':res,
        'p83':p83_res,
#         'p90':p90_res,
#         'p95':p95_res,
    }


best_profit_analysis(df_all)
#         
# percentile_dic = best_profit_analysis(df)
# p = percentile_4p(0.04, percentile_dic)
# print(p)
# for k, v in percentile_dic.items():
#     print(k, v)

  
v = all_ticker_4p_percentile(df_all)
# print(v)
xx=list(v['4p'].values())
p83=list(v['p83'].values())
# p90=list(v['p90'].values())
# p95=list(v['p95'].values())
print(p83)
print(len(p83))
trace1 = go.Histogram(
    x=p83,
    histnorm='percent',
    xbins=dict(
        start=0.0,
        end=0.1,
        size=0.005
    ),
    name='83'
)
fig = go.Figure(data=[trace1])
fig.show()