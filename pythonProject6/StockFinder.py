import sys
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

form_class = uic.loadUiType("stockFinder.ui")[0]
x = np.arange(0.0, 2 * np.pi, 0.1)
sin_y = np.sin(x)
cos_y = np.cos(x)
h = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
t = [30, 32, 34, 32, 33, 31, 29, 32, 35, 45]
engine = 'yahoo'
start = datetime.datetime(2019, 1, 1)
end = datetime.datetime.now()


class MyWindow(QMainWindow, form_class):
    def __init__(self):
        root = tkinter.Tk()
        root.withdraw()
        super().__init__()
        self.setupUi(self)

        self.SDR = stockReader()

        self.bar(h, t)
        self.plot(h, t)

        btn1 = self.pushButton
        btn1.clicked.connect(self.btn1_clicked)

    def btn1_clicked(self):
        # 조회
        id = self.lineEdit.text()
        if self.if_integer(id):  #종목코드로 입력했을 경우
            msg.showwarning('안내', '주식의 종목이름을 정확히 입력해주세요')

        code = self.SDR.get_stock_code(id) + '.ks'
        print(code)
        result = self.SDR.get_stock(code, engine, start, end)
        print(result)

    def if_integer(self, st):
        reg_exp = "[-+]?\d+$"
        return re.match(reg_exp, st) is not None

    def plot(self, hour, temperature):
        self.graphWidget.plot(hour, temperature)
        self.graphWidget.setBackground('w')

    def bar(self, hour, temperature):
        w = self.graphWidget2
        w.setBackground('w')

        # 값에 해당 하는 바를 그린 뒤에 위젯에 삽입 해야 한다
        bar = pg.BarGraphItem(x=hour, height=temperature, width=0.3)
        w.addItem(bar)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
