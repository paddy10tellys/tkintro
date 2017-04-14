import matplotlib
import matplotlib.animation as animation
matplotlib.use("TkAgg")  # the backend of Matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
#from matplotlib.figure import Figure
from matplotlib import style
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker


import tkinter as tk
from tkinter import ttk
import numpy as np
import urllib
import json
from urllib.request import urlopen

import datetime as dt
from dateutil.parser import parse
#from datetime import datetime  # otherwise huobi timestamp conversion does not work
import time
#import dateutil

import requests


import pandas as pd  # data manipulation
import numpy as np  # number crunching

pd.options.mode.chained_assignment = None


style.use("ggplot")
LARGE_FONT=("Verdana", 12)
NORM_FONT=("Verdana", 10)
SMALL_FONT=("Verdana", 8)

f = plt.figure()

#a = f.add_subplot(111)

exchange = "BTC-e"

# forces graph update prn, say after clicking to change to another exchange
DatCounter = 9000

programName = "btce"
resampleSize = "15min"
DataPace = "tick"
candleWidth = 0.008
paneCount = 1
topIndicator = "none"
middleIndicators = "none"
bottomIndicator = "none"
chartLoad = True

lightColor="#00A3E0"
darkColor="#183A54"

EMAs = []
SMAs = []

def loadChart(run):
    global chartLoad

    if run =="start":
        chartLoad = True

    elif run == "stop":
        chartLoad = False

def tutorial():
#    def leavemini(what):
#       what.destroy()
    def page2():
        tut.destroy()
        tut2 = tk.Tk()

        def page3():
            tut2.destroy()
            tut3 = tk.Tk()

            tut3.wm_title("Part 3!")

            label = ttk.Label(tut3, text="Part 3", font=NORM_FONT)
            label.pack(side="top", fill="x", pady=10)
            B1 = ttk.Button(tut3, text = "Done!", command=tut3.destroy)
            B1.pack()
            tut3.mainloop()

        tut2.wm_title("Part 2!")
        label = ttk.Label(tut2, text="Part 2", font=NORM_FONT)
        label.pack(side="top", fill="x", pady=10)
        B1 = ttk.Button(tut2, text = "Next", command=page3)
        B1.pack()
        tut2.mainloop()

    tut = tk.Tk()
    tut.wm_title("Tutorial")
    label =ttk.Label(tut, text="What vexes thee?", font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)

    B1 = ttk.Button(tut, text="Overview of the application", command=page2)
    B1.pack()

    B2 = ttk.Button(tut, text="How do I trade with this client", command=lambda: popupmsg("Not yet completed"))
    B2.pack()

    B3 = ttk.Button(tut, text="Indicator Questions/Help", command=lambda: popupmsg("Not yet completed"))
    B3.pack()

    tut.mainloop()



def addMiddleIndicator(what):
    global middleIndicators
    global DatCounter  # so, update "right now!"

    if DataPace == "tick":
        popupmsg("Indicators in Tick Data not available.")

    if what != "none":
        if middleIndicators == "none":  # is it currently none
            if what =="sma":
                midIQ = tk.Tk()
                midIQ.wm_title("Periods?")
                label = ttk.Label(midIQ, text="Choose how many periods you want your sma to be")
                label.pack(side="top", fill="x", pady=10)
                e = ttk.Entry(midIQ)
                e.insert(0, 10)  # sets a default entry value
                e.pack()
                e.focus_set()

                def callback():
                    global middleIndicators
                    global DatCounter
                    middleIndicators = []  # so, if middleIndicator is none
                    periods = (e.get())
                    group = []
                    group.append("sma")
                    group.append(int(periods))
                    middleIndicators.append(group)
                    DatCounter = 9000
                    print("middle indicator set to: ", middleIndicators)
                    midIQ.destroy()

                b = ttk.Button(midIQ, text="Submit", width=10, command=callback)
                b.pack()
                tk.mainloop()


            if what =="ema":
                midIQ = tk.Tk()
                midIQ.wm_title("Periods")
                label = ttk.Label(midIQ, text="Choose how many periods you want your sma to be")
                label.pack(side="top", fill="x", pady=10)
                e = ttk.Entry(midIQ)
                e.insert(0, 10)  # sets a default entry value
                e.pack()
                e.focus_set()

                def callback():
                    global middleIndicators
                    global DatCounter
                    middleIndicators = []  # so, if middleIndicator is none
                    periods = (e.get())
                    group = []
                    group.append("ema")
                    group.append(int(periods))
                    middleIndicators.append(group)
                    DatCounter = 9000
                    print("middle indicator set to: ", middleIndicators)
                    midIQ.destroy()

                b = ttk.Button(midIQ, text="Submit", width=10, command=callback)
                b.pack()
                tk.mainloop()


        else:
            if what == "sma":
                midIQ = tk.Tk()
                midIQ.wm_title("Periods?")
                label = ttk.Label(midIQ, text="Choose how many periods you want your sma to be")
                label.pack(side="top", fill="x", pady=10)
                e = ttk.Entry(midIQ)
                e.insert(0, 10)  # sets a default entry value
                e.pack()
                e.focus_set()

                def callback():
                    global middleIndicators
                    global DatCounter
                    periods = (e.get())
                    group = []
                    group.append("sma")
                    group.append(int(periods))
                    middleIndicators.append(group)
                    DatCounter = 9000
                    print("middle indicator set to: ", middleIndicators)
                    midIQ.destroy()

                b = ttk.Button(midIQ, text="Submit", width=10, command=callback)
                b.pack()
                tk.mainloop()


            if what == "ema":
                midIQ = tk.Tk()
                midIQ.wm_title("Periods?")
                label = ttk.Label(midIQ, text="Choose how many periods you want your EMA to be")
                label.pack(side="top", fill="x", pady=10)
                e = ttk.Entry(midIQ)
                e.insert(0, 10)  # sets a default entry value
                e.pack()
                e.focus_set()

                def callback():
                    global middleIndicators
                    global DatCounter
                    periods = (e.get())
                    group = []
                    group.append("ema")
                    group.append(int(periods))
                    middleIndicators.append(group)
                    DatCounter = 9000
                    print("middle indicator set to: ", middleIndicators)
                    midIQ.destroy()

                b = ttk.Button(midIQ, text="Submit", width=10, command=callback)
                b.pack()
                tk.mainloop()

    else:
        middleIndicators = "none"





