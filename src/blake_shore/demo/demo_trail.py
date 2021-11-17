from blake_shore.lib.generate_trail import gen_option_trail_from_today_option
from blake_shore.lib.visual import ploty_stock_option, ploty_leverage


risk_free_rate = 0.005

ticker_vector = [
    {'ticker':'fb', 'strike':318, 'op_p':20.83, 'today':'2021-05-07', 'mature':'2021-08-20', 'p_s':319, 'p_e':319},
    {'ticker':'fb', 'strike':318, 'op_p':20.83, 'today':'2021-05-07', 'mature':'2021-08-20', 'p_s':319, 'p_e':339},
    {'ticker':'fb', 'strike':318, 'op_p':20.83, 'today':'2021-05-07', 'mature':'2021-08-20', 'p_s':319, 'p_e':365},
    {'ticker':'fb', 'strike':318, 'op_p':20.83, 'today':'2021-05-07', 'mature':'2021-08-20', 'p_s':319, 'p_e':375},
    {'ticker':'tsla', 'strike':640, 'op_p':126.45, 'today':'2021-03-09', 'mature':'2021-09-09', 'p_s':634.01, 'p_e':863.01},
    {'ticker':'tsla', 'strike':640, 'op_p':126.45, 'today':'2021-03-09', 'mature':'2021-09-09', 'p_s':634.01, 'p_e':766}
]

ticker_row = ticker_vector[0]

res_df = gen_option_trail_from_today_option(
    ticker=ticker_row['ticker'],
    strike_price=ticker_row['strike'],
    option_price=ticker_row['op_p'],
    date_mature=ticker_row['mature'],
    ##########
    date_today=ticker_row['today'],
    stock_price_today=ticker_row['p_s'],
    stock_price_on_mature=ticker_row['p_e'],
    ##########
    risk_free_rate=risk_free_rate
)

res_df.to_csv('D:/f_data/temp/op_test.csv', index=False)
# ploty_stock_option(res_df)
# ploty_leverage(res_df)
# ploty_leverage(res_df, absolute=False)