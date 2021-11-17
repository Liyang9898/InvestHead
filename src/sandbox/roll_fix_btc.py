from util.util_finance import trade_distribution_plot


path = 'D:/f_data/trades_csv/BTC_1D_fmt_trades_all_entry.csv'
path2 = 'D:/f_data/price_with_indicator/BTC_1D_fmt_idc.csv'


    
trade_distribution_plot(path, path2)
# 
# rows = []
# for i in range(0, len(df)):
#     df.loc[i, 'entry_ts']
#     df.loc[i, 'exit_ts']
#     df.loc[i, 'entry_roll']
#     df.loc[i, 'exit_roll']
#     
#     rows.append({'ts': df.loc[i, 'entry_ts'], 'position':df.loc[i, 'entry_roll'], 'type':'entry'})
#     rows.append({'ts': df.loc[i, 'exit_ts'], 'position':df.loc[i, 'exit_roll'], 'type':'exit'})
#     
# df_ee = pd.DataFrame(rows)
# 
# 
# 
# # df = px.data.gapminder().query("country=='Canada'")
# fig = px.scatter(df_ee, x="ts", y="position", color='type', title='Life expectancy in Canada')
# fig.show()
# 
# # plot_line_chart_from_df_col(df=df_ee, x_col='ts', y_cols=['exit_fix', 'exit_roll'])
# 
# 
# print(df.columns)
# df.to_csv('D:/f_data/temp/rollfix_test.csv')
# print(df)
# plot_line_chart_from_df_col(df=df, x_col='exit_ts', y_cols=['exit_fix', 'exit_roll'])