from blake_shore.lib.helper import option_info_reformat

fb_options_3m = option_info_reformat({ # 4x  iv=0.3
    'tag': 'fb_options_3m',
    # environment info
    'increase_factor' : 0.04 * 3,
    'risk_free_rate' : 0.005,
    
    # option basic info
    'ticker':'fb',
    'st_price_now' : 319,
    'today' : '2021-05-07',
    'mature' : '2021-08-20',
    
    # option chain
    'option_chain' : {
        'strike=-8%': {'strike':295, 'op_p':35.13},
        'strike=-4%': {'strike':305, 'op_p':29.83},
        'strike=0%': {'strike':319, 'op_p':20.83},
        'strike=4%': {'strike':330, 'op_p':15.83},
        'strike=8%': {'strike':345, 'op_p':10.5},
    }
})

amzn_options_3m = option_info_reformat({ # 4.5x    iv=0.28
    'tag': 'amzn_options_3m',                                        
    # environment info
    'increase_factor' : 0.04 * 3,
    'risk_free_rate' : 0.005,
    
    # option basic info
    'ticker':'amzn',
    'st_price_now' : 3289,
    'today' : '2021-05-07',
    'mature' : '2021-08-20',
    
    # option chain
    'option_chain' : {
        'strike=-8%': {'strike':3000, 'op_p':379.73},
        'strike=-4%': {'strike':3120, 'op_p':296.8},
        'strike=0%': {'strike':3250, 'op_p':219.75},
        'strike=4%': {'strike':3350, 'op_p':170},
        'strike=8%': {'strike':3500, 'op_p':111},
    }
})

amd_options_3m = option_info_reformat({ # 3x   iv=0.37-0.45
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
        'strike=-8%': {'strike':70, 'op_p':12.53},
        'strike=-4%': {'strike':75, 'op_p':8.33},
        'strike=0%': {'strike':77.5, 'op_p':6.98},
        'strike=4%': {'strike':80, 'op_p':5.83},
        'strike=8%': {'strike':82.5, 'op_p':4.83},
    }
})

tsla_options_2m = option_info_reformat({ # minus iv = 0.54-0.58
    'tag': 'tsla_options_2m',
    # environment info
    'increase_factor' : 0.04 * 2,
    'risk_free_rate' : 0.005,
    
    # option basic info
    'ticker':'tsla',
    'st_price_now' : 670.71,
    'today' : '2021-05-07',
    'mature' : '2021-07-16',
    
    # option chain
    'option_chain' : {
        'strike=-8%': {'strike':620, 'op_p':94.9},
        'strike=-4%': {'strike':640, 'op_p':82.83},
        'strike=0%': {'strike':670, 'op_p':66.58},
        'strike=4%': {'strike':690, 'op_p':56.95},
        'strike=8%': {'strike':720, 'op_p':44.45},
    }
})

tsla_options_4m = option_info_reformat({ # neutral   iv = 0.57-0.6
    'tag': 'tsla_options_4m',
    # environment info
    'increase_factor' : 0.04 * 4,
    'risk_free_rate' : 0.005,
    
    # option basic info
    'ticker':'tsla',
    'st_price_now' : 670.71,
    'today' : '2021-05-07',
    'mature' : '2021-09-17',
    
    # option chain
    'option_chain' : {
        'strike=-8%': {'strike':600, 'op_p':131.83},
        'strike=-4%': {'strike':640, 'op_p':109.53},
        'strike=0%': {'strike':660, 'op_p':99.35},
        'strike=4%': {'strike':700, 'op_p':81.25},
        'strike=8%': {'strike':710, 'op_p':77.15},
    }
})

ttc_options_2m = option_info_reformat({ #8x  iv = 20%
    'tag': 'ttc_options_2m',
    # environment info
    'increase_factor' : 0.04 * 2,
    'risk_free_rate' : 0.005,
    
    # option basic info
    'ticker':'ttc',
    'st_price_now' : 116.51,
    'today' : '2021-05-07',
    'mature' : '2021-07-16',
    
    # option chain
    'option_chain' : {
        'strike=-8%': {'strike':105, 'op_p':12.55},
        'strike=-4%': {'strike':110, 'op_p':8.9},
        'strike=0%': {'strike':115, 'op_p':5.6},
        'strike=4%': {'strike':120, 'op_p':3.05},
        'strike=8%': {'strike':125, 'op_p':1.68},
    }
})

