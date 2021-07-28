# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import pdb



# path = '../mydata/퀀트포트[20210716]_20210717_083839.csv'
# df = pd.read_csv(path)

def read_csv(csvpath = None):
    df = pd.read_csv(csvpath).values
    outputs = []
    for i in range(20):
        code = df[i,0]
        name = df[i,1]
        value = df[i,2]
        outputs.append((i,code,name,value))
    return outputs

def read_excel(excelpath, sheet_name = '실적발표후 분기만 4대포트'):
    df = pd.read_excel(excelpath, sheet_name=sheet_name)

    data = df.values
    output = {}
    output['code'] = {}
    output['code']['마법공식'] = data[:20,13]
    output['code']['저밸류'] = data[20:40,13]
    output['code']['고속성장'] = data[40:60,13]
    output['code']['슈퍼퀀트'] = data[60:80,13]

    output['name'] = {}
    output['name']['마법공식'] = data[:20,14]
    output['name']['저밸류'] = data[20:40,14]
    output['name']['고속성장'] = data[40:60,14]
    output['name']['슈퍼퀀트'] = data[60:80,14]
    return output

def get_super(quantking_list):
    codes = quantking_list['code']['슈퍼퀀트']
    names = quantking_list['name']['슈퍼퀀트']
    outputs = []
    for i in range(20):
        outputs.append((i,codes[i],names[i],-1))

    return outputs

def get_mix(quantking_list):
    codes = {}
    names = {}
    codes['슈퍼퀀트'] = quantking_list['code']['슈퍼퀀트']
    names['슈퍼퀀트'] = quantking_list['name']['슈퍼퀀트']
    codes['저밸류'] = quantking_list['code']['저밸류']
    names['저밸류'] = quantking_list['name']['저밸류']
    codes['고속성장'] = quantking_list['code']['고속성장']
    names['고속성장'] = quantking_list['name']['고속성장']
    codes['마법공식'] = quantking_list['code']['마법공식']
    names['마법공식'] = quantking_list['name']['마법공식']

    outputs = []
    checks = []
    for i in range(20):
        for q_type in ['슈퍼퀀트', '마법공식', '고속성장', '저밸류']:
            code = codes[q_type][i]
            if code in checks:
                continue
            checks.append(code)
            outputs.append((i,codes[q_type][i],names[q_type][i],-1))

    return outputs[:20]

if __name__ == '__main__':
    quantking_path = '../mydata/퀀트데이터2021.07.15(21년2Q매영순YOYQOQ).xlsx'
    quantking_sheet_name = '실적발표후 분기만 4대포트'
    quantking_list = read_excel(quantking_path,quantking_sheet_name)
    quantking_superlist = get_super(quantking_list)
    quantking_mixlist = get_mix(quantking_list)