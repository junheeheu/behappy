# -*- coding: utf-8 -*-
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
from PyQt5.QtTest import *
from config import *
import pdb

class KW_class(QAxWidget):
    def __init__(self):
        super().__init__()
        print('-' * 25)
        print('키움 Class')
        print('-' * 25)

        ########## event loop group ##########
        self.login_event_loop = None
        self.detail_account_event_loop = None
        self.detail_mystock_event_loop = QEventLoop()
        self.calculator_event_loop = QEventLoop()
        ########## event loop group ##########

        ########## money group ##########
        self.use_money = 0 
        self.use_money_rate = 0.5
        ########## money group ##########

        ########## variable group ##########
        self.account_stock_dict = {}
        self.not_account_stock_dict = {}
        self.company_basic_infos_dict = {}
        ########## variable group ##########

        ########## screen group ##########
        self.screen_calculation_stock = '4000'
        self.screen_stock_infos = '4000'
        ########## screen group ##########

        self.get_ocs_instance()
        self.event_slots()

        self.signal_login_commConnect()
        self.get_account_info()

        # self.detail_account_info()
        # self.detail_account_mystock() 

        ############## Analysis ###############
        # self.calculator_fnc()

        ############## Get Basic Infos for Company ###############
        self.get_com_basic_info()

    def get_ocs_instance(self):
        self.setControl('KHOPENAPI.KHOpenAPICtrl.1')

    def event_slots(self):
        self.OnEventConnect.connect(self.login_slot)
        self.OnReceiveTrData.connect(self.trdata_slot)

    def login_slot(self, errCode):
        print(errors(errCode))

        self.login_event_loop.exit()

    def signal_login_commConnect(self):
        self.dynamicCall('CommConnect()')
        self.login_event_loop = QEventLoop()
        self.login_event_loop.exec_()

    def get_account_info(self):
        acount_list = self.dynamicCall("GetLogininfo(String)", "ACCNO")
        acount_list = acount_list.split(';')[:-1]
        self.acount_num = acount_list[0]

        print('myacount num', self.acount_num)

    def detail_account_info(self):
        print('예수금 요청하기')

        self.dynamicCall('SetInputValue(String, String)', '계좌번호', self.acount_num)
        self.dynamicCall('SetInputValue(String, String)', '비밀번호', '0000')
        self.dynamicCall('SetInputValue(String, String)', '비밀번호입력매체구분', '00')
        self.dynamicCall('SetInputValue(String, String)', '조회구분', '2')
        self.dynamicCall('CommRqData(String, String, int, String)', '예수금상세요청', 'opw00001', '0', '1000')

        self.detail_account_event_loop = QEventLoop()
        self.detail_account_event_loop.exec_()

    def detail_account_mystock(self, sPrevNext='0'):
        print('계좌평가잔고내역 요청하기')

        self.dynamicCall('SetInputValue(String, String)', '계좌번호', self.acount_num)
        self.dynamicCall('SetInputValue(String, String)', '비밀번호', '0000')
        self.dynamicCall('SetInputValue(String, String)', '비밀번호입력매체구분', '00')
        self.dynamicCall('SetInputValue(String, String)', '조회구분', '2')
        self.dynamicCall('CommRqData(String, String, int, String)', '계좌평가잔고내역', 'opw00018', '0', '1000')

        self.detail_account_event_loop = QEventLoop()
        self.detail_account_event_loop.exec_()

        self.detail_mystock_event_loop.exec_()

    def get_code_list_by_market(self, market_code):
        code_list = self.dynamicCall('GetCodeListByMarket(QString)', market_code)
        return code_list.split(';')[:-1]

    def calculator_fnc(self):
        code_list = self.get_code_list_by_market('10')
        print('KOSDAQ: ', len(code_list))

        for idx, code in enumerate(code_list):
            self.dynamicCall('DisconnectRealData(QString)', self.screen_calculation_stock)

            print('%s / %s : KOSDAQ Stock Code : %s is updating...' % (idx+1,len(code_list), code))
            self.day_kw_db(code = code)

    def day_kw_db(self, code=None, date=None, sPrevNext='0'):
        QTest.qWait(3600)

        self.dynamicCall('SetInputValue(QString, QString)', '종목코드', code)
        self.dynamicCall('SetInputValue(QString, QString)', '수정주가구분', '1')

        if date != None:
            self.dynamicCall('SetInputValue(QString, QString)', '기준일자', date)

        self.dynamicCall('CommRqData(String, String, int, String)', '주식일봉차트조회', 'opt10081', sPrevNext, self.screen_calculation_stock)

        self.calculator_event_loop.exec_()

    def get_com_basic_info(self):
        code_list = self.get_code_list_by_market('0') # 10: KOSDAQ, 0: IN
        print('KOSDAQ: ', len(code_list))

        for idx, code in enumerate(code_list):
            self.dynamicCall('DisconnectRealData(QString)', self.screen_calculation_stock)

            print('%s / %s : KOSDAQ Stock Code : %s is updating...' % (idx+1,len(code_list), code))
            self.com_basic_info(code = code)

    def com_basic_info(self, code=None, date=None, sPrevNext='0'):
        QTest.qWait(3600)

        self.dynamicCall('SetInputValue(QString, QString)', '종목코드', code)

        if date != None:
            self.dynamicCall('SetInputValue(QString, QString)', '기준일자', date)

        self.dynamicCall('CommRqData(String, String, int, String)', '주식기본정보요청', 'opt10001', sPrevNext, self.screen_stock_infos)

        self.calculator_event_loop.exec_()


    def trdata_slot(self, sScrNo, sRQName, sTrCode, sRecordName, sPrevNext):
        if sRQName == '예수금상세요청':
            deposit = self.dynamicCall('GetCommData(String, String, int, String)', sTrCode, sRQName, '0', '예수금')
            print('예수금: ', deposit)

            self.use_money = int(deposit) * self.use_money_rate / 4

            ok_deposit = self.dynamicCall('GetCommData(String, String, int, String)', sTrCode, sRQName, '0', '출금가능금액')
            print('출금가능금액: ', ok_deposit)

            self.detail_account_event_loop.exit()

        elif sRQName == '계좌평가잔고내역':
            total_buy_money = self.dynamicCall('GetCommData(String, String, int, String)', sTrCode, sRQName, '0', '총매입금액')
            total_buy_money = int(total_buy_money)

            print('총매입금액: ', total_buy_money)

            total_profit_rate = self.dynamicCall('GetCommData(String, String, int, String)', sTrCode, sRQName, '0', '총수익률(%)')
            total_profit_rate = float(total_profit_rate)
            print('총수익률: ', total_profit_rate)

            rows = self.dynamicCall('GetRepeatCnt(QString, QString)', sTrCode, sRQName)
            cnt = 0
            for i in range(rows):
                code = self.dynamicCall('GetCommData(QString, QString, int, QString)', sTrCode ,sRQName, i, '종목번호')
                name = self.dynamicCall('GetCommData(QString, QString, int, QString)', sTrCode ,sRQName, i, '종목명')
                stock_quantity = self.dynamicCall('GetCommData(QString, QString, int, QString)', sTrCode ,sRQName, i, '보유수량')
                buy_price = self.dynamicCall('GetCommData(QString, QString, int, QString)', sTrCode ,sRQName, i, '매입가')
                earn_rate = self.dynamicCall('GetCommData(QString, QString, int, QString)', sTrCode ,sRQName, i, '수익률(%)')
                current_price = self.dynamicCall('GetCommData(QString, QString, int, QString)', sTrCode ,sRQName, i, '현재가')
                total_chegual_price = self.dynamicCall('GetCommData(QString, QString, int, QString)', sTrCode ,sRQName, i, '매입금액')
                possible_quantity = self.dynamicCall('GetCommData(QString, QString, int, QString)', sTrCode ,sRQName, i, '매매가능수량')

                code = code.strip()[1:]
                name = name.strip()
                stock_quantity = int(stock_quantity.strip())
                buy_price = int(buy_price.strip())
                earn_rate = float(earn_rate.strip())
                current_price = int(current_price.strip())
                total_chegual_price = int(total_chegual_price.strip())
                possible_quantity = int(possible_quantity.strip())

                if code in self.account_stock_dict:
                    pass
                else:
                    self.account_stock_dict[code] = {}
                self.account_stock_dict[code]['종목명'] = name
                self.account_stock_dict[code]['보유수량'] = stock_quantity
                self.account_stock_dict[code]['매입가'] = buy_price
                self.account_stock_dict[code]['수익률(%)'] = earn_rate
                self.account_stock_dict[code]['현재가'] = current_price
                self.account_stock_dict[code]['매입금액'] = total_chegual_price
                self.account_stock_dict[code]['매매가능수량'] = possible_quantity

                
                cnt += 1

            if sPrevNext == '2':
                self.detail_account_mystock(sPrevNext='2')
            else:
                self.detail_mystock_event_loop.exit()

        elif sRQName == '실시간미체결요청':
            rows = self.dynamicCall('GetRepeatCnt(QString, QString)', sTrCode, sRQName)
            
            for i in range(rows):
                code = self.dynamicCall('GetCommData(QString, QString, int, QString)', sTrCode ,sRQName, i, '종목번호')
                name = self.dynamicCall('GetCommData(QString, QString, int, QString)', sTrCode ,sRQName, i, '종목명')
                order_no = self.dynamicCall('GetCommData(QString, QString, int, QString)', sTrCode ,sRQName, i, '주문번호')
                order_status = self.dynamicCall('GetCommData(QString, QString, int, QString)', sTrCode ,sRQName, i, '주문상태')
                order_quantity = self.dynamicCall('GetCommData(QString, QString, int, QString)', sTrCode ,sRQName, i, '주문수량')
                order_price = self.dynamicCall('GetCommData(QString, QString, int, QString)', sTrCode ,sRQName, i, '주문가격')
                order_gubun = self.dynamicCall('GetCommData(QString, QString, int, QString)', sTrCode ,sRQName, i, '주문구분')
                not_quantity = self.dynamicCall('GetCommData(QString, QString, int, QString)', sTrCode ,sRQName, i, '미체결수량')
                ok_quantity = self.dynamicCall('GetCommData(QString, QString, int, QString)', sTrCode ,sRQName, i, '체결량')

                code = code.strip()[1:]
                name = name.strip()
                order_no = int(order_no.strip())
                order_status = order_status.strip()
                order_quantity = int(order_quantity.strip())
                order_price = float(order_price.strip())
                order_gubun = order_gubun.strip().lstrip('+').lstrip('-')
                not_quantity = int(not_quantity.strip())
                ok_quantity = int(ok_quantity.strip())
                

                if order_no in self.not_account_stock_dict:
                    pass
                else:
                    self.not_account_stock_dict[order_no] = {}

                self.not_account_stock_dict[order_no]['종목번호'] = code
                self.not_account_stock_dict[order_no]['종목명'] = name
                self.not_account_stock_dict[order_no]['주문상태'] = order_status
                self.not_account_stock_dict[order_no]['주문수량'] = order_quantity
                self.not_account_stock_dict[order_no]['주문가격'] = order_price
                self.not_account_stock_dict[order_no]['주문구분'] = order_gubun
                self.not_account_stock_dict[order_no]['미체결수량'] = not_quantity
                self.not_account_stock_dict[order_no]['체결량'] = ok_quantity

            if sPrevNext == '2':
                self.detail_account_mystock(sPrevNext='2')
            else:
                self.detail_mystock_event_loop.exit()
        
        elif sRQName == '주식일봉차트조회':
            code = self.dynamicCall('GetCommData(QString, QString, int, QString)', sTrCode ,sRQName, 0, '종목코드')
            code = code.strip()
            print('일봉데이터 요청: ', code)

            if sPrevNext == '2':
                self.day_kw_db(code=code, sPrevNext=sPrevNext)
            else:
                self.calculator_event_loop.exit()

        elif sRQName == '주식기본정보요청':
            code = self.dynamicCall('GetCommData(QString, QString, int, QString)', sTrCode ,sRQName, 0, '종목코드')
            code = code.strip()
            # print('주식기본정보요청: ', code)

            self.company_basic_infos_dict[code] = {}
            comname = self.dynamicCall('GetCommData(String, String, int, String)', sTrCode, sRQName, '0', '종목명')
            self.company_basic_infos_dict[code]['종목명'] = comname.strip()
            selfmoney = self.dynamicCall('GetCommData(String, String, int, String)', sTrCode, sRQName, '0', '자본금')
            self.company_basic_infos_dict[code]['자본금'] = selfmoney.strip()
            PER = self.dynamicCall('GetCommData(String, String, int, String)', sTrCode, sRQName, '0', 'PER')
            self.company_basic_infos_dict[code]['PER'] = PER.strip()
            EPS = self.dynamicCall('GetCommData(String, String, int, String)', sTrCode, sRQName, '0', 'EPS')
            self.company_basic_infos_dict[code]['EPS'] = EPS.strip()
            ROE = self.dynamicCall('GetCommData(String, String, int, String)', sTrCode, sRQName, '0', 'ROE')
            self.company_basic_infos_dict[code]['ROE'] = ROE.strip()
            PBR = self.dynamicCall('GetCommData(String, String, int, String)', sTrCode, sRQName, '0', 'PBR')
            self.company_basic_infos_dict[code]['PBR'] = PBR.strip()
            EV = self.dynamicCall('GetCommData(String, String, int, String)', sTrCode, sRQName, '0', 'EV')
            self.company_basic_infos_dict[code]['EV'] = EV.strip()
            BPS = self.dynamicCall('GetCommData(String, String, int, String)', sTrCode, sRQName, '0', 'BPS')
            self.company_basic_infos_dict[code]['BPS'] = BPS.strip()
            salestotal = self.dynamicCall('GetCommData(String, String, int, String)', sTrCode, sRQName, '0', '매출액')
            self.company_basic_infos_dict[code]['매출액'] = salestotal.strip()
            earnmoney = self.dynamicCall('GetCommData(String, String, int, String)', sTrCode, sRQName, '0', '영업이익')
            self.company_basic_infos_dict[code]['영업이익'] = earnmoney.strip()
            earnmoney_year = self.dynamicCall('GetCommData(String, String, int, String)', sTrCode, sRQName, '0', '당기순이익')
            self.company_basic_infos_dict[code]['당기순이익'] = earnmoney_year.strip()

            print(self.company_basic_infos_dict[code]['종목명'], code)
            print('자본금: ', self.company_basic_infos_dict[code]['자본금'])
            print('매출액: ', self.company_basic_infos_dict[code]['매출액'])
            print('영업이익: ', self.company_basic_infos_dict[code]['영업이익'])
            print('당기순이익: ', self.company_basic_infos_dict[code]['당기순이익'])
            print('PER: ', self.company_basic_infos_dict[code]['PER'])
            print('EPS: ', self.company_basic_infos_dict[code]['EPS'])
            print('ROE: ', self.company_basic_infos_dict[code]['ROE'])
            
            
            
            if sPrevNext == '2':
                self.com_basic_info(code=code, sPrevNext=sPrevNext)
            else:
                self.calculator_event_loop.exit()


