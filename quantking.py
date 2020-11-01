# -*- coding: utf-8 -*-
import pandas as pd
import pdb

datapath = './data/퀀트데이터2020.10.30.xlsx'

def get_stocks():
    # port4_1 = pd.read_excel(datapath, usecols='A', sheet_name='실적발표후 분기만 4대포트')
    # port4_2 = pd.read_excel(datapath, usecols='N', sheet_name='실적발표후 분기만 4대포트')
    # port4_3 = pd.read_excel(datapath, usecols='O', sheet_name='실적발표후 분기만 4대포트')

    port4 = pd.read_excel(datapath, usecols='A,N,O', sheet_name='실적발표후 분기만 4대포트')
    
    portnames = []
    for name in port4['전달/오늘']:
        if type(name) is float:
            continue
        portnames.append(name)
    
    codes = []
    for code in port4['코드번호.2']:
        codes.append(code)
    
    names = []
    for name in port4['종목명']:
        names.append(name)

    ports = {}
    count = 0
    for portname in portnames:
        ports[portname] = {'codes': codes[count*20:(count+1)*20],
                        'names': names[count*20:(count+1)*20]}
        count += 1
    return ports

def get_totalstocks():
    ports = get_stocks()

    portnames = list(ports.keys())

    codes = []

    for portname in portnames:
        for code in ports[portname]['codes']:
            code = code[1:]
            codes.append(code)

    return codes

if __name__ == '__main__':
    # get_stocks()
    get_totalstocks()