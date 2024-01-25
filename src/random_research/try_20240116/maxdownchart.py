'''
Created on Jan 16, 2024

@author: spark
'''
import pandas as pd
from util.general_ui import plot_line_from_xy_list


path_position_record='C:/f_data/temp/position_list_strat_param_20211006_ma_max_drawdown_cut.csv'
df=pd.read_csv(path_position_record)
print(df)

max = 0
x_list=[]
y_list=[]
print(x_list)
# df['down_from_max']
for i in range(len(df)):
    date = df.loc[i, "date"]
    x_list.append(date)
    v = df.loc[i, "baseline"]
    if v > max:
        max = v
    down_from_max = v/max-1
    y_list.append(down_from_max)
    # print(down_from_max)
    
    
plot_line_from_xy_list(x_list, y_list, title='down from max')