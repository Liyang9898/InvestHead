
import pandas as pd
from datetime import datetime

def ts_position_dict_to_dataframe(data_dict):
    data_list = list(data_dict.items())
    df = pd.DataFrame(data_list,columns=['date', 'position'])
    return df


def ts_position_dict_to_csv(data_dict, path):
    df = ts_position_dict_to_dataframe(data_dict)
    df.to_csv(path, index=False)
    
    
def ts_position_dicts_to_dataframe(price_dict, position_dict, path):
    rows = []
    for t, p_base in price_dict.items():
        date_str = t.split(' ')[0]
#         dt = datetime.strptime(date_str, '%Y-%m-%d')
#         weekday = dt.weekday() # Monday = 0
#         year = dt.year
#         month = dt.month
#         day = dt.day
#         
#         is_week_start = False
#         is_month_start = False
#         is_year_start = False
#         
#         if weekday == 0:
#             is_week_start = True
#             
#         if day == 1:
#             is_month_start = True
#         
#         if day == 1 and month == 1:
#             is_year_start = True
        
        p_position = position_dict[t]
        row = {
            'date':date_str,
            'baseline':p_base,
            'experiment':p_position,
#             'is_week_start':is_week_start,
#             'is_month_start':is_month_start,
#             'is_year_start':is_year_start,
        }
        rows.append(row)
    df = pd.DataFrame(rows)
    df.to_csv(path, index=False)
    
    
    
# data_dict = {"a": 1, "b": 2, "c": 3}
# 
# path = 'D:/f_data/temp/play.csv'
# ts_position_dict_to_csv(data_dict, path)
# df = ts_position_dict_to_dataframe(data_dict)
# 
# print(df)