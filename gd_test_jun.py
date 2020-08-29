# -*- coding: utf-8 -*-
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pdb


scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

# scope = ['https://www.googleapis.com/auth/drive']

pdb.set_trace()
credentials = ServiceAccountCredentials.from_json_keyfile_name('./data/behappy-287913-cc1952405a61.json', scope)

gs = gspread.authorize(credentials) #.open("Google Sheet Name")

doc = gs.open_by_url('https://docs.google.com/spreadsheets/d/1b4oZS7a7EzlXvYi2Xb8BJtJbboEIuteRs_wrM1yqdtg/edit#gid=0')


worksheet = doc.worksheet('test')
cell_data = worksheet.acell('B2').value
row_data = worksheet.row_values(2)

worksheet.update_acell('B1', 'b1 updated')

worksheet_0 = doc.add_worksheet(title='test2', rows='500', cols='500')

pdb.set_trace()
temp = 0
