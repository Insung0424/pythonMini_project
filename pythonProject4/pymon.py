import sys
import time
from pandas import DataFrame
import datetime
import webreader
import numpy as np

from PyQt5.QtWidgets import *
import Kiwoom

MARKET_KOSPI = 0
MARKET_KOSDAQ = 10

class PyMon:
    def __init__(self):
        self.kiwoom = Kiwoom.Kiwoom()
        self.kiwoom.comm_connect()
        self.get_code_list()

    def run(self):
        buy_list = []
        num = len(self.kosdaq_codes)

        for i, code in enumerate(self.kosdaq_codes):
            print(i, '/', num)
            if self.check_speedy_rising_volume(code):
                buy_list.append(code)

        self.update_buy_list(buy_list)

    def get_code_list(self):
        self.kospi_codes = self.kiwoom.get_code_list_by_market(MARKET_KOSPI)
        self.kosdaq_codes = self.kiwoom.get_code_list_by_market(MARKET_KOSDAQ)

    def get_ohlcv(self, code, start):
        self.kiwoom.ohlcv = {'date': [], 'open': [], 'high': [], 'low': [], 'close': [], 'volume': []}

        self.kiwoom.set_input_value('종목코드', code)
        self.kiwoom.set_input_value('기준일자', start)
        self.kiwoom.set_input_value('수정주가구분', 1)
        self.kiwoom.comm_rq_data('opt10081_req', 'opt10081', 0, '0101')
        time.sleep(3.6)

        df = DataFrame(self.kiwoom.ohlcv, columns=['open', 'high', 'low', 'close', 'volume'],
                   index=self.kiwoom.ohlcv['date'])
        return df

    def check_speedy_rising_volume(self, code):
        today = datetime.datetime.today().strftime("%Y%m%d")
        # today = '20221007'
        df = self.get_ohlcv(code, today)
        volumes = df['volume']

        if len(volumes) < 21:
            return False

        sum_vol20 = 0
        today_vol = 0

        for i, vol in enumerate(volumes):
            if i == 0:
                today_vol = vol
            elif 1 <= i <= 20:
                sum_vol20 += vol
            else:
                break

        avg_vol20 = sum_vol20 / 20
        if today_vol > avg_vol20 * 10:
            return True

    def wallet(self):
        account_number = self.kiwoom.get_login_info("ACCNO")
        account_number = account_number.split(';')[0]

        # opw00001
        self.kiwoom.set_input_value("계좌번호", account_number)
        self.kiwoom.comm_rq_data("opw00001_req", "opw00001", 0, "2000")

        # balance
        item = self.kiwoom.wallet
        my_wallet = float(self.change_format(item)) * 0.05
        int_my_wallet = int(my_wallet)

        f = open("test.txt", "wt")
        f.writelines("매수;시장가;" + str(int_my_wallet) + ";0;매수전\n")
        f.close()

    def update_buy_list(self, buy_list):

        # account_number = self.kiwoom.get_login_info("ACCNO")
        # account_number = account_number.split(';')[0]
        #
        # # opw00001
        # self.kiwoom.set_input_value("계좌번호", account_number)
        # self.kiwoom.comm_rq_data("opw00001_req", "opw00001", 0, "2000")
        #
        # # balance
        # item = QTableWidgetItem(self.kiwoom.d2_deposit)
        # my_wallet = item * 0.05
        # print(my_wallet)

        f = open("buy_list.txt", "wt")
        for code in buy_list:
            f.writelines("매수;%s;시장가;5;0;매수전\n" % (code))
        f.close()

    def calculate_estimated_dividend_to_treasury(self, code):
        estimated_dividend_yield = webreader.get_estimated_dividend_yield(code)
        current_3year_treasury = webreader.get_current_3year_treasury()
        estimated_dividend_to_treasury = float(estimated_dividend_yield) / float(current_3year_treasury)
        return estimated_dividend_to_treasury

    def get_min_max_dividend_to_treasury(self, code):
        previous_dividend_yield = webreader.get_previous_dividend_yield(code)
        three_years_treasury = webreader.get_3year_treasury()

        now = datetime.datetime.now()
        cur_year = now.year
        previous_dividend_to_treasury = {}

        for year in range(cur_year - 5, cur_year):
            if year in previous_dividend_yield.keys() and year in three_years_treasury.keys():
                ratio = float(previous_dividend_yield[year]) / float(three_years_treasury[year])
                previous_dividend_to_treasury[year] = ratio

        print(previous_dividend_to_treasury)
        min_ratio = min(previous_dividend_to_treasury.values())
        max_ratio = max(previous_dividend_to_treasury.values())

        return (min_ratio, max_ratio)

    @staticmethod
    def change_format(data):
        strip_data = data.lstrip('-0')
        if strip_data == '':
            strip_data = '0'

        return strip_data

    def run_dividend(self):
        buy_list = []

        for code in self.kospi_codes[0:50]:
            time.sleep(0.5)
            ret = self.buy_check_by_dividend_algorithm(code)
            if ret[0] == 1:
                buy_list.append((code, ret[1]))

        sorted_list = sorted(buy_list, key=lambda t: t[1], reverse=True)

        buy_list = []
        for i in range(0, 5):
            code = sorted_list[i][0]
            buy_list.append(code)

        self.update_buy_list(buy_list)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pymon = PyMon()
    pymon.run()