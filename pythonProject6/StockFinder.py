import sys
import mpl_finance
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
from PyQt5.QtCore import QDate
import matplotlib.ticker as ticker

# 그래프 폰트 크기 조절
matplotlib.rc('xtick', labelsize=7)
matplotlib.rc('ytick', labelsize=7)
matplotlib.rc('font', family='NanumGothic')
# UI 불러오기
form_class = uic.loadUiType("stockFinder.ui")[0]
# # 검색 엔진
# engine = 'yahoo'


class MyWindow(QMainWindow, form_class):

    def __init__(self):

        root = tkinter.Tk()
        root.withdraw()
        super().__init__()
        self.setupUi(self)

        self.SDR = stockReader()

        #  코스피 코스닥 종목 최신화
        self.SDR.write_csv()

        self.dateEdit_2.setDate(QDate.currentDate())  # 검색종료일을 당일로 설정

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

        btn7 = self.pushButton_7
        btn7.clicked.connect(self.btn7_clicked)

        btn8 = self.pushButton_8
        btn8.clicked.connect(self.btn8_clicked)
        self.pushButton_8.setEnabled(False)

        btn9 = self.pushButton_9
        btn9.clicked.connect(self.btn9_clicked)
        self.pushButton_9.setEnabled(False)

        btn10 = self.pushButton_10
        btn10.clicked.connect(self.btn10_clicked)

    def create_canvas(self):
        self.fig1 = plt.figure(figsize=(12, 8))
        self.top_axes = plt.subplot2grid((4, 4), (0, 0), rowspan=3, colspan=4)
        self.bottom_axes = plt.subplot2grid((4, 4), (3, 0), rowspan=1, colspan=4)
        self.canvas1 = FigureCanvas(self.fig1)

        box1 = self.verticalLayout  # 상하 LayOut 2개를 생성하려다 더 좋은 방법 발견해서 1개로 진행
        box1.addWidget(self.canvas1)  # 그림판 위치 잡기
        self.pushButton_8.setEnabled(False)
        self.pushButton_9.setEnabled(False)

    def delete_canvas(self):
        # 역순으로 제거 및 None 타입 변환
        box1 = self.verticalLayout
        box1.removeWidget(self.canvas1)

        self.fig1 = None
        self.top_axes = None
        self.bottom_axes = None
        self.canvas1 = None

    # 버튼2~6까지 반복되는 부분이 많아서 만들어 보았으나 실행은 되지만 에러가 발생함
    # 함수를 중단할 수 있는 방법이 필요함
    # def is_result(self):
    #     result = self.get_result
    #     if result is None:
    #         result = msg.showwarning('안내', '종목조회를 먼저해주세요')
    #         return result
    # 
    #     return result

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
        if code is None:
            msg.showwarning('안내', '주식의 종목이름을 정확히 입력해주세요')
            return

        start = self.dateEdit.date().toString("yyyy-MM-dd")
        end = self.dateEdit_2.date().toString("yyyy-MM-dd")

        result = self.SDR.get_stock(code, start, end)

        self.get_result = result  # 다른 버튼 에서 data를 사용하기 위해 변수 설정

        self.top_axes.plot(result.index, result['Close'], label=id)
        self.top_axes.legend(loc='best')
        self.top_axes.grid()
        self.top_axes.set_ylabel('원')
        self.canvas1.draw()

        self.top_axes.set_title(id)  # 종목 이름을 타이틀로 설정

        self.pushButton_2.setEnabled(True)
        self.pushButton_3.setEnabled(True)
        self.pushButton_4.setEnabled(True)
        self.pushButton_5.setEnabled(True)
        self.pushButton_6.setEnabled(True)
        self.pushButton_8.setEnabled(True)
        self.pushButton_9.setEnabled(True)
        self.pushButton_10.setEnabled(True)

    def btn2_clicked(self):
        result = self.get_result
        if result is None:
            msg.showwarning('안내', '종목조회를 먼저해주세요')
            return

        Close5 = result['Close'].rolling(window=5).mean()
        result.insert(len(result.columns), "Close5", Close5)
        self.top_axes.plot(result.index, result['Close5'], '-.', label="5일 종가 평균")
        self.top_axes.legend(loc='best')
        self.canvas1.draw()

        self.pushButton_2.setEnabled(False)

    def btn3_clicked(self):
        result = self.get_result
        if result is None:
            msg.showwarning('안내', '종목조회를 먼저해주세요')
            return

        Close20 = result['Close'].rolling(window=20).mean()
        result.insert(len(result.columns), "Close20", Close20)
        self.top_axes.plot(result.index, result['Close20'], '--', label="20일 종가 평균")
        self.top_axes.legend(loc='best')
        self.canvas1.draw()

        self.pushButton_3.setEnabled(False)

    def btn4_clicked(self):
        result = self.get_result
        if result is None:
            msg.showwarning('안내', '종목조회를 먼저해주세요')
            return

        Close60 = result['Close'].rolling(window=60).mean()
        result.insert(len(result.columns), "Close60", Close60)
        self.top_axes.plot(result.index, result['Close60'], ':', label="60일 종가 평균")
        self.top_axes.legend(loc='best')
        self.canvas1.draw()

        self.pushButton_4.setEnabled(False)

    def btn5_clicked(self):
        result = self.get_result
        if result is None:
            msg.showwarning('안내', '종목조회를 먼저해주세요')
            return

        Close120 = result['Close'].rolling(window=120).mean()
        result.insert(len(result.columns), "Close120", Close120)
        self.top_axes.plot(result.index, result['Close120'], label="120일 종가 평균")
        self.top_axes.legend(loc='best')
        self.canvas1.draw()

        self.pushButton_5.setEnabled(False)

    # barGraph
    def btn6_clicked(self):
        self.bottom_axes.cla()
        result = self.get_result
        if result is None:
            msg.showwarning('안내', '종목조회를 먼저해주세요')
            return

        # 거래량 값으로서 큰 값이 발생할 때 그 값을 오일러 상수(e)의 지수 형태로 표현되지 않게 해줍니다.
        self.bottom_axes.get_yaxis().get_major_formatter().set_scientific(False)

        self.bottom_axes.bar(result.index, result['Volume'])

        self.canvas1.draw()

        self.pushButton_6.setEnabled(False)
        self.pushButton_10.setEnabled(True)

    def btn7_clicked(self):
        self.delete_canvas()
        self.create_canvas()

    def btn8_clicked(self):
        id = 'KS11'

        start = self.dateEdit.date().toString("yyyy-MM-dd")
        end = self.dateEdit_2.date().toString("yyyy-MM-dd")

        result = self.SDR.get_stock(id, start, end)

        self.get_result = result  # 다른 버튼 에서 data를 사용하기 위해 변수 설정

        self.top_axes.plot(result.index, result['Close'], label='코스피')
        self.top_axes.legend(loc='best')
        self.canvas1.draw()

        self.pushButton_8.setEnabled(False)

    def btn9_clicked(self):
        id = 'IXIC'

        start = self.dateEdit.date().toString("yyyy-MM-dd")
        end = self.dateEdit_2.date().toString("yyyy-MM-dd")

        result = self.SDR.get_stock(id, start, end)
        print(result)
        self.get_result = result  # 다른 버튼 에서 data를 사용하기 위해 변수 설정

        self.top_axes.plot(result.index, result['Close'], label='나스닥')
        self.top_axes.legend(loc='best')
        self.canvas1.draw()

        self.pushButton_9.setEnabled(False)

    def btn10_clicked(self):
        self.bottom_axes.cla()
        result = self.get_result
        if result is None:
            msg.showwarning('안내', '종목조회를 먼저해주세요')
            return

        # 거래량 값으로서 큰 값이 발생할 때 그 값을 오일러 상수(e)의 지수 형태로 표현되지 않게 해줍니다.
        self.bottom_axes.get_yaxis().get_major_formatter().set_scientific(False)

        day_list = []
        name_list = []
        for i, day in enumerate(result.index):
            if day.dayofweek == 0:
                day_list.append(i)
                name_list.append(day.strftime('%d') + '(Mon)')

        self.bottom_axes.xaxis.set_major_locator(ticker.FixedLocator(day_list))
        self.bottom_axes.xaxis.set_major_formatter(ticker.FixedFormatter(name_list))

        mpl_finance.candlestick2_ohlc(self.bottom_axes, result['Open'], result['High'], result['Low'], result['Close'], width=0.5,
                                      colorup='r', colordown='b')
        self.bottom_axes.grid()
        self.canvas1.draw()

        self.pushButton_10.setEnabled(False)
        self.pushButton_6.setEnabled(True)

    def if_integer(self, st):
        reg_exp = "[-+]?\d+$"
        return re.match(reg_exp, st) is not None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()


    # pandas_datareader.data 에서 사용한 방식
    # def btn1_clicked(self):
    #     if self.fig1 is None:
    #         self.create_canvas()
    #     else:
    #         self.delete_canvas()
    #         self.create_canvas()
    #     # 조회
    #     id = self.lineEdit.text()
    #     if self.if_integer(id):  # 종목코드 또는 숫자로 입력했을 경우
    #         msg.showwarning('안내', '주식의 종목이름을 정확히 입력해주세요')
    #         return
    #
    #     code = self.SDR.get_stock_code(id)
    #     if code is None:
    #         msg.showwarning('안내', '주식의 종목이름을 정확히 입력해주세요')
    #         return
    #
    #     print(code)
    #
    #     engine = self.comboBox.currentText()
    #     print(engine)
    #
    #     try:
    #
    #         if engine == 'yahoo':
    #             if code in '.ks':
    #                 result = self.SDR.get_stock(code, engine, start, end)
    #
    #                 self.get_result = result
    #
    #                 self.top_axes.plot(result.index, result['Close'], label='Close')
    #                 self.top_axes.legend(loc='best')
    #                 self.top_axes.grid()
    #                 self.canvas1.draw()
    #             else:  # 야후파이넨스에서 코스닥 최근 5년 기록을 읽어 오지 못 함
    #                 raise RemoteDataError
    #         else:
    #             print(code)
    #             result = self.SDR.get_stock(code, engine, start, end)
    #
    #             self.get_result = result
    #
    #             self.top_axes.plot(result['Close'], label='Close')
    #             self.top_axes.legend(loc='best')
    #             self.top_axes.grid()  # 격자 그리기
    #             self.canvas1.draw()
    #
    #     except RemoteDataError:
    #         msg.showwarning('안내',  engine+'에는 해당종목의 검색결과가 존재하지 않습니다')
    #         return
    #
    #     self.top_axes.set_title(id)  # 종목 이름을 타이틀로 설정
    #
    #     self.pushButton_2.setEnabled(True)
    #     self.pushButton_3.setEnabled(True)
    #     self.pushButton_4.setEnabled(True)
    #     self.pushButton_5.setEnabled(True)
    #     self.pushButton_6.setEnabled(True)