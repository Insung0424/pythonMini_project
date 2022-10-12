from pandas import Series, DataFrame
import pandas as pd
import pandas_datareader.data as web
import datetime
import time
import matplotlib.pyplot as plt

start = datetime.datetime(2019, 1, 1)
end = datetime.datetime.now()

gs = web.DataReader('078930.KS', 'yahoo', start, end)
new_gs = gs[gs['Volume'] != 0]

Close5 = new_gs['Adj Close'].rolling(window=5).mean()
new_gs.insert(len(new_gs.columns), "Close5", Close5)

Close20 = new_gs['Adj Close'].rolling(window=20).mean()
new_gs.insert(len(new_gs.columns), "Close20", Close20)

Close60 = new_gs['Adj Close'].rolling(window=60).mean()
new_gs.insert(len(new_gs.columns), "Close60", Close60)

Close120 = new_gs['Adj Close'].rolling(window=120).mean()
new_gs.insert(len(new_gs.columns), "Close120", Close120)

plt.plot(new_gs.index, new_gs['Adj Close'], label='Adj Close')
plt.plot(new_gs.index, new_gs['Close5'], label="Close5")
plt.plot(new_gs.index, new_gs['Close20'], label="Close20")
plt.plot(new_gs.index, new_gs['Close60'], label="Close60")
plt.plot(new_gs.index, new_gs['Close120'], label="Close120")

plt.legend(loc='best')
plt.grid()
plt.show()
