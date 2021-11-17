from blake_shore.lib.blake_shore_core import get_implied_volatility, get_option_price

op_type = 'c'  # 'c' for call, 'p' for put
stock_p = 634.01  # Underlying asset price
strike_p = 640  # Strike
expire_days = 180  # (Annualized) time-to-expiration
r = 0.0153  # Interest free rate
op_p_actual = 126.45
iv = get_implied_volatility(op_p_actual, stock_p, strike_p, expire_days, r, op_type)
print(iv)


op_type = 'c'  # 'c' for call, 'p' for put
stock_p = 634.01  # Underlying asset price
strike_p = 640  # Strike
t = 180  # (Annualized) time-to-expiration   3/9  9/17      6 month 1 week      5 month 3 week   0.49
r = 0.0153  # Interest free rate
v = 0.72222  # Implied Volatility
op_p_est = get_option_price(v, stock_p, strike_p, t, r, op_type)
print(op_p_est)

