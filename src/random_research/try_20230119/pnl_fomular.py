'''
Created on Jan 27, 2023

@author: spark
'''
import pandas as pd
import plotly.express as px

def mudong_op_pnl_conversion(price, strike, up, low):
    '''
    strike is a price
    up and low are percentage: like +0.2 or -0.15
    '''
    if price > strike * (1+ up):
        return strike * up
    elif price > strike and price <= strike * (1+ up):
        return price - strike
    elif price > strike * (1+low) and price <= strike:
        return 0
    elif price <= strike * (1+low):
        return price - strike * (1 + low)
        

# testing
# up = 0.2
# low = -0.2
# strike = 400    
# x = []
# y = []
# for price in range (250, 500):
#     gain = mudong_op_pnl_conversion(price, strike, up, low)
#     x.append(price)
#     y.append(gain)
#
# df = pd.DataFrame(dict(
#     x=x,y=y
# ))
#
# fig = px.line(df, x="x", y="y", title="Unsorted Input") 
# fig.show()