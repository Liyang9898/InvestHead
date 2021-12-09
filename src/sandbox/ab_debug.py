from datetime import datetime

from api.api import api_download_ticker
import pandas as pd
from util.util_finance import compute_alpha_beta_from_position, \
    compuate_alpha_beta_to_csv_img
from util.util_time import df_filter_dy_date


path = 'D:/f_data/perf_compare/fb_vs_spy_2021-10-17_18-02-27_3446/asset/merge.csv'
df = pd.read_csv(path)
# print(df)
date_col='date'
period = 'month'


base_col='baseline'
exp_col = 'experiment'

# base_col='experiment'
# exp_col = 'baseline'

print(df)





# x = compute_alpha_beta_from_position(df, date_col, base_col, exp_col, period)
# print(x)
position_csv = 'D:/f_data/batch_20211116/step8_portfolio_time_series/position.csv'
date_col = 'date'
position_col = 'roll'
START_DATE = '2006-01-01'
ANALYSIS_START_DATE = '2009-01-01' # DUE TO 3 YEARS OF HISTORICAL PERF COLLECTION 
END_DATE = '2022-01-01'
result_path = 'D:/f_data/temp/ab/'

compuate_alpha_beta_to_csv_img(
    position_csv, 
    date_col, 
    position_col, 
    start_date=ANALYSIS_START_DATE, 
    end_date=END_DATE, 
    benchmark_ticker='spy',
    period='year',
    result_path=result_path
)
