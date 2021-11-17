import pandas as pd
from util.general_ui import plot_lines_from_xy_list
from util.util_finance import  get_position_perf, compute_alpha_beta_from_position, \
    get_line_speed, get_line_speed_chart
from util.util_finance_chart import get_drop_chart, get_return_chart_period, \
    plot_chart_normalized_on_start, plot_chart_normalized_on_abs_return
from util.util_pandas import df_normalize


################################################self strategy##################################################
###############################################################################################################
strategy_name='strat_param_20211006' # same as strat_param_swing_2150in_2150out_plain
# strategy_name='strat_param_20211006_ma_max_drawdown_cut_neutral_out'
# strategy_name='temp'
path_position_record = f'D:/f_data/temp/position_list_{strategy_name}.csv'
path_position_record = 'D:/f_data/operation_test/2021-10-12/indicator/spy_iwf.csv'

# path_position_record = f'D:/f_data/temp/position_list_strat_param_20211006.csv'
###############################################################################################################
###############################################################################################################


###########################################JP private client###################################################
###############################################################################################################
# ticker_list = [
#     'iwf', 
#     'JLGMX',
#     'JMGMX',
#     'JGSMX',
#     'JSDRX'
# ]
# 
# strategy_name='iwf'
# path_position_record = f'D:/f_data/temp/jp_portfolio/{strategy_name}_downloaded_raw.csv'
###############################################################################################################
###############################################################################################################


df = pd.read_csv(path_position_record)
# df = df[df['date'] > '2017-01-01'].copy()
# df = df[(df['date'] < '2021-08-01') & (df['date'] > '2009-08-01')].copy()
df.reset_index(inplace=True, drop=True)
# print(df)

df_normalize(df=df, normalize_col='baseline')
df_normalize(df=df, normalize_col='experiment')


info_base = get_position_perf(df, 'date', 'baseline')
info_exp = get_position_perf(df, 'date', 'experiment')
  
print('===============baseline===============')
for k,v in info_base.items():
    print(k, v)
print('===============experiment===============')
for k,v in info_exp.items():
    print(k, v)

# alpha beta
print('===============Alpha Beta===============')
alpha_beta_year = compute_alpha_beta_from_position(df=df, date_col='date', base_col='baseline', exp_col='experiment', period='year', plot=False)
alpha_beta_month = compute_alpha_beta_from_position(df=df, date_col='date', base_col='baseline', exp_col='experiment', period='month', plot=False)
alpha_beta_week = compute_alpha_beta_from_position(df=df, date_col='date', base_col='baseline', exp_col='experiment', period='week', plot=False)
print('alpha_beta_year', alpha_beta_year)
print('alpha_beta_month', alpha_beta_month)
print('alpha_beta_week', alpha_beta_week)




# ========== plot ==========
# plot_chart_normalized_on_start(df, 'date', 'baseline', 'experiment')
# plot_chart_normalized_on_abs_return(df, 'date', 'baseline', 'experiment')

# get_drop_chart(df=df, date_col='date', base_col='baseline', exp_col='experiment')
# get_line_speed_chart(df=df, date_col='date', baseline_col='baseline', position_col='experiment', time_bucket=1)
# get_return_chart_period(df=df, date_col='date', base_col='baseline', exp_col='experiment', period='month')
# get_return_chart_period(df=df, date_col='date', base_col='baseline', exp_col='experiment', period='week')
# get_return_chart_period(df=df, date_col='date', base_col='baseline', exp_col='experiment', period='year')
# plot_lines_from_xy_list(x_list=df['date'].to_list(), y_list_map={'baseline':df['baseline'].to_list(),'experiment':df['experiment'].to_list()}, title='position')

