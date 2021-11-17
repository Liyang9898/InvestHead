from blake_shore.lib.generate_trail import get_op_price_trail_assuming_v

price_trail = {
    '2021-03-09': 634.01,
    '2021-04-09': 641.01,
    '2021-05-09': 684.01,
    '2021-06-09': 729.01,
    '2021-07-09': 769.01,
    '2021-08-09': 814.01,
    '2021-09-09': 863.01,
}

    
res = get_op_price_trail_assuming_v(
    price_trail, # price, time
    strike_p=640, # op param
    mature_date='2021-09-17', # op param
    op_type='c', # op param
    risk_free_rate=0.0153,
    volatility_implied=0.71,  
)
# print(res[['date','option_price','leverage','leverage_ab']])
res.to_csv('D:/f_data/temp/op_test_sparse.csv', index=False)
