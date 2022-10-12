import requests
import re
import pandas as pd
from bs4 import BeautifulSoup
import datetime
import webreader
import numpy as np

code = '035720'

def get_financial_statements(code):
    re_enc = re.compile("encparam: '(.*)'", re.IGNORECASE)
    re_id = re.compile("id: '([a-zA-Z0-9]*)' ?", re.IGNORECASE)

    url = "http://companyinfo.stock.naver.com/v1/company/c1010001.aspx?cmp_cd={}".format(code)
    html = requests.get(url).text
    encparam = re_enc.search(html).group(1)
    encid = re_id.search(html).group(1)

    url = "http://companyinfo.stock.naver.com/v1/company/ajax/cF1001.aspx?cmp_cd={}&fin_typ=0&freq_typ=A&encparam={}&id={}".format(code, encparam, encid)
    headers = {"Referer": "HACK"}
    html = requests.get(url, headers=headers).text

    dfs = pd.read_html(html)
    df = dfs[1]['연간연간컨센서스보기']
    df.index = dfs[1]['주요재무정보'].values.flatten()
    df = df.loc['현금배당수익률']
    df.index = df.index.str[:7]

    return df.to_dict()

def get_3year_treasury():
    url = "http://www.index.go.kr/strata/jsp/showStblGams3.jsp?stts_cd=288401&amp;idx_cd=2884&amp;freq=Y&amp;period=1998:2022"
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html5lib')
    td_data = soup.select('tr td')

    treasury = {}
    start_year = 1998

    for x in td_data:
        treasury[start_year] = x.text
        start_year += 1

    return treasury


def get_dividend_yield(code):
    url = "http://companyinfo.stock.naver.com/company/c1010001.aspx?cmp_cd=" + code
    html = requests.get(url).text

    soup = BeautifulSoup(html, 'html5lib')
    dt_data = soup.select("td dl dt")

    dividend_yield = dt_data[-2].text
    dividend_yield = dividend_yield.split(' ')[1]
    dividend_yield = dividend_yield[:-1]

    return dividend_yield


def get_estimated_dividend_yield(code):
    dividend_yield = get_financial_statements(code)
    dividend_yield = sorted(dividend_yield.items())[-1]
    return dividend_yield[1]


def get_current_3year_treasury():
    url = "http://finance.naver.com/marketindex/interestDailyQuote.nhn?marketindexCd=IRR_GOVT03Y&page=1"
    html = requests.get(url).text

    soup = BeautifulSoup(html, 'html5lib')
    td_data = soup.select("tr td")
    return td_data[1].text


def get_previous_dividend_yield(code):
    dividend_yield = get_financial_statements(code)

    now = datetime.datetime.now()
    cur_year = now.year

    div_key = []
    previous_dividend_yield = {}

    for k in dividend_yield:
        div_key.append(k[:4])

    for year in range(cur_year-5, cur_year+1):
        if str(year) in div_key:
            previous_dividend_yield = dividend_yield

    return previous_dividend_yield


if __name__ == "__main__":
    dividend_dict = get_financial_statements(code)
    year_3 = get_3year_treasury()
    dividend_yield = get_dividend_yield(code)
    estimated_dividend_yield = get_estimated_dividend_yield(code)
    current = get_current_3year_treasury()
    # year_5 = get_previous_dividend_yield(code)

    print(dividend_dict)
    print(year_3)
    print(dividend_yield)
    print(estimated_dividend_yield)
    print(current)
    print(get_previous_dividend_yield(code))



