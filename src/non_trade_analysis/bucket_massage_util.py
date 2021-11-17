'''
Created on Nov 10, 2020

@author: leon
'''


def process_bucket(input):
    freq = len(input)
    down_counter = {
        3:0,
        7:0,
        14:0
    }
    all_max={
        3:[],
        7:[],
        14:[]
    }
    
    all_min={
        3:[],
        7:[],
        14:[]
    }
    for record in input:
        current_price = record['current_price']
        tag = record['tag']
        data_pack = record['data_pack']
        # record is like {3:{},7:{},14{}}
#         print(current_price, data_pack[3]['low'],data_pack[7]['low'],data_pack[14]['low'])
        if data_pack[3]['low'] < current_price:
            down_counter[3]=down_counter[3]+1
        elif data_pack[7]['low'] < current_price:
            down_counter[7]=down_counter[7]+1
        elif data_pack[14]['low'] < current_price:
            down_counter[14]=down_counter[14]+1
            
        all_max[3].append(int(data_pack[3]['high_delta']))
        all_max[7].append(int(data_pack[7]['high_delta']))
        all_max[14].append(int(data_pack[14]['high_delta']))

        all_min[3].append(int(data_pack[3]['low_delta']))
        all_min[7].append(int(data_pack[7]['low_delta']))
        all_min[14].append(int(data_pack[14]['low_delta']))

    return {
        'cnt':float(freq),
        '3':float(down_counter[3])/float(freq),
        '7':float(down_counter[3])/float(freq),
        '14':float(down_counter[3])/float(freq),
        '3_list_max':all_max[3],
        '7_list_max':all_max[7],
        '14_list_max':all_max[14],
        
        '3_list_min':all_min[3],
        '7_list_min':all_min[7],
        '14_list_min':all_min[14]
    }