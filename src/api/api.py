
# from batch_20201214.reuse_position.reuse_position_lib import reuse_position_cash_history
from indicator_master.create_indicator_api_main import price_csv_append_indicator, \
    plot_indicator_from_csv
from norgate.ticker_price_downloader import pull_ticker_price_locally_norgate
import pandas as pd
from price_asset_master.lib.api.api import download_ticker
from trading_floor.api_trade.api import gen_trades_to_csv, \
    gen_trades_summary_from_csv
from util.util_finance import get_position_perf, compuate_alpha_beta_to_csv_img, \
    get_trade_perf_from_trades_csv
from util.util_time import df_filter_dy_date


def api_download_ticker(ticker, start, end, path_out, interval, norgate=False):
    """
    output: download given ticker to a csv
    interval : str
            Valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
    """
    if not norgate:
        download_ticker(ticker, start, end, path_out, interval)
    else:
        pull_ticker_price_locally_norgate(ticker, start, end, path_out)


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
    
    
def api_gen_trade_summary(
        trade_result_all_entry_path,
        trade_result_consecutive_entry_path,
        trade_summary_path,
        start_date, 
        end_date, 
):
    """
    Input: 2 trades file (consecutive & all_entry) CSV
    Output: trade summary output file CSV
    """
    gen_trades_summary_from_csv(
        trade_result_all_entry_path,
        trade_result_consecutive_entry_path,
        trade_summary_path,
        start_date, 
        end_date, 
    )

# 
# def api_build_portfolio_time_series(
#     start_date,
#     end_date,
#     trade_folder,
#     ticker_rank_folder,
#     indicator_folder,
#     output_folder,
#     stock_pick_strategy,
#     capacity,
# ):
#     """
#     this function insert all available trades into a n track portfolio
#     automatically insert new trades when there is vacancy
#     input: time range, trades files, price files
#     output: portfolio time series
#     """
#     reuse_position_cash_history(
#         start_date,
#         end_date,
#         trade_folder,
#         ticker_rank_folder,
#         indicator_folder,
#         output_folder,
#         stock_pick_strategy,
#         capacity,
#     )
    
    
def api_position_perf_from_csv(
    position_path, 
    start_date, 
    end_date, 
    date_col, 
    position_col,
    perf_output_path
):
    """
    input:
        file with position time series(date_col, position_col) , time range
    output:
        position perf: return, std, sharpe ratio, down down
    """
    df = pd.read_csv(position_path)
    df_filter = df_filter_dy_date(df,date_col,start_date,end_date)
    perf = get_position_perf(df_filter, date_col, position_col)
    perf['start_date'] = start_date
    perf['end_date'] = end_date
    #  convert to df
    rows = [perf]
    df = pd.DataFrame(rows)   
    df.to_csv(perf_output_path, index=False)
    

def api_trade_perf_from_trades_csv(trades_csv, output_perf_csv):
    """
    input: trades csv, each row is a trade
    output: trades perf, win lose rate, avg pnl, win_lose_pnl ratio
    """
    get_trade_perf_from_trades_csv(trades_csv, output_perf_csv)


def api_compuate_alpha_beta_to_csv_img(
    position_csv, 
    date_col, 
    position_col, 
    start_date, 
    end_date, 
    benchmark_ticker,
    period,
    result_path,
    norgate=False
):
    """
    this function computes alpha beta and saves to csv and img
    it take care the download of benchmark in the process
    input: time range, position data, benchmark
    output: alpha beta r-square of stat in csv and png
    period: year, month, week
    """
    compuate_alpha_beta_to_csv_img(
        position_csv, 
        date_col, 
        position_col, 
        start_date, 
        end_date, 
        benchmark_ticker,
        period,
        result_path,
        norgate
    )


