from batch_20201214.batch_trade_lib import gen_trades_based_on_price_with_indicator
from indicator_master.indicator_caching_lib import csv2df_indicator
import pandas as pd
from trading_floor.TradeInterface import genTradingBundleFromCSV, \
    genTradingBundleFromDataframe, merge_trade_summary
from util.util_pandas import dict_to_one_row_df
from util.util_time import df_filter_dy_date


def gen_trades_to_csv(
    ticker,
    start_date, 
    end_date, 
    strategy,
    indicator_file_path, 
    trade_result_all_entry_path, 
    trade_result_consecutive_entry_path, 
):
    """
    given indicator, date range and strategy, 
    generate trades for all entries and consecutive entries,
    save result in csv in given folder
    """
    
    df = csv2df_indicator(indicator_file_path)
    price_with_indicator = df_filter_dy_date(df,'date', start_date, end_date)
    trades = gen_trades_based_on_price_with_indicator(
        ticker,
        price_with_indicator, 
        strategy,
    )
    trades_consecutive = trades['trades_consecutive']
    trades_all_entry = trades['trades_all_entry']
 
    trades_all_entry.trades2CSV(trade_result_all_entry_path)
    trades_consecutive.trades2CSV(trade_result_consecutive_entry_path)
    
    
def df_filter_trades_dy_date(df,s,e):
    # create a copy of input df and filter by date range, and return
    s = s + ' 00:00:00'
    e = e + ' 00:00:00'
    df = df.loc[(df['entry_ts']>=s) & (df['entry_ts']<=e)]
    df_filtered = df.copy()
    df_filtered.reset_index(inplace=True,drop=True)
    return df_filtered


def gen_trades_summary_from_csv(
    trades_all_entry_path,
    trades_consecutive_entry_path,
    trade_summary_path,
    start_date, 
    end_date, 
):
    """
    key metric:
    all_universe_win_rate
    anual_return_avg
    win_lose_pnl_ratio
    --------
    all_universe_lose_rate
    average_trade_win_pnl_p
    average_trade_lose_pnl_p
    """
    df_all_entry = pd.read_csv(trades_all_entry_path)
    df_consecutive = pd.read_csv(trades_consecutive_entry_path)
    
    df_all_entry = df_filter_trades_dy_date(df_all_entry, start_date, end_date)
    df_consecutive = df_filter_trades_dy_date(df_consecutive, start_date, end_date)
    
    trades_all_entry = genTradingBundleFromDataframe(df_all_entry)
    trades_consecutive = genTradingBundleFromDataframe(df_consecutive)

    over_all_summary = merge_trade_summary(trades_consecutive.tradeSummary2dict(),trades_all_entry.tradeSummary2dict())
    
    over_all_summary['key_metric_win_rate'] = over_all_summary['all_universe_win_rate']
    over_all_summary['key_metric_annual_avg_return'] = over_all_summary['anual_return_avg']
    over_all_summary['key_metric_win_lose_pnl_ratio'] = over_all_summary['win_lose_pnl_ratio']
    df = dict_to_one_row_df(over_all_summary)
    df.to_csv(trade_summary_path, index=False)

    return over_all_summary
    