def addTopIndicator(what):
    global topIndicator
    global DatCounter  # so, update "right now!"

    if DataPace == "tick":
        popupmsg("Indicators in Tick Data not available.")

    elif what == "none":
        topIndicator = what
        DatCounter = 9000

    elif what == "rsi":
        rsiQ = tk.Tk()
        rsiQ.wm_title("Periods?")
        label =  ttk.Label(rsiQ, text="Choose how many periods you want rsi to consider")
        label.pack(side="top", fill="x", pady=10)

        e = ttk.Entry(rsiQ)
        e.insert(0, 4)
        e.pack()
        e.focus_set()

        def callback():
            global topIndicator
            global DatCounter
            periods = (e.get())
            group = []
            group.append("rsi")
            group.append(periods)
            topIndicator = group
            DatCounter = 9000
            print("Set top indicator to ", group)
            rsiQ.destroy()  # destros window when done

        b = ttk.Button(rsiQ, text="Submit", width=10, command=callback)
        b.pack()
        tk.mainloop()  # this is for rsi because it has parameters to set

    elif what == "macd":
        global addTopIndicator
        global DatCounter
        topIndicator = "macd"
        DatCounter = 9000


def addBottomIndicator(what):
    global bottomIndicator
    global DatCounter  # so, update "right now!"

    if DataPace == "tick":
        popupmsg("Indicators in Tick Data not available.")

    elif what == "none":
        bottomIndicator = what
        DatCounter = 9000

    elif what == "rsi":
        rsiQ = tk.Tk()
        rsiQ.wm_title("Periods?")
        label =  ttk.Label(rsiQ, text="Choose how many periods you want rsi to consider")
        label.pack(side="top", fill="x", pady=10)

        e = ttk.Entry(rsiQ)
        e.insert(0, 4)
        e.pack()
        e.focus_set()

        def callback():
            global bottomIndicator
            global DatCounter

            periods = (e.get())
            group = []
            group.append("rsi")
            group.append(periods)

            bottomIndicator = group
            DatCounter = 9000
            print("Set bottom indicator to ", group)
            rsiQ.destroy()  # destros window when done

        b = ttk.Button(rsiQ, text="Submit", width=10, command=callback)
        b.pack()
        tk.mainloop()  # this is for rsi because it has parameters to set

    elif what == "macd":
        global addBottomIndicator
        global DatCounter
        bottomIndicator = "macd"
        DatCounter = 9000


def changeExchange(toWhat,pn):  # to what exchange
    global exchange  # globals are constants that can be modified
    global datCounter
    global programName

    exchange = toWhat
    programName = pn
    DatCounter = 9000

def changeTimeFrame(tf):
    global DataPace
    global DatCounter
    if tf == "7d" and resampleSize == "1Min":
        popupmsg("too much data. Choose a smaller time frame, or higher OHLC sample interval")

    else:
        DataPace = tf
        DatCounter = 9000

def changeSampleSize(size, width): # candlestick dimensions
    global resampleSize
    global DatCounter
    global candlewidth
    if DataPace == "7d" and resampleSize == "1Min":
        popupmsg("too much data. Choose a smaller time frame, or higher OHLC sample interval")
    elif DataPace == "tick":
        popupmsg("You're currently viewing tick data, not OHLC.")
    else:
        resampleSize = size
        DatCounter = 9000
        candleWidth = width

def popupmsg(msg):
    popup = tk.Tk()
    popup.wm_title=("!")
    label = ttk.Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Okay", command=popup.destroy)
    B1.pack()
    popup.mainloop()



