# -*- coding: utf-8 -*-
from kw.kw_jun import *

import sys
from PyQt5.QtWidgets import *
import pdb

import quantking

def main():
    print('-' * 25)
    print('Start JUNY INVESTMENT Code')
    print('-' * 25)

    app = QApplication(sys.argv)
    kw = KW_class()

    interesting_comps = quantking.get_totalstocks()

    print('=' * 25)
    print('내 계좌 정보')
    print('=' * 25)
    kw.signal_login_commConnect()
    acount_list = kw.get_account_info()
    print('내 계좌 수:', len(acount_list))
    print('내 계좌: ', acount_list)

    mymoney = kw.detail_account_info(acount_list[0])
    print('예수금:', mymoney['예수금'])

    for code in interesting_comps:
        temp = kw.com_basic_info(code=code, screen_stock_infos='10001', date=None, sPrevNext='0')
        print(code, temp['종목명'], temp['현재가'])
    
    pdb.set_trace()
    temp = 0

    # print('출금가능금액:', mymoney['출금가능금액'])

    # print('=' * 25)
    # print('기업 코드 list 가져오기')
    # print('=' * 25)
    # codes = {}
    # codes['장내'] = kw.get_code_list_by_market('0')
    # codes['코스닥'] = kw.get_code_list_by_market('10')
    # print('장내 상장 기업 수: ', len(codes['장내']))
    # print('코스닥 상장 기업 수: ', len(codes['코스닥']))

    # ilbong = kw.day_ilbong_db(code=codes['장내'][0], screen_ilbong_stock = '0500')

    app.exec_()

    return

if __name__ == '__main__':
    main()