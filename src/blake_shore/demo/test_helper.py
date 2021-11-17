from blake_shore.data.options import fb_options_3m
from blake_shore.lib.helper import option_info_reformat
from util.util import print_dict

# def option_jacker_negation_price(options):
#     # this function reverse the growth of option's underlying price
#     options_neg = {}
#     for tag, option in options.items():
#         options_neg[tag] = option.copy()
#         options_neg[tag]['increase_factor'] *= -1
#     return options_neg 
# 
# fb_options_3m
# 
# print_dict(fb_options_3m)
# 
# x = option_jacker_negation_price(fb_options_3m)
# 
# print_dict(x)