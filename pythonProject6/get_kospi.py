import pandas
import requests
from bs4 import BeautifulSoup
from io import BytesIO

# 0. 공통 헤더
headers = {'Referer': 'http://data.krx.co.kr/contents/MDC/MDI/mdiLoader'}

# 1. OTP 받기
otp_url = 'http://data.krx.co.kr/comm/fileDn/GenerateOTP/generate.cmd'
otp_data = {
    'locale': 'ko_KR',
    'mktId': 'KSQ',  # STK = kospi   KSQ = kosdaq
    'share': '1',
    'csvxls_isNo': 'false',
    'name': 'fileDown',
    'url': 'dbms/MDC/STAT/standard/MDCSTAT01901'
}
otp = requests.post(otp_url, otp_data, headers=headers).text

# 2. 데이터 다운로드
data_url = 'http://data.krx.co.kr/comm/fileDn/download_csv/download.cmd'
data  = requests.post(data_url, {'code':otp}, headers=headers)

# 3. 판다스 DataFrame으로 변환
df = pandas.read_csv(BytesIO(data.content), encoding='EUC-KR')
# print(df)  CSV 파일로 저장하면 됨
# 인코딩 오류로 불러오질 못함 현재 cp949
df.to_csv("filename.csv", mode='w', encoding="ANSI")