import pandas as pd
from util.util_finance import get_position_perf
from util.util_time import df_filter_dy_date


position_path = 'D:/f_data/batch_20211116/step8_portfolio_time_series/position.csv'
start_date = '2009-01-01'
end_date = '2022-01-01'

date_col = 'date'
position_col = 'roll'
perf_output_path = 'D:/f_data/temp/xxxx.csv'

def get_position_perf_from_csv(
    position_path, 
    start_date, 
    end_date, 
    date_col, 
    position_col,
    perf_output_path
):
    df = pd.read_csv(position_path)
    df_filter = df_filter_dy_date(df,date_col,start_date,end_date)
    perf = get_position_perf(df_filter, date_col, position_col)
    perf['start_date'] = start_date
    perf['end_date'] = end_date
    #  convert to df
    rows = [perf]
    df = pd.DataFrame(rows)   
    df.to_csv(perf_output_path, index=False)

        
        
get_position_perf_from_csv(
    position_path, 
    start_date, 
    end_date, 
    date_col, 
    position_col,
    perf_output_path
)        