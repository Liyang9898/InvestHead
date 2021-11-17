import pandas as pd
from util.util_finance import multi_protfolio_perf, cash_pnl
from matplotlib import pyplot as plt

path = 'D:/f_data/temp/movingwindow_test.csv'
df = pd.read_csv(path)

positon=df['exit_on_not_8_21_50'].to_list()
initial_cash = 100
p = cash_pnl(positon, initial_cash)
plt.plot(p)
plt.show()
print(p)