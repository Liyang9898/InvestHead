from blake_shore.lib.application import simple_option_viewer_2_side
from blake_shore.lib.visual import ploty_stock_option_batch, \
    ploty_leverage_batch


option_2_side = simple_option_viewer_2_side(
    ###############customize#######################
    mature_date='2021-09-17',
    strike_price=50,
    option_price=4.75,
    stock_price_current=53.69,
    ###############default#########################
    monthly_increase_perscent=0.04,
    monthly_decrease_perscent=-0.04,
    ticker='unknown',        
)

ploty_stock_option_batch(option_2_side)
ploty_leverage_batch(option_2_side, absolute=True)
ploty_leverage_batch(option_2_side, absolute=False)