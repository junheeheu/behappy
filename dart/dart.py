import urllib
import urllib.request as request
import json
import pdb
from bs4 import BeautifulSoup

K = '5c3d324c19cc602c532bbfa645848356ad167a5c'
bgn_de='20201001'
end_de='20201015'
formtypecode = 'A002'

URL = 'https://opendart.fss.or.kr/api/list.json?crtfc_key=%s&pblntf_detail_ty=%s&bgn_de=%s&end_de=%s&corp_cls=Y&page_no=%d&page_count=%d' % (
    K, formtypecode, bgn_de, end_de, 1, 100
)

RLT = request.urlopen(URL)
D = RLT.read().decode('utf-8')
pdb.set_trace()
D = json.loads(D)

print(D)

# utf-8, euc-kr