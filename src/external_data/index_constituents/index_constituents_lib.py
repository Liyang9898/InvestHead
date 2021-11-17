from datetime import datetime
import numpy as np


def date_format_convert_russell2000(input_str):
    # September-2021 to 2021-09
    src_fmt = '%B-%Y'
    dest_fmt = '%Y'
    d = datetime.strptime(input_str, src_fmt)
    res = d.strftime(dest_fmt)
    return res


def date_format_convert_russell3000(input_str):
    # 6/1 - 6/30/2021 to 2021
#     input_str = input_str.replace(" ","")
#     print(input_str)
#     tokens = input_str.split('-')
#     input_str = tokens[1]
#     print(input_str)
    input_str = input_str[-4:]
#     print(input_str)
    return input_str
#     src_fmt = '%m/%d/%Y'
#     dest_fmt = '%Y'
#     d = datetime.strptime(input_str, src_fmt)
#     res = d.strftime(dest_fmt)
#     return res


def ticket_format(ticker):
    # default invalid ticket str is empty string
    
    # case: nan
    if ticker == np.nan:
        ticker = ''
        
    # ticker is -
    if ticker == '-':
        ticker = ''
        
    if not type(ticker) == str:
        return ''
    
    # case:if has (), remove it
    ticker = ticker.replace(" ", "")
    if ticker.find('(')!=-1:
        l = ticker.find('(')
        ticker = ticker[:l]

    ticker = ticker.upper()
    return ticker


