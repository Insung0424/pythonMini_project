import pandas_datareader.data as web
import datetime
import pandas as pd
import numpy as np
from selenium import webdriver
import requests
import re
from bs4 import BeautifulSoup
import csv


url = 'https://finance.naver.com/'

class stockReader():
    # def __init__(self):
    #     super().__init__()
    #     self.get_stock_code('3S')

    def get_stock_code(self, id):
        f = open('KOSDAQ.csv', 'r')
        readFile = csv.reader(f)
        code = None
        for data in readFile:
            if id == data[1]:
                code = data[0]
        f.close()

        if code == None:
            f = open('KOSPI.csv', 'r')
            readFile = csv.reader(f)
            for data in readFile:
                if id == data[1]:
                    code = data[0]
            f.close()

        return code

    def get_stock(self, name, engine, b_day, e_day):

        data = web.DataReader(name, engine, b_day, e_day)
        nonZdata = data[data['Volume'] != 0]

        print(nonZdata)

        return nonZdata



# c = stockReader()
# Close5 = new_gs['Adj Close'].rolling(window=5).mean()
# new_gs.insert(len(new_gs.columns), "Close5", Close5)
#
# Close20 = new_gs['Adj Close'].rolling(window=20).mean()
# new_gs.insert(len(new_gs.columns), "Close20", Close20)
#
# Close60 = new_gs['Adj Close'].rolling(window=60).mean()
# new_gs.insert(len(new_gs.columns), "Close60", Close60)
#
# Close120 = new_gs['Adj Close'].rolling(window=120).mean()
# new_gs.insert(len(new_gs.columns), "Close120", Close120)
#
# plt.plot(new_gs.index, new_gs['Adj Close'], label='Adj Close')
# plt.plot(new_gs.index, new_gs['Close5'], label="Close5")
# plt.plot(new_gs.index, new_gs['Close20'], label="Close20")
# plt.plot(new_gs.index, new_gs['Close60'], label="Close60")
# plt.plot(new_gs.index, new_gs['Close120'], label="Close120")
#
# plt.legend(loc='best')
# plt.grid()
# plt.show()