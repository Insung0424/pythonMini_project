import pandas_datareader.data as web
import datetime
import numpy as np
from pandas_datareader._utils import RemoteDataError
from selenium import webdriver
import requests
import re
from bs4 import BeautifulSoup
import csv
import pandas_datareader.naver as web_naver
import FinanceDataReader as fdr
import pandas
import requests
from io import BytesIO


class stockReader():

    def get_stock_code(self, id):
        # 깔끔하게 .csv 파일로 만들어주는 사이트와 라이브러리가 있는데 사용안할 이유가 없음
        # url = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query={}'.format(id)
        # res = requests.get(url=url)
        # find_code = BeautifulSoup(res.text, "html.parser")
        # code = find_code.select_one('em.t_nm')
        # print(code.text)
        # print(id)
        # return code.text

        f = open('filename.csv', 'r')
        readFile = csv.reader(f)
        code = None
        for data in readFile:
            if id == data[3]:
                # code = data[0] + '.kq'  # pandas_datareader.data 에서 사용한 방식
                code = data[2]
        f.close()

        if code == None:
            f = open('KOSPI.csv', 'r')
            readFile = csv.reader(f)
            for data in readFile:
                if id == data[1]:
                    # code = data[0] + '.ks'  # pandas_datareader.data 에서 사용한 방식
                    code = data[0]
            f.close()

        return code

    def get_stock(self, name, b_day, e_day):
        data = fdr.DataReader(name, b_day, e_day)
        nonZdata = data[data['Volume'] != 0]
        return nonZdata

    def write_csv(self):
        KO = ['STK', 'KSQ']  # STK = kospi   KSQ = kosdaq
        fileName = ['KOSPI.csv', 'KOSDAQ.csv']

        for i in range(2):
            # 0. 공통 헤더
            headers = {'Referer': 'http://data.krx.co.kr/contents/MDC/MDI/mdiLoader'}

            # 1. OTP 받기
            otp_url = 'http://data.krx.co.kr/comm/fileDn/GenerateOTP/generate.cmd'
            otp_data = {
                'locale': 'ko_KR',
                'mktId': KO[i],
                'share': '1',
                'csvxls_isNo': 'false',
                'name': 'fileDown',
                'url': 'dbms/MDC/STAT/standard/MDCSTAT01901'
            }
            otp = requests.post(otp_url, otp_data, headers=headers).text

            # 2. 데이터 다운로드
            data_url = 'http://data.krx.co.kr/comm/fileDn/download_csv/download.cmd'
            data = requests.post(data_url, {'code': otp}, headers=headers)

            # 3. 판다스 DataFrame으로 변환
            df = pandas.read_csv(BytesIO(data.content), encoding='EUC-KR')

            # 4. 코스닥.csv 파일 저장
            df.to_csv(fileName[i], mode='w', encoding="ANSI")



    # 야후는 코스닥 기록을 가져오질 못하고 네이버는 y축 값에 오류가있어서 그래프가 망가짐
    # def get_stock(self, name, engine, b_day, e_day):
    #     # if engine == 'yahoo':
    #     #     data = web.DataReader(name, engine, b_day, e_day)
    #     #     nonZdata = data[data['Volume'] != 0]
    #     #     return nonZdata
    #     # else:
    #     #     data = web.DataReader(name, engine, b_day, e_day)
    #     #     nonZdata = data[data['Volume'] != 0]
    #     #     return nonZdata