# from blake_shore.data.options import amd_options_3m_one
from blake_shore.lib.generate_trail import batch_gen_option_trail_from_today_option
from blake_shore.lib.helper import iv_and_leverage_from_option_group, \
    option_info_reformat
from blake_shore.lib.visual import ploty_stock_option_batch, \
    ploty_leverage_batch


# def foo(option_spec):
#     """
#     input: option spec, 
#     output, option price trail, leverage trail
#     """
#     amd_options_3m_one
amd_options_3m_one = option_info_reformat({ # 3x   iv=0.37-0.45
    'tag': 'amd_options_3m',
    # environment info
    'increase_factor' : 0.04 * 3,
    'risk_free_rate' : 0.005,
    
    # option basic info
    'ticker':'amd',
    'st_price_now' : 78.82,
    'today' : '2021-05-07',
    'mature' : '2021-08-20',
    
    # option chain
    'option_chain' : {
        'strike=0%': {'strike':77.5, 'op_p':6.98},
    }
})

dfs = batch_gen_option_trail_from_today_option(amd_options_3m_one, negative_growth=True)   
# df=dfs['strike=0%']
# df.to_csv('D:/f_data/temp/option_152022.csv')
# print(dfs['strike=0%'].columns)
# print(dfs['strike=0%'])
res = iv_and_leverage_from_option_group(dfs)
# print(res)
ploty_stock_option_batch(dfs)
ploty_leverage_batch(dfs, absolute=True)