def animate(i):
    global refreshRate
    global DatCounter
    global dataLink

    if chartLoad:
        if paneCount ==1:
            if DataPace == "tick":
                try:
                    if exchange == "BTC-e":
                        a = plt.subplot2grid((6, 4), (0,0), rowspan = 5, colspan = 4)
    #  full 6x4 grid specified by the tuple parameter
    #  (0, 0) starting point top left corner specified by the next tuple

                        a2 = plt.subplot2grid((6, 4), (5,0), rowspan = 1, colspan = 4, sharex = a)
    # the last parameter means that this function shares the x axis with a
    # both subplots zoom tohether if you zoom in/out on one of them

                        dataLink = 'https://btc-e.com/api/3/trades/btc_usd?limit=2000'
                        data = urllib.request.urlopen(dataLink)
                        data = data.read().decode("utf-8")
                        data = json.loads(data)
                        data = data["btc_usd"]
                        data = pd.DataFrame(data)

                        #print(data['type'])

                        data["datestamp"] = np.array(data['timestamp']).astype("datetime64[s]")
                        allDates = data["datestamp"].tolist()

    # tolist because we cannot pass a numpy array through here

                        buys = data[(data['type']=="bid")]
                        #  buys["datestamp"] = np.array(buys["timestamp"]).astype("datetime64[s]")
                        buyDates = (buys["datestamp"]).tolist()



                        sells = data[(data['type']=="ask")]
                        #  sells["datestamp"] = np.array(sells["timestamp"]).astype("datetime64[s]")
                        sellDates = (sells["datestamp"]).tolist()

                        volume = data["amount"] # from the json data
    # specified in the amount field of the JSON datatype we receive
                        a.clear()

                        a.plot_date(buyDates, buys["price"], lightColor, label="buys")
                        a.plot_date(sellDates, sells["price"], darkColor, label="sells")
                        #a.plot_date(buyDates, buys["price"], "g", label="buys")
                        #a.plot_date(sellDates, sells["price"], "r", label="sells")

                        a2.fill_between(allDates, 0, volume, facecolor =darkColor)

                        a.xaxis.set_major_locator(mticker.MaxNLocator(5))
    # sets the maximum amount of whole dates as marks, less crowded
                        a.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:M:S"))
