# from matplotlib import pyplot as plt

import pandas as pd
from util.general_ui import plot_bars_from_xy_list
# from util.util_finance import multi_protfolio_perf, cash_pnl


path = 'C:/f_data/temp/movingwindow_test.csv'
df = pd.read_csv(path)
print(df)  
x_list = df['date'].to_list()
y_list = df['price'].to_list()
plot_bars_from_xy_list(x_list, y_list, title='default', path='C:/f_data/temp/html.html')
