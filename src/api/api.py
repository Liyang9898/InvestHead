
from indicator_master.create_indicator_api_main import price_csv_append_indicator, \
    plot_indicator_from_csv
from price_asset_master.lib.api.api import download_ticker
from trading_floor.api_trade.api import gen_trades_to_csv


def api_download_ticker(ticker, start, end, path_out, interval):
    """
    output: download given ticker to a csv
    interval : str
            Valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
    """
    download_ticker(ticker, start, end, path_out, interval)
    

def api_gen_indicator(input_path, output_path, start_date, end_date):
    """
    input: given raw price csv, 
    output: generate price with indicator
    """
    price_csv_append_indicator(
        input_file_path=input_path, 
        output_file_path=output_path,
        start_time=start_date, 
        end_time=end_date,
        plot_chart=False
    )
    
    
def api_plot_indicator_from_csv(indicator_path):
    """
    Input indicator file
    draw the plot
    """
    plot_indicator_from_csv(indicator_path)
    
    
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
    Input: indicator file
    Output: trades in 2 mode: all_entry & consecutive
    """    
    gen_trades_to_csv(
        ticker,
        start_date, 
        end_date, 
        strategy,
        indicator_file_path, 
        trade_result_all_entry_path, 
        trade_result_consecutive_entry_path, 
    )
# api_gen_trades()
# api_download_ticker()