# removes the top xaxis labe above the vol data as it looks bad, see vid22 3:42
                        plt.setp(a.get_xticklabels(), visible = False)

                        a.legend(bbox_to_anchor=(0, 1.02, 1, .102), loc=3, ncol=2, borderaxespad=0)
                        #a.legend()
                        title = "BTC-E BTC prices \nLastPrice: "+str(data["price"][1999])
                        a.set_title(title)

                    if exchange == "Bitstamp":
                        a = plt.subplot2grid((6, 4), (0,0), rowspan = 5, colspan = 4)
    #  full 6x4 grid specified by the tuple parameter
    #  (0, 0) starting point top left corner specified by the next tuple

                        a2 = plt.subplot2grid((6, 4), (5,0), rowspan = 1, colspan = 4, sharex = a)
    # the last parameter means that this function shares the x axis with a
    # both subplots zoom tohether if you zoom in/out on one of them

                        dataLink = 'https://www.bitstamp.net/api/transactions/'
                        data = urllib.request.urlopen(dataLink)
                        data = data.read().decode("utf-8")
                        data = json.loads(data)
                        data = pd.DataFrame(data)
                        #print(data)
                        #print(data['type'])
                        data["datestamp"] = np.array(data['date'].apply(int)).astype('datetime64[s]')
                        #data["datestamp"] = np.array(data['date']).astype("datetime64[s]")
                        dateStamps = data["datestamp"].tolist()
                        #allDates = data["datestamp"].tolist()
    # tolist because we cannot pass a numpy array through here

                        # buys = data[(data['type']=="bid")]
                        # #  buys["datestamp"] = np.array(buys["timestamp"]).astype("datetime64[s]")
                        # buyDates = (buys["datestamp"]).tolist()


                        # sells = data[(data['type']=="ask")]
                        # #  sells["datestamp"] = np.array(sells["timestamp"]).astype("datetime64[s]")
                        # sellDates = (sells["datestamp"]).tolist()

                        volume = data["amount"].apply(float).tolist() # from the json data
    # specified in the amount field of the JSON datatype we receive
                        a.clear()

                        a.plot_date(dateStamps, data["price"], lightColor, label="buys")

                        #a.plot_date(buyDates, data["price"], "g", label="buys")
                        #a.plot_date(sellDates, sells["price"], "r", label="sells")

                        a2.fill_between(dateStamps, 0, volume, facecolor =darkColor)

                        a.xaxis.set_major_locator(mticker.MaxNLocator(5))
    # sets the maximum amount of whole dates as marks, less crowded
                        a.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:M:S"))
    # removes the top xaxis labe above the vol data as it looks bad, see vid22 3:42
                        plt.setp(a.get_xticklabels(), visible = False)

                        a.legend(bbox_to_anchor=(0, 1.02, 1, .102), loc=3, ncol=2, borderaxespad=0)
                        #a.legend()
                        title = "Bitstamp BTC prices \nLastPrice: "+str(data["price"][0])
                        a.set_title(title)


                    if exchange == "Bitfinex":
                        a = plt.subplot2grid((6, 4), (0,0), rowspan = 5, colspan = 4)
    #  full 6x4 grid specified by the tuple parameter
    #  (0, 0) starting point top left corner specified by the next tuple

                        a2 = plt.subplot2grid((6, 4), (5,0), rowspan = 1, colspan = 4, sharex = a)
    # the last parameter means that this function shares the x axis with a
    # both subplots zoom tohether if you zoom in/out on one of them
                        dataLink = 'https://api.bitfinex.com/v1/trades/btcusd?limit=2000'
                        data = urllib.request.urlopen(dataLink)
                        data = data.read().decode("utf-8")
                        data = json.loads(data)
                        data = pd.DataFrame(data)
                        #print(data)
                        print(data['type'])


                        data["datestamp"] = np.array(data['timestamp']).astype("datetime64[s]")
                        allDates = data["datestamp"].tolist()
    # tolist because we cannot pass a numpy array through here

                        buys = data[(data['type']=="buy")]
                        #  buys["datestamp"] = np.array(buys["timestamp"]).astype("datetime64[s]")
                        buyDates = (buys["datestamp"]).tolist()


                        sells = data[(data['type']=="sell")]
                        #  sells["datestamp"] = np.array(sells["timestamp"]).astype("datetime64[s]")
                        sellDates = (sells["datestamp"]).tolist()

                        volume = data["amount"].apply(float).tolist() # from the json data
    # specified in the amount field of the JSON datatype we receive
                        a.clear()

                        a.plot_date(buyDates, buys["price"], lightColor, label="buys")
                        a.plot_date(sellDates, sells["price"], darkColor, label="sells")
                        #a.plot_date(buyDates, buys["price"], "g", label="buys")
                        #a.plot_date(sellDates, sells["price"], "r", label="sells")

                        a2.fill_between(allDates, 0, volume, facecolor =darkColor)

                        a.xaxis.set_major_locator(mticker.MaxNLocator(5))
    # sets the maximum amount of whole dates as marks, less crowded
                        a.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:M:S"))
    # removes the top xaxis labe above the vol data as it looks bad, see vid22 3:42
                        plt.setp(a.get_xticklabels(), visible = False)

                        a.legend(bbox_to_anchor=(0, 1.02, 1, .102), loc=3, ncol=2, borderaxespad=0)
                        #a.legend()
                        title = "Bitfinex \nLastPrice: "+str(data["price"][0])
                        a.set_title(title)

                    if exchange == 'Huobi':
                        a = plt.subplot2grid((6, 4), (0,0), rowspan = 5, colspan = 4)

                        urlToVisit = 'http://api.huobi.com/staticmarket/depth_btc_150.js'
                        sourceCode = urllib.request.urlopen(urlToVisit)
                        sourceCode = sourceCode.read().decode("utf-8")
                        sourceCode = json.loads(sourceCode)



                        #tmStp = (sourceCode['ts'])
                        # nb Linux timestamp 13 digit int
                        # nb their clock is out so will need weighting here
                        #tmStp = time.strftime("%a %d %b %Y %H:%M:%S GMT", time.gmtime(tmStp / 1000.0))

                        #for key in sourceCode.keys():  #nb sourceCode is dict
                        #val = sourceCode[key]
                        #print("Key", key, 'points to', val)
                        # using a list means we can access a the list with an array index
                        myItems = sourceCode.items()  # a dict of lists
                        myList = list(myItems)  # convert to a list of lists

                        for x in sourceCode.items():
                                key = x[0]
                                val = x[1]
                                if x[0] == 'asks':
                                    myAskList = (val)  # gets out the asks[price, amount] data
                                        #print(myNextList)

                        for y in myAskList:
                                key = y[0]
                                val = y[1]
                                askP = np.array([0])
                                print(y[0], y[1])  # the BTC price in CNY, the amount of BTC
                                tmStp = (sourceCode['ts'])

                                tmStp = time.strftime("%a %d %b %Y %H:%M:%S GMT", time.gmtime(tmStp / 1000.0))
