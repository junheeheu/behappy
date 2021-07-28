# -*- coding: utf-8 -*-
import pandas_datareader.data as web
from urllib.request import urlopen
import pandas as pd
from securities import *
import pdb
import json
import datetime
import FinanceDataReader as fdr
from pandas import DataFrame

# https://github.com/bjpublic/python-for-finance-data

#######################################
# 환율 데이터
# alpha vantage 에서 무료로 API KEY를 받아서 수집할 수 있음.
# https://www.alphavantage.co/
#######################################

def get_exchangerate_today():
    df = web.DataReader("USD/KRW", "av-forex", api_key=ALPHAVANTAGE_API_KEY)
    out = df.head()
    return float(out['USD/KRW']['Exchange Rate'])

def get_exchangerate_period():
    return

#######################################
# 코스닥/코스피 지수
#######################################
def get_kospi_kosdaq_jisu(maket_type = 'kospi', beforedate = 1): # 'kosdaq'
    if maket_type == 'kospi':
        maket_type= '^KS11'
    elif maket_type == 'kosdaq':
        maket_type= '^KQ11'
    else:
        print('kospi, kosdaq 중 하나를 선택')
    
    df = data.DataReader(maket_type, "yahoo")
    df = df.values
    return df[-1*beforedate:,5] 

#######################################
# 국내 주식 데이터
# pip install finance-datareader
#######################################
import FinanceDataReader as fdr

def get_kor_all_company_name_info():
    kospi_cd = fdr.StockListing('KOSPI')
    kosdaq_cd = fdr.StockListing('KOSDAQ')
    total_cd = pd.concat([kospi_cd,kosdaq_cd])
    # Index(['Symbol', 'Market', 'Name', 'Sector', 'Industry', 'ListingDate',
    #    'SettleMonth', 'Representative', 'HomePage', 'Region'],
    #   dtype='object')
    # out_kospi = kospi_cd.values    
    # out_kosdaq = kosdaq_cd.values
    # df = fdr.DataReader("005930", '2019')
    return total_cd

def get_kor_all_names(total_cd):
    temp = total_cd.values
    return temp[:,0].tolist()

def find_code_by_name_kor(total_cd, name=u'삼성전자'):
    # out = total_cd.loc[total_cd["Name"].str.find(name)>-1]
    out = total_cd[total_cd["Name"] == name]
    return out.values[0][0]

def get_stock_values(code='005930', start_year='2021',start_mon=1,start_day=1):
    start_date = '%s-%02d-%02d' % (start_year, start_day)
    df = fdr.DataReader(code, start_date)
    return df

#######################################
# FNGUIDE
# pip install finance-datareader
#######################################
import re
from bs4 import BeautifulSoup
from html_table_parser import parser_functions as parser
def get_fnguide_table(code='005930'):
    out = {}
    req = urlopen('http://comp.fnguide.com/SVO2/ASP/SVD_main.asp?pGB=1&gicode=A%s'%(code))
    html = req.read()
    soup = BeautifulSoup(html, 'html.parser')
    soup_table_all = soup.find_all("table")
    table_t = parser.make2d(soup_table_all[10])
    out['전체snapshot'] = pd.DataFrame(table_t[1:], columns=table_t[0])
    table_y = parser.make2d(soup_table_all[11])
    out['연간snapshot'] = pd.DataFrame(table_y[1:], columns=table_y[0])
    table_q = parser.make2d(soup_table_all[12])
    out['분기snapshot'] = pd.DataFrame(table_q[1:], columns=table_q[0])
    # 연결 분기: soup_table_all[12]
    # 연결 연간: soup_table_all[11]
    # 연결 연간: soup_table_all[10]
    
    # req = urlopen('https://comp.fnguide.com/SVO2/ASP/SVD_Consensus.asp?pGB=1&gicode=A%s'%(code))
    # html = req.read()
    # soup = BeautifulSoup(html, 'html.parser')
    # soup_table_all = soup.find_all("table")
    # pdb.set_trace()
    return out

