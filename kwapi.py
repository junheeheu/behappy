# -*- coding: utf-8 -*-

####################################
# 설치: pip install pykiwoom
# 설명: https://wikidocs.net/77479
####################################

from pykiwoom.kiwoom import *
import pdb

trdata_list = {
    '주식기본정보요청': 'opt10001',
}

class kwapi():
    def __init__(self):
        self.kiwoom = Kiwoom()
        self.kiwoom.CommConnect(block=True)
        print("블록킹 로그인 완료")

    def get_user_infos(self):
        infos = {}
        infos['전체계좌수'] = self.kiwoom.GetLoginInfo("ACCOUNT_CNT")        # 전체 계좌수
        infos['전체계좌리스트'] = self.kiwoom.GetLoginInfo("ACCNO")                 # 전체 계좌 리스트
        infos['사용자ID'] = self.kiwoom.GetLoginInfo("USER_ID")                # 사용자 ID
        infos['사용자명'] = self.kiwoom.GetLoginInfo("USER_NAME")            # 사용자명
        return infos

    def get_company_codes_list(self):
        code_list = {}
        code_list['코스피'] = self.kiwoom.GetCodeListByMarket('0')
        code_list['코스닥'] = self.kiwoom.GetCodeListByMarket('10')
        code_list['ETF'] = self.kiwoom.GetCodeListByMarket('8')
        return code_list

    def get_company_name(self, code):
        return self.kiwoom.GetMasterCodeName(code)

    def get_lastprice_of_stock(self, code):
        return self.kiwoom.GetMasterLastPrice(code)

    def get_single_trdata4company_basic_infos(self, tr_type="주식기본정보요청", code = None):
        df = self.kiwoom.block_request(trdata_list[tr_type],
                                종목코드=code,
                                output=tr_type,
                                next=0)
        df = df.values
        keys = ['종목코드', '종목명', '결산월', '액면가', '자본금', '상장주식', '신용비율', '연중최고', '연중최저',
                '시가총액', '시가총액비중', '외인소진률', '대용가', 'PER', 'EPS', 'ROE', 'PBR', 'EV',
                'BPS', '매출액', '영업이익', '당기순이익', '250최고', '250최저', '시가', '고가', '저가',
                '상한가', '하한가', '기준가', '예상체결가', '예상체결수량', '250최고가일', '250최고가대비율',
                '250최저가일', '250최저가대비율', '현재가', '대비기호', '전일대비', '등락율', '거래량', '거래대비',
                '액면가단위', '유통주식', '유통비율']
        
        outputs = {}
        for i in range(45):
            outputs[keys[i]] = df[0,i]
        
        outputs['피벗기준선'] = int(abs(int(outputs['현재가']))+ 
                                abs(int(outputs['고가']))+
                                abs(int(outputs['저가'])))/3

        return outputs

    def get_multi_trdata4company_basic_infos(self, tr_type="주식일봉차트조회", code = None):
        # 이 부분은 짜야함.
        # dfs = []
        # df = kiwoom.block_request("opt10081",
        #                         종목코드="005930",
        #                         기준일자="20200424",
        #                         수정주가구분=1,
        #                         output="주식일봉차트조회",
        #                         next=0)
        # print(df.head())
        # dfs.append(df)

        # while kiwoom.tr_remained:
        #     df = kiwoom.block_request("opt10081",
        #                             종목코드="005930",
        #                             기준일자="20200424",
        #                             수정주가구분=1,
        #                             output="주식일봉차트조회",
        #                             next=2)
        #     dfs.append(df)
        #     time.sleep(1)

        # df = pd.concat(dfs)
        # df.to_excel("005930.xlsx")
        return

####################################
# 코스피, 코스닥 지수 가져오기
# 설치: pip install pandas_datareader
####################################

from pandas_datareader import data
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