# nb can't use np.datetime64 here as this only works with strings in ISO 8601 date or datetime format
# the to_datetime function in pandas seems to be more flexible:
                                tmStp2 = pd.to_datetime([tmStp])
                                tmStp2 = tmStp2[0]
                                print(tmStp2)
                                a.clear()
                                a.plot_date(tmStp2, askP, darkColor, label="sells")
                                a.xaxis.set_major_locator(mticker.MaxNLocator(5))
                                a.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:M:S"))
                                # removes the top xaxis labe above the vol data as it looks bad, see vid22 3:42
                                plt.setp(a.get_xticklabels(), visible = False)




                    # if exchange == 'Huobi':
                    #     try:
                    #         a = plt.subplot2grid((6,4), (0,0), rowspan=6, colspan=4)

                    #         data = urllib.request.urlopen('http://seaofbtc.com/api/basic/price?key=1&tf=1d&exchange='+programName).read()

                    #         data = str(data).replace('b','').replace("'",'')
                    #         data = json.loads(data)



                    #         dateStamp = np.array(data[0]).astype('datetime64[s]')
                    #         dateStamp = dateStamp.tolist()

                    #         df = pd.DataFrame({'Datetime':dateStamp})




                    #         df['Price'] = data[1]

                    #         df['Volume'] = data[2]
                    #         df['Symbol'] = "BTCUSD"
                    #         df['MPLDate'] = df['Datetime'].apply(lambda date: mdates.date2num(date.to_pydatetime()))
                    #         df = df.set_index('Datetime')
                    #         lastPrice = df['Price'][-1]

                    #         a.plot_date(df['MPLDate'][-4500:],df['Price'][-4500:], lightColor, label ="price")

                    #         a.xaxis.set_major_locator(mticker.MaxNLocator(5))
                    #         a.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))


                    #         title = exchange+' Tick Data\nLast Price: '+str(lastPrice)
                    #         a.set_title(title)
                    #         priceData = df['Price'].apply(float).tolist()
                    #     except Exception as e:
                    #         print(str(e))







    #                 if exchange == "Huobi":
    #                     a = plt.subplot2grid((6, 4), (0,0), rowspan = 6, colspan = 4)
    # #  full 6x4 grid specified by the tuple parameter
    # #  (0, 0) starting point top left corner specified by the next tuple

    #                     #datalink = 'https://market.huobi.com/staticmarket/ticker_btc_json.js'
    #                     dataLink = 'http://api.huobi.com/staticmarket/ticker_btc_json.js'
    # #{"Ticker": {"high": 86.48, "low": 79.75, "last": 83.9, "vol": 2239560.1752883, "buy": 83.88, "sell": 83.9}}
    #                     data = urllib.request.urlopen(dataLink)
    #                     data = data.read().decode("utf-8")
    #                     data = json.loads(data)
    #                     print(data)
    #                     #print(type(data['time']))  # is class str

    #                     #print(data['ticker']['buy'])
    #                     #print(data['ticker']['symbol'])

    #                     #from datetime import datetime at top of file
    #                     # time = data['time']
    #                     # ftime = float(time)
    #                     # ftime=np.array(ftime)
    #                     # print("datestamp as numpy array", datetime.fromtimestamp(ftime))
    #                     # datestamp = datetime.fromtimestamp(ftime)
    #                     # print(datestamp)

    #                     # time = data['time']
    #                     # time = int(time)
    #                     # time=np.array(time).tolist()
    #                     # print("datestamp as numpy array", datetime.fromtimestamp(time))
    #                     # datestamp = datetime.fromtimestamp(time)
    #                     # print(datestamp)

    #                     buys = data['ticker']['buy']
    #                     sells = data['ticker']['sell']
    #                     data = pd.DataFrame(data)
    #                     buys["datestamp"] = np.array(buys).astype("datetime64[s]")

    #                     # buys = np.array(buys)
    #                     # sells = np.array(sells)


    #                     # print("buys as numpy array", buys) # float
    #                     # print("sells as numpy array", sells) # float

    #                     # a.clear()
    #                     # a.plot_date(buys, time)
    #                     # a.plot_date(sells, time)

#                     if exchange == "Huobi":
#                         from sys import exit
#                         #a = plt.subplot2grid((6, 4), (0,0), rowspan = 6, colspan = 4)

#                         '''
# idiosyncratic shit related to huobi
# http://www.wildbunny.co.uk/blog/2014/06/11/algorithmic-trading-with-bitcoin-part-1/


#                         dataLink = 'http://api.huobi.com/staticmarket/ticker_btc_json.js'
#                         data = urllib.request.urlopen(dataLink)
#                         data = data.read().decode("utf-8")
#                         data = json.loads(data)
#                         data = [data]  # data is a list of dictionaries

#                         print(data, '\n')  # print it out

#                         for item in data:  # get each dictionary from the list of two dictionaries that is data
#                             for k, v in item.items(): # get the key value pairs i.e., the two dictionaries
#                                 if k == 'ticker':  # work on the 'ticker dictionary'
#                                     #print(v)  # prints all 8 items in the ticker dictionary
#                                     openp = v['open']
#                                     lastp = v['last']
#                                     highp = v['high']
#                                     lowp = v['low']
#                                     buyp = ['buy']
#                                     sellp = v['sell']
#                                     volume = v['vol']
#                                     symbol = v['symbol']
#                                     print('opening price:', openp)

