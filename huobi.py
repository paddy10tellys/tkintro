
import pandas as pd  # data manipulation
import numpy as np  # number crunching
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker

import numpy as np
import urllib
import json
from urllib.request import urlopen
import datetime as dt
from dateutil.parser import parse
from datetime import datetime  # otherwise huobi timestamp conversion does not work
import time
import pytz
from time import strftime, gmtime, localtime
import copy



#urlToVisit = 'http://api.huobi.com/staticmarket/depth_btc_10.js'
#urlToVisit = 'http://api.huobi.com/usdmarket/ticker_btc_json.js'
urlToVisit = 'http://api.huobi.com/usdmarket/depth_btc_10.js'
sourceCode = urllib.request.urlopen(urlToVisit)
sourceCode = sourceCode.read().decode("utf-8")
sourceCode = json.loads(sourceCode)

# for key in sourceCode.keys():
#                         val =sourceCode[key]
#                         print("Key", key, 'points to', val)
# for k, v in sourceCode.items(): # get the key value pairs i.e., the two dictionaries
#     if k == 'ts':  # work on the 'ticker dictionary'
#         print(v)

tmStp = (sourceCode['ts'])  # is an int
print(tmStp)
print(type(tmStp)) # is an int

tmStp = (
    dt.datetime.fromtimestamp(
        int(tmStp/1000)
    ).strftime('%Y-%m-%d %H:%M:%S'))
print(type(tmStp))  # is an str
print(tmStp)

t=pd.to_datetime(str(tmStp))
timestring = t.strftime('%Y%m%d')
print('timestring is ',timestring)
print(type(timestring))

# tmStp = dt.datetime.strptime(tmStp, '%Y-%m-%d %H:%M:%S')  # is a datetime
# print(type(tmStp))
# tmStp = tmStp.isoformat()
# print(tmStp)
# print(type(tmStp))

# dt64 = np.datetime64(tmStp).astype("datetime64[s]")
# print(dt64)
# print(type(dt64))

def writeExchangeData(str):
    try:
        exchangeFile = 'Huobi.txt'
        with open(exchangeFile, "a") as f:
            f.write(str)
    except Exception as e:
        print("Failed because of: ", e)

for x in sourceCode.items():
            key = x[0]
            val = x[1]
            if x[0] == 'asks':
                myAskList = (val)
                for y in myAskList:
                    askP = np.array([0])    # y[0] & y[1] are floats
                    addAsks = (timestring, y[0], y[1], 'asks')  # is a tuple
                    s1=""  # map() returns a list from an iterable
                    s1 += "(" + ', '.join(map(str,addAsks)) + ")"
                    print(s1)  # csv strings ask price, ask size, ask signifier

                    unwanted=")'("              # the unwanted crap
                    for ch in unwanted:
                        if ch == ')':
                            s1 = s1.replace(ch, "\n")  # nice lines ok!

                    for ch in unwanted:
                            s1 = s1.replace(ch, "")  # clean up the crap

                    commaCount = 0
                    for i in range(0,len(s1)):
                        if (s1[i]==","):  # every comma
                            commaCount+=commaCount
                            if commaCount ==4: # prepends each new line
                                s1 = s1[:i] + "" + s1[i+1:]  # remove
                                # otherwise each line is comma prepended

                    writeExchangeData(s1)


            elif x[0] == 'bids':
                mySellsList = (val)  # gets out the sells[price, amount] data
                for y in mySellsList:
                    sellP = np.array([0])
                    addSells = (timestring, y[0], y[1], 'bids')  # the BTC price in USD, the amount of BTC
                    s1=""
                    s1 += "(" + ', '.join(map(str,addSells)) + ")"
                    print(s1)
                    unwanted=")'("
                    for ch in unwanted:
                        if ch == ')':
                            s1 = s1.replace(ch, "\n")

                    for ch in unwanted:
                            s1 = s1.replace(ch, "")

                    commaCount = 0
                    for i in range(0,len(s1)):
                        if (s1[i]==","):
                            commaCount+=commaCount
                            if commaCount ==4:
                                s1 = s1[:i] + "" + s1[i+1:]

                    writeExchangeData(s1)

def graphData():
    from matplotlib.dates import bytespdate2num
    try:
        date, askPrice, askSize, bidPrice, bidSize, volume = np.loadtxt('obi.txt',delimiter=',',unpack=True, converters={ 0: mdates.bytespdate2num('%Y%m%d')})
        # floatDate, askPrice, askSize, bidPrice = np.loadtxt('Huobi.txt',delimiter=',',unpack=True, converters={ 0: mdates.bytespdate2num('%Y%m%d')})
        # for eachDate in floatDate:
        #     intDate = [int(eachDate)]
        # for eachDate in intDate:
        #     date = [dt.datetime.fromtimestamp(eachDate)]

        fig = plt.figure()
        ax1 = plt.subplot(1,1,1)
        ax1.plot(date, askPrice)
        ax1.plot(date, bidPrice)

        plt.show()
    except Exception as e:
        print("graphData() failed because of: ", e)


graphData()
time.sleep(555)


# tmStp2 = time.strftime("%a %d %b %Y %H:%M:%S", time.gmtime(tmStp / 1000.0))
# #tmStp2 = tmStp2[0]  # class 'pandas.tslib.Timestamp is a str
# print(tmStp2, askP)

# tz = pytz.timezone('Europe/London')
# dt = datetime.now(tz)
# dt64 = np.datetime64(dt)
# ts = (dt64 - np.datetime64('1970-01-01T00:00:00Z')) / np.timedelta64(1, 's')
# print(dt64)
# print('it is ',dt64)
# print(ts)
# print(type(ts))




# exchange = "Huobi"

# def pullData(exchange):
#     global addAsks, addSells
#     try:
#         exchangeFile = exchange+'.txt'
#         with open(exchangeFile, "a") as f:
#             f.write(A LONG CONCATANATION STRING IN HERE)
#     except Exception as e:
#         print("Failed because of: ", e)

# pullData(exchange)


#             pullData(exchange)

# def getData(exchange):
#     try:
#         exchangeFile = exchange+'.txt'
#         #date, askP = np.loadtxt(exchangeFile, delimiter=',', usecols=range(2))
#         #print(date, askP)
#     except Exception as e:
#         print("Failed because of: ", e)

# getData(exchange)

# fig, ax = plt.subplots()
# ax.plot(ts, askP)
# plt.xlabel("Date")
# plt.ylabel("Ask Price")
# ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
# ax.format_ydata = askP
# ax.grid(True)
# ax.autoscale_view()
# fig.autofmt_xdate()
# plt.show()
