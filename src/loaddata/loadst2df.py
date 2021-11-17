'''
Created on Jan 12, 2020

@author: leon
'''
import pandas as pd

# # timescope = '1min'
# # timescope = '5min'
# timescope = '1min_12years'

def load_st_data(timescope):
    scope_option = {
        '1min_12years':{
            'path':["""D:/f_data/es-1m_2007_to_2019end_changed4_inmarket_format.csv"""],
            'endtime':'10:30:00'
        },
        '5min_12years':{
            'path':["""D:/f_data/es-5m_2007_to_2019end_nytime_format.csv"""],
            'endtime':'12:30:00'
        },
        '1min':{
            'path':[
                """D:/f_data/BATS_SPY_1min_1120_1224_format.csv""", 
                """D:/f_data/BATS_SPY_1min_1223_0107_format.csv""",
                """D:/f_data/BATS_SPY_1min_2020_01_format.csv"""
            ],
            'endtime':'10:30:00'
        },
        '5min':{
            'path':["""D:/f_data/BATS_SPY_5min_format.csv"""],
            'endtime':'11:30:00'
        }
    }
    
    # end_time = scope_option[timescope]['endtime']
    paths = scope_option[timescope]['path']
    
    dfs = []
    for path in paths:
        df = pd.read_csv(
            path,
            sep=',',
            header=0,
            names=['time', 'open', 'high', 'low', 'close', 'date', 'est_time', 'year']
        )
        dfs.append(df)
    df = pd.concat(dfs).drop_duplicates().reset_index(drop=True)
    return df
#     print(df)