#                         for item in data:  # get each dictionary from the list of two dictionaries that is data
#                             for k, v in item.items(): # get the key value pairs i.e., the two dictionaries
#                                 if k == 'time':
#                                     timestamp = v # print the single item in the time dictionary
#                                     print('Unix timestamp:', timestamp)

#                         exchangeFile = exchange+'.txt'
#                         print('Creating',exchangeFile)

#                         def pullData(exchange):
#                             try:
#                                 urlToVisit = 'http://api.huobi.com/staticmarket/btc_kline_200_json.js'
#                                 sourceCode = urllib.request.urlopen(urlToVisit)
#                                 sourceCode = sourceCode.read().decode("utf-8")
#                                 sourceCode = json.loads(sourceCode)
#                                 print(sourceCode[0][:])
#                                 # ['20170407170000000', 7091.87, 7110.0, 7091.87, 7093.88, 3.2892]
#                                 # Date and time, opening price, the highest price, the lowest price, closing price, volume
#                                 timeStmp = (sourceCode[0][0]) # the first element in the list is a unix timestamp
#                                 timeStmp = timeStmp[:11]  # shorten it to a range that dateutils parser can use
#                                 timeStmp = parse(timestamp)  # this is a'datetime.datetime' object
#                                 timeStmp = timeStmp.strftime("%Y-%m-%d %H:%M:%S") # convert to a string thus can be saved to file
#                                 saveFile = open(exchangeFile,'a')
#                                 lineToWrite = timeStmp+','+'cost'+'\n'
#                                 saveFile.write(lineToWrite)
#                                 saveFile.close()

#                             except Exception as e:
#                                 print("Failed because of: ", e)


#                         #import datetime as dt at top of file
#                         # dt is module name, datetime is the class, fromtimestamp() is the method
#                         timestamp = dt.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')
#                         print(timestamp)

#                         pullData(exchange)

#                         #timestamp, openp, lastp, highp, lowp, buyp, sellp, volume, symbol = np.loadtxt(exchangeFile,delimiter=',',unpack=True)

#                         #exit()
# ####################################################################
# '''
# #  {"id":1491662772566,"ts":1491662772566,"bids":[[7110.000000,1.000000]],"asks":[[7124.310000,0.010000]],"symbol":"btccny"}
#                         def depthData():
#                             try:
#                                 urlToVisit = 'http://api.huobi.com/staticmarket/depth_btc_150.js'
#                                 sourceCode = urllib.request.urlopen(urlToVisit)
#                                 sourceCode = sourceCode.read().decode("utf-8")
#                                 sourceCode = json.loads(sourceCode)



#                                 #tmStp = (sourceCode['ts'])

#                                 # nb Linux timestamp 13 digit int
#                                 # nb their clock is out so will need weighting here
#                                 #tmStp = time.strftime("%a %d %b %Y %H:%M:%S GMT", time.gmtime(tmStp / 1000.0))

#                                 #for key in sourceCode.keys():  #nb sourceCode is dict
#                                     #val = sourceCode[key]
#                                     #print("Key", key, 'points to', val)

#                                 # using a list means we can access a the list with an array index
#                                 myItems = sourceCode.items()  # a dict of lists
#                                 myList = list(myItems)  # convert to a list of lists

#                                 for x in sourceCode.items():
#                                         key = x[0]
#                                         val = x[1]
#                                         if x[0] == 'asks':
#                                             myAskList = (val)  # gets out the asks[price, amount] data
#                                             #print(myNextList)

#                                 for y in myAskList:
#                                         key = y[0]
#                                         val = y[1]
#                                         askP = np.array([0])
#                                         print(y[0], y[1])  # the BTC price in CNY, the amount of BTC
#                                         tmStp = (sourceCode['ts'])

#                                         tmStp = time.strftime("%a %d %b %Y %H:%M:%S GMT", time.gmtime(tmStp / 1000.0))
# # nb can't use np.datetime64 here as this only works with strings in ISO 8601 date or datetime format
# # the to_datetime function in pandas seems to be more flexible:
#                                         tmStp2 = pd.to_datetime([tmStp])
#                                         tmStp2 = tmStp2[0]
#                                         print(tmStp2)
#                                         a.clear()
#                                         a.scatter(tmStp2, askP)

#                                         a.plot(tmStp2, askP)
#                                         a.show()





#                                 #print(myList[0][0])
#                                 #print(myList[0][1])
#                                 #print(myList[0][2])
#                                 #print(myList[0][3])
#                                 #print(myList[0][4])
#                                 #print(myList[0][5])
#                                 #print(myList[0][6])
#                                 #print(myList[0][7])
#                                 #print(myList[0][8])


#                                 for k, v in sourceCode.items():
#                                     #print(k, 'corresponds to', v)
#                                     if k == 'bids':
#                                         print('Someone bid', v[0][1], 'BTC at', v[0][0], 'CNY on', tmStp)
#                                         #print(sourceCode['ts'])