#######################################
# RIM - 단순 계산
# (자기자본 + 자기자본 * (예상ROE-요구수익률) * 지속계수)/(1+요구수익률+지속계수)
# 예상ROE: FNGUIDE에서 확보
# 요구수익률: 한국신용평가 홈페이지로(https://www.kisrating.com) 이 BBB- 회사채 수익률 기준
# 지속계수: 0.9, 0.8 사용
# # RIM - 성장 반영 10년 시뮬레이션
# 지속계수: 1, 0.9, 0.8 사용
# 시점: 현재부터 10년 후
# 요구수익률: (10년간 동일) 한국신용평가 홈페이지로(https://www.kisrating.com) 이 BBB- 회사채 수익률 기준
# 초과이익률: (1년마다 지속 계수를 곱함) 전년도 초과이익률(초기 초과이익률:예상ROE - 요구수익률) * 지속계수
# ROE: 요구수익률 + 초과이익률 [fnguid ROE: temp_infos[18,1:7], 현재값은 temp_infos[18,5]]
# 지배주주순이익: 전년도 지배주주지분 * ROE 
# 지배주주지분: 전년도 지배주주지분 + 지배주주순이익 [fnguid지배주주지분: temp_infos[10,1:7], 현재값은 temp_infos[10,5]]
# 초과이익: 지배주주순이익 - 전년도 지배주주지분 * 요구수익률
# PV of RI: 초과이익를 현재가치로 계산 np.npv 사용 [np.npv(요구수익률, 초과이익9년list)]
# RIM 주주가치: 지배주주지분 + PV of RI
# RIM 적정주가: RIM 주주가치 / 주식수
#######################################
import numpy as np

def _get_infos(fnguide_infos):
    temp_infos_q = fnguide_infos['분기snapshot'].values
    temp_infos_y = fnguide_infos['연간snapshot'].values
    basic_infos = {}
    basic_infos['예상ROE'] = temp_infos_y[18,6]
    temp = np.array(temp_infos_q[18,2:6],dtype=np.float).mean()
    if basic_infos['예상ROE'] == '':
        basic_infos['예상ROE'] = temp
    else:
        basic_infos['예상ROE'] = float(basic_infos['예상ROE'])
    basic_infos['지배주주지분'] = float(temp_infos_q[10,5].replace(',',''))
    basic_infos['주식수'] = float(temp_infos_q[24,5].replace(',',''))

    return basic_infos

# import  numpy_financial as npf
def cal_srim(basic_infos, r, persistence_factor):
    r = r / 100
    infos = {}
    infos['초과이익률'] = [basic_infos['예상ROE']  / 100 - r]
    infos['ROE'] = [basic_infos['예상ROE'] / 100]
    infos['지배주주지분'] = [basic_infos['지배주주지분']]
    infos['지배주주순이익'] = [0]
    infos['초과이익'] = [0]
    for i in range(1,10):
        infos['초과이익률'].append(infos['초과이익률'][i-1]*persistence_factor)
        infos['ROE'].append(infos['초과이익률'][i]+r)
        infos['지배주주순이익'].append(infos['지배주주지분'][i-1]*infos['ROE'][i])
        infos['지배주주지분'].append(infos['지배주주지분'][i-1]+infos['지배주주순이익'][i])
        infos['초과이익'].append(infos['지배주주순이익'][i]-infos['지배주주지분'][i-1]*r)
    result = {'지속계수': persistence_factor}
    result['PV'] = np.npv(r,infos['초과이익'][1:])
    result['주주가치'] = basic_infos['지배주주지분'] + result['PV']
    result['적정주가'] = result['주주가치'] / basic_infos['주식수'] * 100000
    return result['적정주가']

def _get_required_earnrate():
    # 요구수익률
    req = urlopen('https://www.kisrating.com/ratingsStatistics/statics_spread.do')
    html = req.read()
    soup = BeautifulSoup(html, 'html.parser')
    soup_table_all = soup.find_all("table")
    table = parser.make2d(soup_table_all[0])
    return float(table[11][8])

if __name__ == '__main__':
    # print(get_exchangerate_today())
    # find_code_by_name_kor(get_kor_all_company_name_info())
    get_kor_all_names(get_kor_all_company_name_info())
    # get_stock_values()

    # r = _get_required_earnrate()
    # basic_infos = _get_infos(get_fnguide_table('005930'))
    # infos = {}
    # infos['적당'] = cal_srim(basic_infos, r, 0.9)
    # infos['고점'] = cal_srim(basic_infos, r, 1.)
    # infos['저점'] = cal_srim(basic_infos, r, 0.8)
    pdb.set_trace()