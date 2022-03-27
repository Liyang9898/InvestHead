import pandas as pd
from util.general_ui import plot_bars_from_xy_list, plot_line_from_xy_list
from util.util_time import gen_date_list_in_range


# import numpy as np
path = 'D:/f_data/analysis/20220312_ibkr/closed_formatted.csv'
df = pd.read_csv(path)
df = df.dropna()

df['start'] = pd.to_datetime(df['date'])
df['end'] = pd.to_datetime(df['close date'])
df.reset_index(inplace=True, drop=True)
print(df)

pos_cnt = {}
for i in range(len(df)):
    s = str(df.loc[i, 'start']).split(' ')[0]
    e = str(df.loc[i, 'end']).split(' ')[0]
    l = gen_date_list_in_range(s, e, end_inclusive=True)
#     print(s, e, l)
    for d in l:
        if d not in pos_cnt.keys():
            pos_cnt[d] = 0
        pos_cnt[d] = pos_cnt[d] + 1
        
print(pos_cnt)
x_list = list(pos_cnt.keys())
y_list = list(pos_cnt.values())
plot_line_from_xy_list(x_list, y_list, title='default')