# -*- coding: utf-8 -*-
from kwapi import kwapi
from conn_excel import *
import pandas as pd
import os
import pdb
import sys
import shutil
import tqdm
import time

kw = kwapi()

def get_junlogic(my_money,save_root,csvpath = './mydata/오늘의종목_20210717_084023.csv'):
    filename = csvpath.split('/')[-1].split('.csv')[0]
    stock_list = read_csv(csvpath)
    limit_a_stock = float(my_money) / 20

    codes = []
    names = []
    values = []
    nrofbuys = []
    pivots = []
    pbar = tqdm.tqdm(range(20))
    for i in pbar:
        stock_info = stock_list[i]
        codes.append(stock_info[1][1:])
        names.append(stock_info[2])
        values.append(stock_info[3])
        infos = kw.get_single_trdata4company_basic_infos(code=stock_info[1][1:])
        time.sleep(1)
        pivots.append(infos['피벗기준선'])
        nrofbuys.append(int(limit_a_stock / infos['피벗기준선']))
    
    df = pd.DataFrame(list(zip(codes,names,values,pivots,nrofbuys)), columns=['code','name','value','pivots','norbuy'])
    
    savepath = '%s/%s.xlsx' % (save_root,filename)
    if os.path.exists(savepath):
        os.remove(savepath)
    df.to_excel(savepath)
    return

def get_quantkinglogic(my_money,save_root,excelpath):
    filename = excelpath.split('/')[-1].split('.xlsx')[0]
    stock_list_total = read_excel(excelpath)
    super_list = get_super(stock_list_total)
    mix_list = get_mix(stock_list_total)
    limit_a_stock = float(my_money) / 20

    codes, names, values, nrofbuys, pivots = _complete_list(super_list, limit_a_stock)
    
    df = pd.DataFrame(list(zip(codes,names,values,nrofbuys,pivots)), columns=['code','name','value','norbuy','pivot'])
    
    savepath = '%s/%s_super.xlsx' % (save_root,filename)
    if os.path.exists(savepath):
        os.remove(savepath)
    df.to_excel(savepath)

    codes, names, values, nrofbuys, pivots = _complete_list(mix_list, limit_a_stock)
    
    df = pd.DataFrame(list(zip(codes,names,values,pivots,nrofbuys)), columns=['code','name','value','pivot','norbuy'])
    
    savepath = '%s/%s_mix.xlsx' % (save_root,filename)
    if os.path.exists(savepath):
        os.remove(savepath)
    df.to_excel(savepath)
    return

def _complete_list(stock_list, limit_a_stock):
    codes = []
    names = []
    values = []
    nrofbuys = []
    pivots = []

    pbar = tqdm.tqdm(range(20))
    for i in pbar:
        stock_info = stock_list[i]
        code = stock_info[1][1:]
        codes.append(code)
        
        name = stock_info[2]
        names.append(name)

        infos = kw.get_single_trdata4company_basic_infos(code=code)
        time.sleep(1)
        value = abs(int(infos['현재가']))
        values.append(value)
        pivots.append(infos['피벗기준선'])

        nrofbuys.append(int(limit_a_stock / infos['피벗기준선']))
    return codes, names, values, nrofbuys, pivots

if __name__ == '__main__':
    save_root = './to_buy'
    
    my_money = 2000 * 10000
    csvpath = './mydata/오늘의종목_20210717_084023.csv'
    get_junlogic(my_money,save_root,csvpath)

    my_money = 1800 * 10000
    excelpath = u'./mydata/퀀트데이터2021.07.15(21년2Q매영순YOYQOQ).xlsx'
    get_quantkinglogic(my_money,save_root,excelpath)