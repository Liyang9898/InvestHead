'''
Created on Jun 11, 2020

@author: leon
'''
from util import util
from indicator_master.constant import trade_summary_interface
import pandas as pd

all_stocks_trade_summary_file="D:/f_data/download_yfinance_trades_summary_conclusion/trade_summaries.csv"
df=util.load_df_from_csv(all_stocks_trade_summary_file, ['ticker','avg_daily_volumn']+trade_summary_interface)
print("total stock: "+str(len(df)))


# move these function some where
# extract trading summary from a list of tickers
def getTradeSummaryStr(
    ticker,
    win_rate,
    lose_rate,
    neutral_rate,
    total_trades,
    win,
    lose,
    neutral,
    win_pnl_p,
    lose_pnl_p
):
    trade_summary_str="""
    [{ticker}] win trades:{win}({win_rate}), lose trades:{lose}({lose_rate}), neutral trades:{neutral}({neutral_rate}), total trades:{total}
    win_pnl:{win_pnl_p}, lose_pnl:{lose_pnl_p}""".format(
        ticker=ticker,
        win_rate="{:.2%}".format(win_rate),
        lose_rate="{:.2%}".format(lose_rate),
        neutral_rate="{:.2%}".format(neutral_rate),
        total=total_trades,
        win=win,
        win_pnl_p="{:.2%}".format(win_pnl_p),
        lose=lose,
        lose_pnl_p="{:.2%}".format(lose_pnl_p),
        neutral=neutral
    )
    return trade_summary_str

def dfrow2tradeSummaryStr(dfrow):
    dfstr=getTradeSummaryStr(
        ticker=dfrow['ticker'],
        win_rate=dfrow['win_rate'],
        lose_rate=dfrow['lose_rate'],
        neutral_rate=dfrow['neutral_rate'],
        total_trades=dfrow['total_trades'],
        win=dfrow['win'],
        lose=dfrow['lose'],
        neutral=dfrow['neutral'],
        win_pnl_p=dfrow['win_pnl_p'],
        lose_pnl_p=dfrow['lose_pnl_p']
    )
    return dfstr


def printTradeSummaryFromTicker(df, ticker):
    df_target=(df.loc[(df['ticker']==ticker)].reset_index(drop=True)).loc[0]
    s=dfrow2tradeSummaryStr(df_target)
    print(s)

ticker_list = ['FB','GOOG','AMZN','AMD']

for ticker in ticker_list:
    printTradeSummaryFromTicker(df, ticker)