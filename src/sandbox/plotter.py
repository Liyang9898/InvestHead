import pandas as pd
from util.general_ui import plot_points_from_xy_list
from util.util_pandas import df_normalize
from util.util_time import df_filter_dy_date


path = 'D:/f_data/batch_archive/20220318_russell1000_1991_2022_filter/step9_conclusion/baseball_card_position_time_series.csv'
# path = 'D:/f_data/batch_archive/20220318_russell1000_1991_2022_normal/step9_conclusion/baseball_card_position_time_series.csv'
df = pd.read_csv(path)
print(df)  
date_col = 'date'
s = '2021-11-23'
e = '2022-01-01'
df = df_filter_dy_date(df,date_col,s,e)
df_normalize(df, '$SPX')
df_normalize(df, 'portfolio')


x_list = df['date'].to_list()
y_list_map = {
    'spy':df['$SPX'].to_list(),
    'port':df['portfolio'].to_list()
}
plot_points_from_xy_list(x_list, y_list_map, title='default', path=None, mode='markers')