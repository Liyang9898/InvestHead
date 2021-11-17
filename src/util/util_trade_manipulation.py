
import pandas as pd


def gen_cash_path(trade_df):
    # input: trade_df should have the following as input
    # ticker,entry_ts,exit_ts,entry_price,exit_price
    
    # output: trade_df will have 4 more columns fix_start, fix_end, roll_start, roll_end
    # indicating the cash history
    # fix->always buy with 1 unit
    # roll always buy using all money you have now
    
    # data cleaning, keep necessary
    df_cut = trade_df[['ticker','entry_price','exit_price','entry_ts','exit_ts']]
    df=df_cut.copy()
    df.sort_values(by=['entry_ts'])
    
    # data validation: all column has no null, 
    assert df['ticker'].isnull().sum() == 0
    assert df['entry_price'].isnull().sum() == 0
    assert df['exit_price'].isnull().sum() == 0
    assert df['entry_ts'].isnull().sum() == 0
    assert df['exit_ts'].isnull().sum() == 0

    df['fix_start'] = 1
    df['roll_start'] = 1
    df['fix_end'] = 1
    df['roll_end'] = 1
    
    # iterate
    for i in range(0, len(df)):
        factor = df.loc[i, 'exit_price'] / df.loc[i, 'entry_price']
 
        if i > 0:
            df.loc[i, 'fix_start'] = df.loc[i-1, 'fix_end']
            df.loc[i, 'roll_start'] = df.loc[i-1, 'roll_end']
         
        df.loc[i, 'fix_end'] = df.loc[i, 'fix_start'] + (factor - 1)
        df.loc[i, 'roll_end'] = df.loc[i, 'roll_start'] * factor        

    return df

path = 'D:/f_data/trades_csv/SPY_1D_fmt_trades_consecutive.csv'
df = pd.read_csv(path)
df['ticker'] = 'SPY'
df2 = gen_cash_path(df)
print(df2)