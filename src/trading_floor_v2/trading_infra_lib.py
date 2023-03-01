'''
Created on Mar 1, 2023

@author: spark
'''
import pandas as pd


STATUS_LONG = 'long'
STATUS_SHORT = 'short'
STATUS_EMPTY = 'empty'

ACTION_ENTER = 'enter'
ACTION_EXIT = 'exit'


def test_enter(df, i):
    '''
    This function checks if we should enter on bar i, so it check signal on i-1
    '''
    idx = i - 1
    date = df.loc[i, 'date']
    enter_price = df.loc[i, 'open'] # we enter on open
    res = {
        'action': '',
        'type': '',
        'ts':date,
        'price': enter_price
    }
    
    # feature (use idx - 1 signal)
    ema21 = df.loc[idx, 'ema21']
    ma50 = df.loc[idx, 'ma50']
    
    
    # making trade decision
    if ema21 > ma50:
        res['action'] = ACTION_ENTER
        res['type'] = STATUS_LONG

    elif ema21 < ma50:
        res['action'] = ACTION_ENTER
        res['type'] = STATUS_SHORT
        
    else:
        res = None
    
    return res


def test_exit(df, i, enter_info):
    '''
    This function checks if we should exit on bar i, so it check signal on i-1
    We assume we always check on the valid bar
    '''
    idx = i - 1
    date = df.loc[i, 'date']
    enter_price = df.loc[i, 'open'] # we enter on open
    res = {
        'action': '',
        'type': '',
        'ts':date,
        'price': enter_price
    }
    
    # feature (use idx - 1 signal)
    ema21 = df.loc[idx, 'ema21']
    ma50 = df.loc[idx, 'ma50']
    
    # enter info
    trade_type = enter_info['type']
    
    # making trade decision
    if trade_type == STATUS_LONG and ema21 < ma50: # exit
        res['action'] = ACTION_EXIT
        res['type'] = trade_type

    elif trade_type == STATUS_SHORT and ema21 > ma50: # exit
        res['action'] = ACTION_EXIT
        res['type'] = trade_type      
        
    else:
        res = None
    
    return res
    

def run_trading_strategy(df):
    '''
    This function run trading strategy on df (dataframe with price info and indicator info)
    '''
    df.reset_index(drop=True, inplace=True)
    
    trade_status = STATUS_EMPTY
    enter_info = None
    action_list = []
    
    for i in range(1, len(df)): # start with 1 because we always check previous bar's signal for decision on this bar
        
        if trade_status == STATUS_EMPTY: # not holding
            '''
            In here, you are not holding anything, try to enter
            End up: 1. entered or 2.keeps empty
            '''
            
            enter_info = test_enter(df, i)
            
            if enter_info != None: # entered
                '''
                entered!!!!
                '''
                trade_status = enter_info['type']
                action_list.append(enter_info)
    
            else: # keeps empty
                trade_status = STATUS_EMPTY
                
            
        else: # holding
            '''
            In here, you are holding something, try to exit
            End up: 1. empty 2. keep holding
            '''
            if enter_info == None:
                raise Exception('missing holding information')
            
            exit_info = test_exit(df, i, enter_info)
            
            
            if exit_info != None:
                '''
                exited!!!
                '''
                trade_status = STATUS_EMPTY
                action_list.append(exit_info)
    
    
    # close up unfinished trade
    if trade_status != STATUS_EMPTY: # exist unfinished trade
        last_idx = len(df) - 1
        exit_info = {
            'action': ACTION_EXIT,
            'type': enter_info['type'],
            'ts':df.loc[last_idx, 'date'],
            'price': df.loc[last_idx, 'open'],
        }
        action_list.append(exit_info)
    
    df_action = pd.DataFrame(action_list)
    return df_action