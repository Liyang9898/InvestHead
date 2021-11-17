'''
Created on Jul 9, 2020

@author: leon
'''

def unfinished_bar_best_price(open, close, high, low, target, direction):
    if direction == 1: # go up
        if open<close:#green
            if open > target:
                return close
            else:
                return high
        else:#red
            if open < target:
                return high
            else:
                return target
    elif direction == -1:
        if open<close:#green
            if close < target:
                return low
            else:
                return target
        else:#red
            if open < target:
                return close
            else:
                return low
