from datetime import date
from blake_shore.lib.generate_trail import batch_gen_option_trail_from_today_option
from blake_shore.lib.helper import option_info_reformat
from util.util import day_gap


def simple_option_viewer(
    mature_date,
    strike_price,
    
    option_price,
    stock_price_current,
    monthly_increase_perscent,
    ticker='unknown',
):
    today = date.today().strftime("%Y-%m-%d")
    
    month=int(day_gap(today,mature_date) * 1.0 / 30)
    

    increase_factor = monthly_increase_perscent * month
    
    options = option_info_reformat({
        'tag': f"{ticker}_options_{month}m",
        # environment info
        'increase_factor' : increase_factor,
        'risk_free_rate' : 0.005,
        
        # option basic info
        'ticker':ticker,
        'st_price_now' : stock_price_current,
        'today' : today,
        'mature' : mature_date,
        
        # option chain
        'option_chain' : {
            'strike=0%': {'strike':strike_price, 'op_p':option_price},
        }
    })
    print(options)
    res = batch_gen_option_trail_from_today_option(options)

    implied_volatility = res['strike=0%'].loc[0,'implied_volatility']
    print(f"implied_volatility:{implied_volatility}")
    return res


def simple_option_viewer_2_side(
    ###############customize#######################
    mature_date,
    strike_price,
    option_price,
    stock_price_current,
    ###############default#########################
    monthly_increase_perscent,
    monthly_decrease_perscent,
    ticker='unknown',        
):
    option_info_positive = simple_option_viewer(
        ###############customize#######################
        mature_date=mature_date,
        strike_price=strike_price,
        option_price=option_price,
        stock_price_current=stock_price_current,
        ###############default#########################
        monthly_increase_perscent=monthly_increase_perscent, 
        ticker=ticker,
    )
    
    option_info_negative = simple_option_viewer(
        ###############customize#######################
        mature_date=mature_date,
        strike_price=strike_price,
        option_price=option_price,
        stock_price_current=stock_price_current,
        ###############default#########################
        monthly_increase_perscent=monthly_decrease_perscent, 
        ticker=ticker,
    )
    
    option_2_side = {}
    option_2_side['positive'] = option_info_positive['strike=0%']
    option_2_side['negative'] = option_info_negative['strike=0%']
    
    return option_2_side
