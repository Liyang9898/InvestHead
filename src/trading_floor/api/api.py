from batch_20201214.batch_trade_lib import gen_trades_based_on_price_with_indicator
from indicator_master.indicator_caching_lib import csv2df_indicator
from trading_floor.TradeInterface import genTradingBundleFromCSV
from util.util_time import df_filter_dy_date


def api_gen_trades(
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

    trades_consecutive.trades2CSV(trade_result_consecutive_entry_path)
    trades_all_entry.trades2CSV(trade_result_all_entry_path)
    


def api_gen_trades_summary(
    trades_all_entry_path,
#     trades_consecutive_entry_path,
#     start_date, 
#     end_date, 
):
    df_all_entry = genTradingBundleFromCSV(trades_all_entry_path)
    df_all_entry.printTradesSummary()