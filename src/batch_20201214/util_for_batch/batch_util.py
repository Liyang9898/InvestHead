'''
Created on Jan 13, 2021

@author: leon
'''
import pandas as pd
import os

def get_ticker_list(path, ticker_col):
    df = pd.read_csv(path)
    return list(df[ticker_col])


def check_ticker_exist(path,ticker):
    for file in os.listdir(path):
        if not file.endswith(".csv"):
            continue
        
        # extract ticker
        t = file.split('_')[0]
        if t == ticker:
            return True
    return False

def get_all_files(folder):
    files = {}
    for file in os.listdir(folder):
        if file.endswith(".csv"):
            ticker = file.split('_')[0]
            files[ticker] = file
    return files

def get_all_all_entry_files(folder):
    files = {}
    for file in os.listdir(folder):
        if file.endswith("_all_entry.csv"):
            ticker = file.split('_')[0]
            files[ticker] = file
    return files

def get_all_files_general(folder):
    files = {}
    for file in os.listdir(folder):
        if file.endswith(".csv"):
            files[file] = file
    return files