#                                 for k, v in sourceCode.items():
#                                     if k == 'ask':
#                                         print('Someone asked', v[0][1], 'BTC at', v[0][0], 'CNY on', tmStp)



# # https://github.com/huobiapi/API_Docs_en/wiki/REST-Candlestick-Chart




# # {'asks': [[7122.33, 0.03]], 'symbol': 'btccny', 'bids': [[7110.59, 0.01]], 'ts': 1491663633620, 'id': 1491663633620}

#                             except Exception as e:
#                                 print("Failed because of: ", e)

#                         depthData()



                except Exception as e:
                    print("Failed because of: ", e)

#  []: Used to define mutable data types - lists, list comprehensions and for indexing/lookup/slicing.
   #  (): Define tuples, order of operations, generator expressions, function calls and other syntax.
   #  {}: The two hash table types - dictionaries and sets.

  # [{'time': '1491589759', 'ticker': {'last': 7157.35, 'vol': 6019.5942, 'low': 7050.0, 'symbol': 'btccny', 'buy': 7128.68, 'sell': 7140.51, 'open': 7099.53, 'high': 7300.0}}]

  # dictionary key, value pairs are separated with commas.

  # The key & value pairs are listed between curly brackets " { } "

  # We query the dictionary using square brackets " [ ] "

  # Huobi Market Data api (google translate) https://translate.googleusercontent.com/translate_c?act=url&depth=1&hl=en&ie=UTF8&prev=_t&rurl=translate.google.com&sl=auto&tl=en&u=http://www.huobi.com/help/index.php%3Fa%3Dmarket_help&usg=ALkJrhiklnKqkg1JZM-VE37fNP7csWAEww







class EpistimiZer(tk.Tk): # parenthesis => inheritence so local class inherits tkinter
# constructor initialises tkinter. Takes any no of args, kwargs are dictionaries
    def __init__(self, *args, **kwargs):  # kwargs are keyword arguments
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "EpistimiZer Client")
        container = tk.Frame(self) # contains everything in the app

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1) # 0 is min size, priority 1
        container.grid_columnconfigure(0, weight=1)

        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Save settings", command = lambda: popupmsg("in development..."))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=quit)
        menubar.add_cascade(label="File", menu=filemenu)

        exchangeChoice = tk.Menu(menubar, tearoff=1)
        exchangeChoice.add_command(label="BTC-e", command=lambda: changeExchange("BTC-e","btce"))

        exchangeChoice.add_command(label="Bitfinex", command=lambda: changeExchange("Bitfinex","bitfinex"))

        exchangeChoice.add_command(label="Bitstamp", command=lambda: changeExchange("Bitstamp","bitstamp"))

        exchangeChoice.add_command(label="Huobi", command=lambda: changeExchange("Huobi","huobi"))

        menubar.add_cascade(label="Exchange", menu=exchangeChoice)

        dataTF = tk.Menu(menubar, tearoff=1)
        dataTF.add_command(label="Tick", command = lambda: changeTimeFrame('tick'))
        dataTF.add_command(label="1 Day", command = lambda: changeTimeFrame('1d'))
        dataTF.add_command(label="3 day", command = lambda: changeTimeFrame('3d'))
        dataTF.add_command(label="1 week", command = lambda: changeTimeFrame('7d'))
        menubar.add_cascade(label = "Dataq Time Frame", menu = dataTF)

        OHLCI = tk.Menu(menubar, tearoff=1)
        OHLCI.add_command(label="Tick", command = lambda: changeTimeFrame('tick'))
        OHLCI.add_command(label="1 minute", command = lambda: changeSampleSize('1Min', 0.0005)) # 2nd parameter is the candle width
        OHLCI.add_command(label="5 minute", command = lambda: changeSampleSize('5Min', 0.003))
        OHLCI.add_command(label="15 minute", command = lambda: changeSampleSize('15Min', 0.008))
        OHLCI.add_command(label="30 minute", command = lambda: changeSampleSize('30Min', 0.016))
        OHLCI.add_command(label="1 hour", command = lambda: changeSampleSize('1H', 0.032))
        OHLCI.add_command(label="3 hour", command = lambda: changeSampleSize('3H', 0.096))
        menubar.add_cascade(label="OHLC Interval", menu=OHLCI)

        topIndi = tk.Menu(menubar, tearoff=1)
        topIndi.add_command(label="None", command = lambda: addTopIndicator('none'))
        topIndi.add_command(label="RSI", command = lambda: addTopIndicator('rsi'))
        topIndi.add_command(label="MACD", command = lambda: addTopIndicator('macd'))
        menubar.add_cascade(label="Top Indicator", menu=topIndi)

        mainI = tk.Menu(menubar, tearoff=1)
        mainI.add_command(label="None", command = lambda: addMiddleIndicator('none'))
        mainI.add_command(label="SMA", command = lambda: addMiddleIndicator('sma'))
        mainI.add_command(label="EMA", command = lambda: addMiddleIndicator('ema'))
        menubar.add_cascade(label="Main/middle Indicator", menu=mainI)

        bottomI = tk.Menu(menubar, tearoff=1)
        bottomI.add_command(label="None", command = lambda: addBottomIndicator('none'))
        bottomI.add_command(label="RSI", command = lambda: addBottomIndicator('rsi'))
        bottomI.add_command(label="MACD", command = lambda: addBottomIndicator('macd'))
        menubar.add_cascade(label="Bottom Indicator", menu=bottomI)

        tradeButton = tk.Menu(menubar, tearoff=1)
        tradeButton.add_command(label = "Manual Trading", command=lambda: popupmsg("This is not live yet"))
        tradeButton.add_command(label = "Automated Trading", command=lambda: popupmsg("This is not live yet"))
        tradeButton.add_separator()
        tradeButton.add_command(label = "Quick Buy", command=lambda: popupmsg("This is not live yet"))
        tradeButton.add_command(label = "Quick Sell", command=lambda: popupmsg("This is not live yet"))
        tradeButton.add_separator()
        tradeButton.add_command(label = "Set-up Quick Buy/Sell", command=lambda: popupmsg("This is not live yet"))

        menubar.add_cascade(label="Trading",menu=tradeButton)

        startStop = tk.Menu(menubar, tearoff = 1)
        startStop.add_command(label="Resume", command = lambda: loadChart('start'))
        startStop.add_command(label="Pause", command = lambda: loadChart('stop'))
        menubar.add_cascade(label = "Resume/Pause client", menu = startStop)

        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Tutorial", command=tutorial)

        menubar.add_cascade(label="Help", menu=helpmenu)







        tk.Tk.config(self, menu=menubar)

        # STUFF NEW PAGES IN HERE #
        self.frames = {} # dictionary of values used by cont (the key)

        #  for F in (StartPage, PageOne, PageTwo, PageThree):
        for F in (StartPage, BTCe_Page):
            frame = F(container, self) # initialise frame & save to frames in line below
            self.frames[F] = frame # assign the start page to the frames dictionary
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage) #  initialising - show the start page

    def show_frame(self, cont): # later, the cont parameter is a key that determines which frame is shown
        frame = self.frames[cont] # pass the key in
        frame.tkraise() # show the corresponding frame


