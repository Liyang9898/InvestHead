from py_vollib.black_scholes import black_scholes
from py_vollib.black_scholes.implied_volatility import implied_volatility


############################################# 
## global valuable: 
# 1.option_strike_price
# 2.interest_rate
# 3.util_mature
# # valuable at time t before mature: 
# 1.stock price
# 2.option price  (compute)
# 3.volatility (compute)
############################################# 
def get_implied_volatility(
    op_p,
    st_p,
    #############
    strike_p,
    day,
    r,
    #############
    op_type # c/p
):
    expire_year = day * 1.0 / 365
    iv = implied_volatility(
        op_p, 
        st_p, 
        strike_p, 
        expire_year, 
        r, 
        op_type
    )
    return iv


def get_option_price(
    v,
    st_p,
    #############
    strike_p,
    day,
    r,
    #############
    op_type # c/p
):
    expire_year = day * 1.0 / 365
    op_p_est = black_scholes(op_type, st_p, strike_p, expire_year, r, v)
    return op_p_est