pool_options_3m = option_info_reformat({ # 4x
    'tag': 'pool_options_3m',
    # environment info
    'increase_factor' : 0.04 * 3,
    'risk_free_rate' : 0.005,
    
    # option basic info
    'ticker':'pool',
    'st_price_now' : 444,
    'today' : '2021-05-07',
    'mature' : '2021-08-20',
    
    # option chain
    'option_chain' : {
        'strike=-8%': {'strike':400, 'op_p':54.2},
        'strike=-4%': {'strike':420, 'op_p':40.1},
        'strike=0%': {'strike':440, 'op_p':28.3},
        'strike=4%': {'strike':460, 'op_p':20.05},
        'strike=8%': {'strike':480, 'op_p':12.65},
    }
})

morn_options_4m = option_info_reformat({ # 5x
    'tag': 'morn_options_4m',
    # environment info
    'increase_factor' : 0.04 * 4,
    'risk_free_rate' : 0.005,
    
    # option basic info
    'ticker':'morn',
    'st_price_now' : 262.1,
    'today' : '2021-05-07',
    'mature' : '2021-09-17',
    
    # option chain
    'option_chain' : {
        'strike=-8%': {'strike':240, 'op_p':28.25},
        'strike=-4%': {'strike':250, 'op_p':21.25},
        'strike=0%': {'strike':260, 'op_p':15},
        'strike=4%': {'strike':270, 'op_p':10.25},
        'strike=8%': {'strike':280, 'op_p':7.5},
    }
})


fb_options_5m = option_info_reformat({ # 4x
    'tag': 'fb_options_5m',
    # environment info
    'increase_factor' : 0.04 * 5,
    'risk_free_rate' : 0.005,
    
    # option basic info
    'ticker':'fb',
    'st_price_now' : 319,
    'today' : '2021-05-07',
    'mature' : '2021-10-15',
    
    # option chain
    'option_chain' : {
        'strike=-8%': {'strike':290, 'op_p':43.43},
        'strike=-4%': {'strike':300, 'op_p':36.28},
        'strike=0%': {'strike':310, 'op_p':31.1},
        'strike=4%': {'strike':320, 'op_p':25.85},
        'strike=8%': {'strike':330, 'op_p':21.28},
    }
})


tsla_options_7m = option_info_reformat({ # 1.4x
    'tag': 'tsla_options_7m',
    # environment info
    'increase_factor' : 0.04 * 7,
    'risk_free_rate' : 0.005,
    
    # option basic info
    'ticker':'tsla',
    'st_price_now' : 670.71,
    'today' : '2021-05-07',
    'mature' : '2021-12-17',
    
    # option chain
    'option_chain' : {
        'strike=-8%': {'strike':620, 'op_p':149.78},
        'strike=-4%': {'strike':640, 'op_p':140.03},
        'strike=0%': {'strike':670, 'op_p':126.53},
        'strike=4%': {'strike':700, 'op_p':114.1},
        'strike=8%': {'strike':725, 'op_p':104.58},
    }
})


ttc_options_6m = option_info_reformat({  # 6x
    'tag': 'ttc_options_6m',
    # environment info
    'increase_factor' : 0.04 * 6,
    'risk_free_rate' : 0.005,
    
    # option basic info
    'ticker':'ttc',
    'st_price_now' : 116.51,
    'today' : '2021-05-07',
    'mature' : '2021-11-19',
    
    # option chain
    'option_chain' : {
        'strike=-8%': {'strike':105, 'op_p':14.5},
        'strike=-4%': {'strike':110, 'op_p':11.7},
        'strike=0%': {'strike':115, 'op_p':9.55},
        'strike=4%': {'strike':120, 'op_p':6.3},
        'strike=8%': {'strike':125, 'op_p':4.2},
    }
})


