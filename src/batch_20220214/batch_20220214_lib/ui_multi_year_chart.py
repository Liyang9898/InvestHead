import pandas as pd
from util.general_ui import plot_bars_from_xy_list
from util.general_ui import plot_points_from_xy_list, plot_bar_set_from_xy_list
from util.util_pandas import df_normalize
from util.util_pandas import percent_increase_of_current_row
from util.util_time import df_filter_dy_date
from util.util_time import extract_period_start_from_df, PERIOD_CALENDAR_YEAR, \
    PERIOD_CALENDAR_MONTH


def gen_time_window_list(start_date, end_date):
    res = []
    start_year = int(start_date.split('-')[0])
    end_year = int(end_date.split('-')[0])
    for s in range(start_year, end_year):
        e = s + 1
        
        s = str(s) + '-01-01'
        e = str(e) + '-01-01'
        
        dic = {
            'start_date': s,
            'end_date': e
        }
        res.append(dic)
    return res
        

def gen_per_year_position_timeseries(
    start_date, 
    end_date,
    col_benchmark,
    col_portfolio,
    col_date,
    output_folder,
    input_timeseries
):
    df = pd.read_csv(input_timeseries)
    window_list = gen_time_window_list(start_date, end_date)

    for window in window_list:
        start_date = window['start_date']
        end_date = window['end_date']
        df_sub = df_filter_dy_date(df,col_date,start_date,end_date)
        if len(df_sub) == 0:
            continue
        
        x_list = df_sub[col_date].to_list()

        df_normalize(df_sub, col_portfolio)
        df_normalize(df_sub, col_benchmark)

        y_list_map = {
            col_portfolio: df_sub[col_portfolio].to_list(),
            col_benchmark: df_sub[col_benchmark].to_list()
        }
        
        title = f'position_timeseries_{start_date}_{end_date}'
        ui_path = f'{output_folder}{title}.html'
        plot_points_from_xy_list(x_list, y_list_map, title=title, path=ui_path, mode='lines+markers')


def gen_vs_benchmark(timeseries_path, col_date, col_benchmark, col_portfolio, out_path):
    df = pd.read_csv(timeseries_path)
    df = extract_period_start_from_df(df, col_date, PERIOD_CALENDAR_YEAR)
    
    
    percent_increase_of_current_row(df, col_benchmark)
    percent_increase_of_current_row(df, col_portfolio)
    df['after_hedge'] = df[f'{col_portfolio}_pct_increase'] - df[f'{col_benchmark}_pct_increase']
    # print(df[['date','portfolio_pct_increase','SPY_pct_increase','after_hedge']])
#     df.to_csv('D:/f_data/temp/c.csv', index=False)
#     print(df)
    
    df_p = df[df['after_hedge']>0]
    df_n = df[df['after_hedge']<0]
#     print(len(df_p)/(len(df_p)+len(df_n)), df_p['after_hedge'].sum(), df_n['after_hedge'].sum())
    win_pnl = round(df_p['after_hedge'].sum(), 2)
    lose_onl = round(df_n['after_hedge'].sum(), 2)
    win_potion = round(len(df_p)/(len(df_p)+len(df_n)), 2)
    
    title = f'PNL vs benchmark, win_potion={win_potion}%, win_pnl={win_pnl}%, lose_onl={lose_onl}%, x is end date of period'
    plot_bars_from_xy_list(x_list=df['date'].to_list(), y_list=df['after_hedge'].to_list(), title=title, path=out_path+'pnl_vs_benchmark.png')
    
    bar_m = {
        'portfolio':df[f'{col_portfolio}_pct_increase'].to_list(),
        'benchmark':df[f'{col_benchmark}_pct_increase'].to_list()
    }
    
    plot_bar_set_from_xy_list(df['date'].to_list(), bar_m, title=title, path=out_path+'yearly_return.html')
    
# start_date = '1970-01-01'
# end_date = '2022-01-01'
# col_benchmark = '$SPX'
# col_portfolio = 'portfolio'
# col_date = 'date'
# output_folder = 'D:/f_data/temp/x/'
# input_timeseries = 'D:/f_data/batch_20220214/step9_conclusion/baseball_card_position_time_series.csv'
# 
# 
# gen_per_year_position_timeseries(
#     start_date, 
#     end_date,
#     col_benchmark,
#     col_portfolio,
#     col_date,
#     output_folder,
#     input_timeseries
# )