# CLONE THIS TO MAKE NEW PAGES #
class StartPage(tk.Frame):
    def __init__(self, parent, controller):  # define the method
        tk.Frame.__init__(self,parent)  # initialise the page
        label = tk.Label(self, text="ALPHA Bitcoin trading application", font=LARGE_FONT)  # initialise label object
        label.pack(pady=10, padx=10)  # pack object
        button1 = ttk.Button(self, text="Agree", command=lambda: controller.show_frame(BTCe_Page))
        button1.pack()
        button2 = ttk.Button(self, text="Disagree", command=quit)
        button2.pack()
        # button3 = ttk.Button(self, text="Graph page ", command=lambda: controller.show_frame(PageThree))
        # button3.pack()
'''
Don't try coding command = whatever as this shows up
immediately & then does absolutely nothing. Using lambda creates a
function that isn't actually used until it is called when the button
IS ACTUALLY PRESSED  thus avoiding this issue. This allows you to pass
a parameter through the command eg a call to another method'''

class PageOne(tk.Frame):
    def __init__(self, parent, controller):  # define the method
        tk.Frame.__init__(self,parent)  # initialise the page
        label = tk.Label(self, text="Page One", font=LARGE_FONT)
        label.pack(pady=10, padx=10)  # pack object
        button1 = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage))
        button1.pack()
        # button2 = ttk.Button(self, text="Page Two", command=lambda: controller.show_frame(PageTwo))
        # button2.pack()


# class PageTwo(tk.Frame):
#     def __init__(self, parent, controller):  # define the method
#         tk.Frame.__init__(self,parent)  # initialise the page
#         label = tk.Label(self, text="Page Two", font=LARGE_FONT)
#         label.pack(pady=10, padx=10)  # pack object
#         button2 = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage))
#         button2.pack()

class BTCe_Page(tk.Frame):
    def __init__(self, parent, controller):  # define the method
        tk.Frame.__init__(self,parent)  # initialise the page
        label = tk.Label(self, text="Graph Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)  # pack object
        button1 = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage))
        button1.pack()

        # f = Figure(figsize=(5,5), dpi=100)
        # a = f.add_subplot(111)
        # a.plot([1,2,3,4,5,6,7,8], [1,4,9,16,25,36,49,64])





        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand = True)

        toolbar= NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand = True)


app = EpistimiZer()  # assign the EpistimiZer object which is inherited ftom tk
app.geometry("1280x720")
''' send to f for figure (top of this file), interval = time between
running this function in millisecs '''
ani = animation.FuncAnimation(f, animate, interval=5000)

app.mainloop()  # works because mainloop is an inherited method of tk as well