###############################daily stock recommendation ###########################
rol_options_3m = option_info_reformat({
    'tag': 'rol_options_3m',
    # environment info
    'increase_factor' : 0.04 * 3,
    'risk_free_rate' : 0.005,
    
    # option basic info
    'ticker':'rol',
    'st_price_now' : 37.12,
    'today' : '2021-05-07',
    'mature' : '2021-08-20',
    
    # option chain
    'option_chain' : {
        'strike=0%': {'strike':35, 'op_p':3.25}
    }
})

vrsn_options_2m = option_info_reformat({
    'tag': 'vrsn_options_2m',
    # environment info
    'increase_factor' : 0.04 * 2,
    'risk_free_rate' : 0.005,
    
    # option basic info
    'ticker':'vrsn',
    'st_price_now' : 222.89,
    'today' : '2021-05-07',
    'mature' : '2021-07-16',
    
    # option chain
    'option_chain' : {
        'strike=0%': {'strike':220, 'op_p':9.95}
    }
})


bro_options_4m = option_info_reformat({
    'tag': 'bro_options_4m',
    # environment info
    'increase_factor' : 0.04 * 4,
    'risk_free_rate' : 0.005,
    
    # option basic info
    'ticker':'bro',
    'st_price_now' : 53.69,
    'today' : '2021-05-07',
    'mature' : '2021-09-17',
    
    # option chain
    'option_chain' : {
        'strike=0%': {'strike':50, 'op_p':4.75}
    }
})


tru_options_4m = option_info_reformat({
    'tag': 'tru_options_4m',
    # environment info
    'increase_factor' : 0.04 * 4,
    'risk_free_rate' : 0.005,
    
    # option basic info
    'ticker':'tru',
    'st_price_now' : 106.21,
    'today' : '2021-05-07',
    'mature' : '2021-09-17',
    
    # option chain
    'option_chain' : {
        'strike=0%': {'strike':105, 'op_p':2.65}
    }
})


shw_options_4m = option_info_reformat({
    'tag': 'shw_options_4m',
    # environment info
    'increase_factor' : 0.04 * 4,
    'risk_free_rate' : 0.005,
    
    # option basic info
    'ticker':'shw',
    'st_price_now' : 287.23,
    'today' : '2021-05-07',
    'mature' : '2021-09-17',
    
    # option chain
    'option_chain' : {
        'strike=0%': {'strike':286.67, 'op_p':17.60}
    }
})


xpo_options_3m = option_info_reformat({
    'tag': 'xpo_options_3m',
    # environment info
    'increase_factor' : 0.04 * 3,
    'risk_free_rate' : 0.005,
    
    # option basic info
    'ticker':'xpo',
    'st_price_now' : 147,
    'today' : '2021-05-07',
    'mature' : '2021-08-20',
    
    # option chain
    'option_chain' : {
        'strike=0%': {'strike':145, 'op_p':12.6}
    }
})


apo_options_4m = option_info_reformat({
    'tag': 'apo_options_4m',
    # environment info
    'increase_factor' : 0.04 * 4,
    'risk_free_rate' : 0.005,
    
    # option basic info
    'ticker':'apo',
    'st_price_now' : 58.22,
    'today' : '2021-05-07',
    'mature' : '2021-09-17',
    
    # option chain
    'option_chain' : {
        'strike=0%': {'strike':55, 'op_p':5.3}
    }
})


it_options_4m = option_info_reformat({
    'tag': 'it_options_4m',
    # environment info
    'increase_factor' : 0.04 * 4,
    'risk_free_rate' : 0.005,
    
    # option basic info
    'ticker':'it',
    'st_price_now' : 234,
    'today' : '2021-05-07',
    'mature' : '2021-09-17',
    
    # option chain
    'option_chain' : {
        'strike=0%': {'strike':230, 'op_p':19.1}
    }
})


amd_options_3m_one = option_info_reformat({ # 3x   iv=0.37-0.45
    'tag': 'amd_options_3m',
    # environment info
    'increase_factor' : 0.03 * 3,
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