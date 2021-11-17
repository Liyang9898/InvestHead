from blake_shore.data.options import (
    fb_options_3m, 
    amzn_options_3m, 
    amd_options_3m,
    tsla_options_2m
)
from blake_shore.lib.generate_trail import batch_gen_option_trail_from_today_option
from blake_shore.lib.visual import ploty_stock_option_batch, \
    ploty_leverage_batch




ticker_vector_diff_st_price_end = {
    'st_e=319-0%': {'ticker':'fb', 'strike':318, 'op_p':20.83, 'today':'2021-05-07', 'mature':'2021-08-20', 'p_s':319, 'p_e':319},
    'st_e=329-3%': {'ticker':'fb', 'strike':318, 'op_p':20.83, 'today':'2021-05-07', 'mature':'2021-08-20', 'p_s':319, 'p_e':329},
    'st_e=339-6%': {'ticker':'fb', 'strike':318, 'op_p':20.83, 'today':'2021-05-07', 'mature':'2021-08-20', 'p_s':319, 'p_e':339},
    'st_e=349-9%': {'ticker':'fb', 'strike':318, 'op_p':20.83, 'today':'2021-05-07', 'mature':'2021-08-20', 'p_s':319, 'p_e':349}
}


dfs = batch_gen_option_trail_from_today_option(amd_options_3m)


ploty_stock_option_batch(dfs)
ploty_leverage_batch(dfs, absolute=True)
ploty_leverage_batch(dfs, absolute=False)