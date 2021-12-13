from datetime import datetime
from functools import reduce

from api.api import api_trade_perf_from_trades_csv, \
    api_compuate_alpha_beta_to_csv_img, api_position_perf_from_csv, \
    api_download_ticker
import pandas as pd
import pandas as pd
from util.general_ui import plot_points_from_xy_list


# trades_csv = 'D:/f_data/perf/trades/SPY_1W_fmt_trades_all_entry_2.csv'
# output_perf_csv = 'D:/f_data/perf/result/spy_1w.csv'
# api_trade_perf_from_trades_csv(trades_csv, output_perf_csv)

position_csv = 'D:/f_data/perf/position/spy_1w.csv'
date_col = 'date'
position_col = 'experiment'
start_date = '2009-01-01' # DUE TO 3 YEARS OF HISTORICAL PERF COLLECTION 
end_date = '2022-01-01'
result_path = 'D:/f_data/perf/position_ab/spy_1w.csv'
benchmark_ticker = 'SPY'
period = 'week'

api_compuate_alpha_beta_to_csv_img(
    position_csv, 
    date_col, 
    position_col, 
    start_date, 
    end_date, 
    benchmark_ticker,
    period,
    result_path=result_path
)

# start_date = '2009-01-01' # DUE TO 3 YEARS OF HISTORICAL PERF COLLECTION 
# end_date = '2022-01-01'
# position_path = 'D:/f_data/perf/position/spy_prod_swin.csv'
# perf_output_path = 'D:/f_data/perf/position_result/spy_prod_swin.csv'
# api_position_perf_from_csv(
#     position_path=position_path, 
#     start_date=start_date, 
#     end_date=end_date, 
#     date_col='date', 
#     position_col='experiment',
#     perf_output_path=perf_output_path
# ) 


# # line chart
# path = 'D:/f_data/perf/position/spy20211207.csv'
# start_date = '2009-01-01' # DUE TO 3 YEARS OF HISTORICAL PERF COLLECTION 
# end_date = '2022-01-01'
# ticker = 'SPY'
# interval='1d'
# 
# 
# api_download_ticker(ticker, start_date, end_date, path, interval)
# path_posetion_spy_1w = 'D:/f_data/perf/position/spy_1w.csv'
# path_posetion_spy_prod_swin = 'D:/f_data/perf/position/spy_prod_swin.csv'
# path_posetion_swing = 'D:/f_data/perf/position/position_swing.csv'
# 
# df_spy = pd.read_csv(path)
# df_spy_1w = pd.read_csv(path_posetion_spy_1w)
# df_spy_prod_swin = pd.read_csv(path_posetion_spy_prod_swin)
# df_swing = pd.read_csv(path_posetion_swing)
# 
# df_spy['spy'] = df_spy['Close']
# df_spy_1w['spy_1w'] = df_spy_1w['experiment']
# df_spy_prod_swin['spy_1d_prod_swing_algo'] = df_spy_prod_swin['experiment']
# df_swing['portfolio_swing'] = df_swing['roll']
# df_spy['date']=df_spy.apply(lambda row : str(datetime.fromtimestamp(int(row['unixtime'])).strftime('%Y-%m-%d')), axis = 1)
# 
# print(df_spy.columns)
# print(df_spy_1w.columns)
# print(df_spy_prod_swin.columns)
# print(df_swing.columns)
# 
# dfList = [df_spy, df_spy_1w, df_spy_prod_swin, df_swing]
# merge = reduce(lambda x, y: pd.merge(x, y, on = 'date'), dfList)
# merge = merge[['date', 'spy','spy_1w','spy_1d_prod_swing_algo','portfolio_swing']]
# 
# merge['spy'] = merge['spy'] / merge.loc[0,'spy']
# merge['spy_1w'] = merge['spy_1w'] / merge.loc[0,'spy_1w']
# merge['spy_1d_prod_swing_algo'] = merge['spy_1d_prod_swing_algo'] / merge.loc[0,'spy_1d_prod_swing_algo']
# merge['portfolio_swing'] = merge['portfolio_swing'] / merge.loc[0,'portfolio_swing']
# 
# x_list = merge['date'].to_list()
# y_list = {
#     'spy':merge['spy'].to_list(),
#     'spy_1w':merge['spy_1w'].to_list(),
#     'spy_1d_prod_swing_algo':merge['spy_1d_prod_swing_algo'].to_list(),
#     'portfolio_swing':merge['portfolio_swing'].to_list(),
# }
# plot_points_from_xy_list(x_list, y_list)

