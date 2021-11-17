import numpy as np


def get_down_from_peak(df):
    df.sort_values(by='date', inplace=True)
    df.reset_index(inplace=True,drop=True)
    max_p = 0
    df['down_from_peak'] = np.nan
    df['previous_peak'] = np.nan
    for i in range(0, len(df)):

        p = df.loc[i, 'close']
        
        if p >= max_p:
            max_p = p
            df.loc[i, 'down_from_peak'] = 0
        else:
            down = p / max_p - 1
            df.loc[i, 'down_from_peak'] = down
            
        df.loc[i, 'previous_peak'] = max_p