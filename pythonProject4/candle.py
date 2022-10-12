import mpl_finance
import pandas_datareader.data as web
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import matplotlib.ticker as ticker

start = datetime.datetime(2016,3,1)
end = datetime.datetime(2016,3,31)

skhynix = web.DataReader('000660.KS','yahoo',start,end)
skhynix = skhynix[skhynix['Volume'] > 0]

fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111)

name_list = []
day_list = []

for i, day in enumerate(skhynix.index):
    if day.dayofweek == 0:
        day_list.append(i)
        name_list.append(day.strftime('%Y-%m-%d') + '(Mon)')

ax.xaxis.set_major_locator(ticker.FixedLocator(day_list))
ax.xaxis.set_major_formatter(ticker.FixedFormatter(name_list))

mpl_finance.candlestick2_ohlc(ax, skhynix['Open'], skhynix['High'], skhynix['Low'], skhynix['Close'], width=0.5, colorup='r', colordown='b')
plt.grid()
plt.show()