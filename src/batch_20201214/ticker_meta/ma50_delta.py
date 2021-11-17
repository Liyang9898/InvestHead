'''
Created on Jan 17, 2021

@author: leon
'''
import os
import pandas as pd
def up_percent(input):
    total = len(input)
    positive = 0
    for x in list(range(0,total-2)):
        diff = input[x+1] - input[x]
        if diff > 0:
            positive = positive + 1
    return positive * 1.0 / total

def ma50_up_percent(file_path, start_time, end_time):
    df = pd.read_csv(file_path)
    df_filtered = df.loc[(df['est_datetime']>=start_time) & (df['est_datetime']<=end_time)]
    input = df_filtered['ma50'].tolist()
    return up_percent(input)

def batch_ma50_up_percent(indicator_folder, start_time, end_time):
    # return a dic, key-ticker, value-percent
    cnt = 1
    res = {}
    for file in os.listdir(indicator_folder):
        if not file.endswith(".csv"):
            continue
        ticker = file.split('_')[0]   

        p=ma50_up_percent(indicator_folder+file, start_time, end_time)
        res[ticker]=p
        print(ticker,p)
        cnt=cnt+1
#         if cnt == 10:
#             break
    return res
############################################source region end#############################################
folder_path_price_with_indicator = "D:/f_data/sweep_20201214/indicator_stock_20210106/"
path_ma50_up_rate = "D:/f_data/sweep_20201214/all_ticker_meta/ma50_up_rate_20210117.csv"
start_time="2016-01-01 20:00:00"
end_time="2020-12-31 19:00:00"
res = batch_ma50_up_percent(folder_path_price_with_indicator, start_time, end_time)
rows=[]
for k,v in res.items():
    row = {'ticker':k,'ma50_up_rate':v}
    rows.append(row)
df = pd.DataFrame(rows)
print(df)
df.to_csv(path_ma50_up_rate, index=False)