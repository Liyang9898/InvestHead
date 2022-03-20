import pandas as pd
from util.general_ui import plot_points_from_xy_list
from util.util_time import gen_date_list_in_range


def gen_daily_position_cnt_from_trade_list(df_trade):
    daily_position_cnt = {}
    for i in range(len(df_trade)):
        start_date = str(df_trade.loc[i, 'entry_ts']).split(' ')[0]
        end_date = str(df_trade.loc[i, 'exit_ts']).split(' ')[0]

        date_list = gen_date_list_in_range(start_date, end_date, False)
        for date in date_list:
            if date not in daily_position_cnt.keys():
                daily_position_cnt[date] = 0
            daily_position_cnt[date] = daily_position_cnt[date] + 1  
    return daily_position_cnt    
        

df = pd.read_csv('D:/f_data/batch_20220310/step8_portfolio_time_series/intermediate_per_track_trades.csv')
# print(df)


daily_position_cnt = gen_daily_position_cnt_from_trade_list(df)
x_list = list(daily_position_cnt.keys())
y_list_map = {'cnt': list(daily_position_cnt.values())}
plot_points_from_xy_list(x_list, y_list_map, title='default', path=None, mode='markers')
# for d, cnt in daily_position_cnt.items()():
#     print(d,cnt)
print(daily_position_cnt)