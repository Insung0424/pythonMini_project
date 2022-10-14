import sys

import pandas
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import pandas_datareader.data as web
import pandas as pd
from pandas import DataFrame as df
from pandas import Series
import numpy as np
import pyqtgraph as pg
import re
import tkinter
from tkinter import messagebox as msg
import datetime
from stockReader import *
import matplotlib

# 그래프 폰트 크기 조절
matplotlib.rc('xtick', labelsize=7)
matplotlib.rc('ytick', labelsize=7)
# UI 불러오기
form_class = uic.loadUiType("stockFinder.ui")[0]
# 검색 엔진
engine = 'yahoo'
# 검색 기간
start = datetime.datetime(2019, 1, 1)
end = datetime.datetime.now()


class MyWindow(QMainWindow, form_class):

    def __init__(self):

        root = tkinter.Tk()
        root.withdraw()
        super().__init__()
        self.setupUi(self)

        self.SDR = stockReader()
        self.get_result = None

        self.fig1 = None
        self.top_axes = None
        self.bottom_axes = None
        self.canvas1 = None

        # self.fig1.tight_layout()  # 자동으로 그래프를 최대 크기로 늘려줌

        # self.fig1 = plt.Figure()
        # self.ax = self.fig1.add_subplot(111)
        # self.canvas1 = FigureCanvas(self.fig1)

        btn1 = self.pushButton
        btn1.clicked.connect(self.btn1_clicked)

        btn2 = self.pushButton_2
        btn2.clicked.connect(self.btn2_clicked)

        btn3 = self.pushButton_3
        btn3.clicked.connect(self.btn3_clicked)

        btn4 = self.pushButton_4
        btn4.clicked.connect(self.btn4_clicked)

        btn5 = self.pushButton_5
        btn5.clicked.connect(self.btn5_clicked)

        # barItem
        btn6 = self.pushButton_6
        btn6.clicked.connect(self.btn6_clicked)

    def create_canvas(self):
        self.fig1 = plt.figure(figsize=(12, 8))
        self.top_axes = plt.subplot2grid((4, 4), (0, 0), rowspan=3, colspan=4)
        self.bottom_axes = plt.subplot2grid((4, 4), (3, 0), rowspan=1, colspan=4)
        self.canvas1 = FigureCanvas(self.fig1)

        box1 = self.verticalLayout  # 상하 LayOut 2개를 생성하려다 더 좋은 방법 발견해서 1개로 진행
        box1.addWidget(self.canvas1)  # 그림판 위치 잡기

    def delete_canvas(self):
        box1 = self.verticalLayout
        box1.removeWidget(self.canvas1)

        self.fig1 = None
        self.top_axes = None
        self.bottom_axes = None
        self.canvas1 = None

    def btn1_clicked(self):
        if self.fig1 is None:
            self.create_canvas()
        else:
            self.delete_canvas()
            self.create_canvas()
        # 조회
        id = self.lineEdit.text()
        if self.if_integer(id):  # 종목코드 또는 숫자로 입력했을 경우
            msg.showwarning('안내', '주식의 종목이름을 정확히 입력해주세요')
            return

        code = self.SDR.get_stock_code(id)
        if self.SDR.get_stock_code(id) is None:
            msg.showwarning('안내', '주식의 종목이름을 정확히 입력해주세요')
            return

        code = code + '.ks'
        print(code)
        result = self.SDR.get_stock(code, engine, start, end)
        self.get_result = result

        self.top_axes.plot(result.index, result['Adj Close'], label='Adj Close')
        self.top_axes.legend(loc='best')
        self.top_axes.grid()
        self.canvas1.draw()

        self.pushButton_2.setEnabled(True)
        self.pushButton_3.setEnabled(True)
        self.pushButton_4.setEnabled(True)
        self.pushButton_5.setEnabled(True)
        self.pushButton_6.setEnabled(True)

    def btn2_clicked(self):
        result = self.get_result
        if result is None:
            msg.showwarning('안내', '종목조회를 먼저해주세요')
            return

        Close5 = result['Adj Close'].rolling(window=5).mean()
        result.insert(len(result.columns), "Close5", Close5)
        self.top_axes.plot(result.index, result['Close5'], '-.', label="Close5")
        self.top_axes.legend(loc='best')
        self.canvas1.draw()

        self.pushButton_2.setEnabled(False)

    def btn3_clicked(self):
        result = self.get_result
        if result is None:
            msg.showwarning('안내', '종목조회를 먼저해주세요')
            return

        Close20 = result['Adj Close'].rolling(window=20).mean()
        result.insert(len(result.columns), "Close20", Close20)
        self.top_axes.plot(result.index, result['Close20'], '--', label="Close20")
        self.top_axes.legend(loc='best')
        self.canvas1.draw()

        self.pushButton_3.setEnabled(False)

    def btn4_clicked(self):
        result = self.get_result
        if result is None:
            msg.showwarning('안내', '종목조회를 먼저해주세요')
            return

        Close60 = result['Adj Close'].rolling(window=60).mean()
        result.insert(len(result.columns), "Close60", Close60)
        self.top_axes.plot(result.index, result['Close60'], ':', label="Close60")
        self.top_axes.legend(loc='best')
        self.canvas1.draw()

        self.pushButton_4.setEnabled(False)

    def btn5_clicked(self):
        result = self.get_result
        if result is None:
            msg.showwarning('안내', '종목조회를 먼저해주세요')
            return

        Close120 = result['Adj Close'].rolling(window=120).mean()
        result.insert(len(result.columns), "Close120", Close120)
        self.top_axes.plot(result.index, result['Close120'], label="Close120")
        self.top_axes.legend(loc='best')
        self.canvas1.draw()

        self.pushButton_5.setEnabled(False)

    # barGraph
    def btn6_clicked(self):
        result = self.get_result
        if result is None:
            msg.showwarning('안내', '종목조회를 먼저해주세요')
            return

        # 거래량 값으로서 큰 값이 발생할 때 그 값을 오일러 상수(e)의 지수 형태로 표현되지 않게 해줍니다.
        self.bottom_axes.get_yaxis().get_major_formatter().set_scientific(False)

        self.bottom_axes.bar(result.index, result['Volume'])

        self.canvas1.draw()

        self.pushButton_6.setEnabled(False)

    def if_integer(self, st):
        reg_exp = "[-+]?\d+$"
        return re.match(reg_exp, st) is not None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
