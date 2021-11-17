'''
Created on Nov 9, 2020

@author: leon
'''
MAX_WINDOW = 14 
bucket = [
    '0-200',
    '200-400',
    '400-600',
    '600-800',
    '800-1000',
    '1000+'
]

# for one bar, scan all following 14 bars
def scanMinMax(df, bar_cnt):
    res = {
        3:{},
        7:{},
        14:{},
    }
    
    
    idx_max = len(df) - 1
    bar_now = df.iloc[bar_cnt,:]
    current_price = bar_now['close']
    delta_drop = -(bar_now['close'] - bar_now['open'])*10
    if delta_drop <= 0:
        return {
            'date':bar_now['est_datetime'],
            'current_price':current_price,
            'tag':'not short',
            'data_pack':{}
        } 
    
    bucket_str = assignBucket(delta_drop)
    
    min_p = current_price
    max_p = current_price
    
    for offset in range(1,MAX_WINDOW+1): 
        idx = bar_cnt + offset
        idx = min(idx,idx_max)

        bar = df.iloc[idx,:]
        max_p = max(max_p, bar['high'])
        min_p = min(min_p, bar['low'])
        
        # record
        if offset in res.keys():
            res[offset]['high']=max_p
            res[offset]['low']=min_p
            res[offset]['high_delta']=max_p-current_price
            res[offset]['low_delta']=min_p-current_price
    print(bar_now['est_datetime'], '-----',bar_cnt)
    return {
        'date':bar_now['est_datetime'],
        'current_price':current_price,
        'tag':bucket_str,
        'data_pack':res
    }    
        
#         
#     print(bucket_str,bar['date'],'----',min_p,'---',max_p)
    
    
def assignBucket(delta):
    if delta >= 0 and delta < 20:
        return '0-200'
    elif delta >= 20 and delta < 40:
        return '200-400'
    elif delta >= 40 and delta < 60:
        return '400-600'
    elif delta >= 60 and delta < 80:
        return '600-800'
    elif delta >= 80 and delta < 100:
        return '800-1000'
    elif delta >= 100:
        return '1000+'
    else: 
        return 'not include'