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
        print('키움 Class Initailize')
        print('-' * 25)

        ######### event loop initialize ######
        self.login_event_loop = None
        self.detail_account_event_loop = QEventLoop()
        self.basic_info_event_loop = QEventLoop()
        self.ilbong_event_loop = QEventLoop()
        ######################################

        ######## 내 돈 관련 변수들 ############
        self.mymoney = {}
        ######################################

        ######## 스크린 번호 관련 변수들 ############
        self.screen_my_info = 2000
        self.screen_real_stock = 5000
        self.screen_meme_stock = 5500
        self.screen_start_stop_real = 1000
        ######################################

        # BackGround 에서 계속 수행되고 있을 애들
        self.__get_ocs_instance()
        self.__event_slots()
        self.__real_event_slots()

        ######## 실시간 관련 함수들 ############
        self.realType = RealType() # at config.py
        # 장 시작 시간을 확인
        self.dynamicCall('SetRealReg(QString, QString, QString, QString)', 
                            self.screen_start_stop_real,
                            '', # 장 시간 확인이므로 기업코드는 빈 값.
                            self.realType.REALTYPE['장시작시간']['장운영구분'],
                            '0' # 처음 등록할 때 0이고 (초기화 됨), 추가할 때는 '1'로 등록해야 함.
                            )
        ######################################
        

    def __get_ocs_instance(self):
        self.setControl('KHOPENAPI.KHOpenAPICtrl.1')

    def __event_slots(self):
        self.OnEventConnect.connect(self.__login_slot)
        self.OnReceiveTrData.connect(self.__trdata_slot)

    def __real_event_slots(self):
        self.OnReceiveRealData.connect(self.__realdata_slot)

    def __login_slot(self, errCode):
        print(errors(errCode))

        self.login_event_loop.exit()

    ########################################
    ### TR slot 함수
    ##### CommRqData 가 있으면 여기 들어가야함.
    ########################################

    def __trdata_slot(self, sScrNo, sRQName, sTrCode, sRecordName, sPrevNext):
        if sRQName == '예수금상세요청':
            self.mymoney['예수금'] = self.dynamicCall('GetCommData(String, String, int, String)', sTrCode, sRQName, '0', '예수금')
            self.mymoney['출금가능금액'] = self.dynamicCall('GetCommData(String, String, int, String)', sTrCode, sRQName, '0', '출금가능금액')
            self.detail_account_event_loop.exit()
        elif sRQName == '주식기본정보요청':
            code = self.dynamicCall('GetCommData(QString, QString, int, QString)', sTrCode ,sRQName, 0, '종목코드')
            code = code.strip()

            self.company_basic_infos_dict = {}
            comname = self.dynamicCall('GetCommData(String, String, int, String)', sTrCode, sRQName, '0', '종목명')
            self.company_basic_infos_dict['종목명'] = comname.strip()
            selfmoney = self.dynamicCall('GetCommData(String, String, int, String)', sTrCode, sRQName, '0', '자본금')
            self.company_basic_infos_dict['자본금'] = selfmoney.strip()
            PER = self.dynamicCall('GetCommData(String, String, int, String)', sTrCode, sRQName, '0', 'PER')
            self.company_basic_infos_dict['PER'] = PER.strip()
            EPS = self.dynamicCall('GetCommData(String, String, int, String)', sTrCode, sRQName, '0', 'EPS')
            self.company_basic_infos_dict['EPS'] = EPS.strip()
            ROE = self.dynamicCall('GetCommData(String, String, int, String)', sTrCode, sRQName, '0', 'ROE')
            self.company_basic_infos_dict['ROE'] = ROE.strip()
            PBR = self.dynamicCall('GetCommData(String, String, int, String)', sTrCode, sRQName, '0', 'PBR')
            self.company_basic_infos_dict['PBR'] = PBR.strip()
            EV = self.dynamicCall('GetCommData(String, String, int, String)', sTrCode, sRQName, '0', 'EV')
            self.company_basic_infos_dict['EV'] = EV.strip()
            BPS = self.dynamicCall('GetCommData(String, String, int, String)', sTrCode, sRQName, '0', 'BPS')
            self.company_basic_infos_dict['BPS'] = BPS.strip()
            salestotal = self.dynamicCall('GetCommData(String, String, int, String)', sTrCode, sRQName, '0', '매출액')
            self.company_basic_infos_dict['매출액'] = salestotal.strip()
            earnmoney = self.dynamicCall('GetCommData(String, String, int, String)', sTrCode, sRQName, '0', '영업이익')
            self.company_basic_infos_dict['영업이익'] = earnmoney.strip()
            earnmoney_year = self.dynamicCall('GetCommData(String, String, int, String)', sTrCode, sRQName, '0', '당기순이익')
            self.company_basic_infos_dict['당기순이익'] = earnmoney_year.strip()
            cur_price = self.dynamicCall('GetCommData(String, String, int, String)', sTrCode, sRQName, '0', '현재가')
            self.company_basic_infos_dict['현재가'] = cur_price.strip()

            self.basic_info_event_loop.exit()

        elif sRQName == '주식일봉차트조회':
            code = self.dynamicCall('GetCommData(QString, QString, int, QString)', sTrCode ,sRQName, 0, '종목코드')
            code = code.strip()
            print('일봉데이터 요청: ', code)

            cnt = self.dynamicCall('GetRepeatCnt(QString, QString)', sTrCode, sRQName)
            for i in range(cnt):
                data = []
                cur_price = self.dynamicCall('GetCommData(QString, QString, int, QString)', sTrCode ,sRQName, i, '현재가')
                value = self.dynamicCall('GetCommData(QString, QString, int, QString)', sTrCode ,sRQName, i, '거래량')
                trading_value = self.dynamicCall('GetCommData(QString, QString, int, QString)', sTrCode ,sRQName, i, '거래대금')
                date = self.dynamicCall('GetCommData(QString, QString, int, QString)', sTrCode ,sRQName, i, '일자')
                start_price = self.dynamicCall('GetCommData(QString, QString, int, QString)', sTrCode ,sRQName, i, '시가')
                high_price = self.dynamicCall('GetCommData(QString, QString, int, QString)', sTrCode ,sRQName, i, '고가')
                low_price = self.dynamicCall('GetCommData(QString, QString, int, QString)', sTrCode ,sRQName, i, '저가')

                data.append('')
                data.append(cur_price.strip())
                data.append(value.strip())
                data.append(trading_value.strip())
                data.append(date.strip())
                data.append(start_price.strip())
                data.append(high_price.strip())
                data.append(low_price.strip())
                data.append('')

                self.prev_ilbong_data.append(data)
            
            # print(len(self.prev_ilbong_data))

            if sPrevNext == '2':
                self.day_ilbong_db(code=code, sPrevNext=sPrevNext)
            else:
                self.ilbong_event_loop.exit()

    ########################################
    ### 실시간 데이터 slot 함수
    ##### CommRqData 가 있으면 여기 들어가야함.
    ########################################

    def __realdata_slot(self, sCode, sRealType, sRealData):
        print('--------------- test')
        if sRealType == '장시작시간':
            fid = self.realType.REALTYPE[sRealType]['장운영구분']
            value = self.dynamicCall('GetCommRealData(QString, int)', sCode, fid)

            if value == '0':
                print('장 시작 (9시) 전')
            elif value == '3':
                print('장 시작')
            elif value == '2':
                print('장 종료, 동시호가로 넘어감')
            elif value == '4':
                print('장 종료 (3시 30분)')

    ########################################
    ### 실행 함수들
    ########################################

    def signal_login_commConnect(self):
        self.dynamicCall('CommConnect()')
        self.login_event_loop = QEventLoop()
        self.login_event_loop.exec_()

    def get_account_info(self):
        acount_list = self.dynamicCall("GetLogininfo(String)", "ACCNO")
        return acount_list.split(';')[:-1]

    def detail_account_info(self, acount_num, password='0000'):
        # print('예수금상세요청 요청하기')

        self.dynamicCall('SetInputValue(String, String)', '계좌번호', acount_num)
        self.dynamicCall('SetInputValue(String, String)', '비밀번호', password)
        self.dynamicCall('SetInputValue(String, String)', '비밀번호입력매체구분', '00')
        self.dynamicCall('SetInputValue(String, String)', '조회구분', '2')
        self.dynamicCall('CommRqData(String, String, int, String)', '예수금상세요청', 'opw00001', '0', '1000')

        self.detail_account_event_loop.exec_()

        return self.mymoney
    
    def get_code_list_by_market(self, market_code):
        '''
        market_code - 0: 장내, 1: 코스닥
        '''
        code_list = self.dynamicCall('GetCodeListByMarket(QString)', market_code)
        return code_list.split(';')[:-1]

    def com_basic_info(self, code=None, screen_stock_infos=None, date=None, sPrevNext='0'):
        QTest.qWait(3600)

        self.dynamicCall('SetInputValue(QString, QString)', '종목코드', code)

        if date != None:
            self.dynamicCall('SetInputValue(QString, QString)', '기준일자', date)

        self.dynamicCall('CommRqData(String, String, int, String)', '주식기본정보요청', 'opt10001', sPrevNext, screen_stock_infos)

        self.basic_info_event_loop.exec_()

        return self.company_basic_infos_dict

    def day_ilbong_db(self, code=None, screen_ilbong_stock=None, date=None, sPrevNext='0'):
        QTest.qWait(3600)

        if sPrevNext=='0':
            self.prev_ilbong_data = []

        if not screen_ilbong_stock == None:
            self.screen_ilbong_stock = screen_ilbong_stock

        self.dynamicCall('SetInputValue(QString, QString)', '종목코드', code)
        self.dynamicCall('SetInputValue(QString, QString)', '수정주가구분', '1')

        if date != None:
            self.dynamicCall('SetInputValue(QString, QString)', '기준일자', date)

        self.dynamicCall('CommRqData(String, String, int, String)', '주식일봉차트조회', 'opt10081', sPrevNext, self.screen_ilbong_stock)

        if sPrevNext=='0':
            self.ilbong_event_loop.exec_()

        return self.prev_ilbong_data

    def screen_number_setting(self):
        '''
        각 스크린에 종목이 겹치는 애들이 없는지 확인하고 재분배
        이 코드는 지금 돌지 않음... 빈 것 채워줘야 함.
        '''

        screen_overwrite = []

        # 계좌평가잔고내역에 있는 종목들
        for code in self.acount_stock_dict.keys():
            if code not in screen_overwrite:
                screen_overwrite.append(code)

        # 미체결에 있는 종목들
        for order_number in self.not_account_stock_dict.keys():
            code = self.not_account_stock_dict[order_number]['종목코드']
            if code not in screen_overwrite:
                screen_overwrite.append(code)

        # 포트폴리오(내가 살 것)에 있는 종물들
        for code in self.portfolio_stock_dict.keys():
            if code not in screen_overwrite:
                screen_overwrite.append(code)

        # 스크린번호 할당
        ##### portfolio_stock_dict 에 있는 항목들을 실시간으로 업데이트 하려고...
        cnt = 0
        for code in screen_overwrite:
            if (cnt % 50) == 0:
                self.screen_real_stock += 1
                self.screen_meme_stock += 1

            if not code in self.portfolio_stock_dict.keys():
                self.portfolio_stock_dict[code] = {}
            self.portfolio_stock_dict[code]['스크린번호'] = str(self.screen_real_stock)
            self.portfolio_stock_dict[code]['주문용스크린번호'] = str(self.screen_meme_stock)
            cnt += 1


        