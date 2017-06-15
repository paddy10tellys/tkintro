import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from scipy.signal import argrelextrema
from matplotlib.finance import candlestick_ohlc
import matplotlib.dates as mdates
import matplotlib.animation as animation
import datetime as dt
import urllib
import json
from urllib.request import urlopen
import datetime as dt
import requests
from matplotlib.dates import date2num
from matplotlib import style
style.use('fivethirtyeight')
'''
change plot size by setting the dynamic rc settings of Matplotlib. These
are stored in a dictionary named rcParams with the key figure.figsize
'''
#Get current size
fig_size=plt.rcParams["figure.figsize"]  #  [6.4, 4.8]

#Change size
fig_size[0]=12.4
fig_size[1]=10.8
plt.rcParams["figure.figsize"]=fig_size

fig = plt.figure()
'''  The figure keeps track of all the child Axes, a smattering of ‘special’
 artists (titles, figure legends, etc), and the canvas. (Don’t worry too
 much about the canvas, it is crucial as it is the object that actually
  does the drawing to get you your plot, but as the user it is more-or-less
  invisible to you). A figure can have any number of Axes, but to be useful
   should have at least one.'''

plt.ion()  # interactive mode on
'''when the interactive mode is on, one can do plot() without having to
 do draw(). Use when in a python console, the interactive part is that the
 console does not freeze. Use instead of show(). Its always either show
 or ion not both. I needed it to stop the animate function freezing'''

'''ax1 is an Axes object created in a figure: it's essentially a box with
 coordinates. A figure can thus contain many axes. Axes objects are the
 used for most plotting operations'''
ax1 = plt.subplot2grid((6,1), (0,0), rowspan=6, colspan=1)
'''1st param is a 6x1 grid, 2nd is starting point
see https://pythonprogramming.net/subplot2grid-add_subplot-matplotlib-tutorial/'''

def animate(i):
    dataLink ='http://api.huobi.com/staticmarket/btc_kline_015_json.js?length=150'
    # see https://translate.googleusercontent.com/translate_c?depth=1&hl
    # =en&prev=search&rurl=translate.google.co.uk&sl=zh-
    # CN&sp=nmt4&u=https://github.com/huobiapi/API_Docs/wiki/REST-
    # Interval&usg=ALkJrhi8n3N455w0mLm1r-HWjDuXgNZ2pg
    r = requests.get(dataLink)  # r is a response object.
    quotes = pd.DataFrame.from_records(r.json())  # from_records() fetches dataset
    quotes[0] = pd.to_datetime(quotes[0].str[:-3], format='%Y%m%d%H%M%S')  #  makes timestamp readable by matplotlib
    #print(quotes)

    # year = quotes[0].dt.year.values[0]
    # print(year)

    #Naming columns
    quotes.columns = ["Date","Open","High","Low","Close", "Vol"]

    #Converting dates column to float values
    quotes['Date'] = quotes['Date'].map(mdates.date2num)
    '''The map(aFunction, aSequence) function applies a passed-in function
    to each item in an iterable object and returns a list containing all
     the function call results. More efficient than a for loop'''

    ''' matplotlib datetimes are represented as simple floats. 1 day
    corresponds to a difference of 1.0, and the dates are in days since 1900'''

    #Making plot
    ax1.clear()  # prevent buildup of clutter & loss of RAM
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d-%H:%S'))
    ax1.relim()
    #The data limits are not updated automatically when artist data are changed
    # after the artist has been added to an Axes instance. In that case, use
    # matplotlib.axes.Axes.relim() prior to calling autoscale_view.
    ax1.autoscale_view()  #  scales in relation to period & length parameters of the json feed?
    #fig.autofmt_xdate() # rotates the times, stops x tick labels from squashing together.
    plt.xticks(rotation=30) # does the same as fig.autofmt_xdate() but won't turn off
    # xtick labels on other subplots nb insert after each subplot
    ax1.fmt_xdata = mdates.DateFormatter('%H:%M GMT+8')  # prints the time in hours
    # and minutes in the lower right toolbar on mouseover
    plt.xlabel('15 minute periods')
    plt.ylabel('Price')
    plt.subplots_adjust(left=0.11, right=0.9, top=0.9, bottom=0.2)  # because the sides
    # and bottom spaces were cramping the labels

    #Converts raw mdate numbers to dates
    ax1.xaxis_date()  # sets xaxis to date


    #Making candlestick plot
    candlestick_ohlc(ax1,quotes.values,width=0.004, colorup='g', colordown='k',alpha=0.75)

    #Plotting a line
    # ax1.plot(quotes['Date'], quotes['Open'])
    # ax1.plot(quotes['Date'], quotes['Close'])
    #print(quotes)

    latest=quotes['Close'].tail(n=1)  # pandas.core.series.Series
    latest = latest.iloc[0]  # <class 'numpy.float64'>
    ''' .iloc indexes by integer (from 0 to length-1 of the axis) '''
    last_two=quotes['Close'].tail(n=2)  # pandas.core.series.Series
    last_two=np.array(last_two)  # <class 'numpy.ndarray'>
    print('latest', last_two[1], ' - previous', last_two[0], '=', last_two[1] - last_two[0])
    direction=last_two[1] - last_two[0]
    if direction > 0:
        print('uptrend')
    elif direction == 0:
        print('sidetrend')
    else:
        print('downtrend')



    # plt.axhline(y=latest, linewidth=1, color='black', linestyle = 'dashed')

    sample_min_max = quotes['Close'].values  # converts df to np array

    # # for local maxima indicies
    # max=argrelextrema(sample_min_max, np.greater)[0]

    # # for local minima indicies
    # min=argrelextrema(sample_min_max, np.less)[0]

    # # for the actual values
    # max_vals = sample_min_max[argrelextrema(sample_min_max, np.greater)[0]]
    # min_vals = sample_min_max[argrelextrema(sample_min_max, np.less)[0]]

    # # for the resistance lines
    # max_vals[::-1].sort() #  sorts the array in place in descending order
    # min_vals[::-1].sort() #  sorts the array in place in descending order

    # #for elem in max_vals[:3]:
    # for elem in max_vals[-10:]:
    #     plt.axhline(y=elem, linewidth=1, color='r')

    # if np.diff(min_vals[-4:]).max() >= 0.001:
    #     print('fell more than 0.001')
    #     for elem in max_vals[-4:]:
    #         plt.axhline(y=elem, linewidth=1, color='b')
    # else:
    #     for elem in max_vals[-4:]:
    #         plt.axhline(y=elem, linewidth=1, color='b')

    print(latest)

    def supres(ltp, n):
        """
        This function takes a numpy array of last traded price
        and returns a tuple of support and resistance levels
        respectively. n is the number of entries to be scanned.
        """
        from scipy.signal import savgol_filter as smooth

        #converting n to a nearest even number
        if n%2 != 0:
            n += 1

        n_ltp = ltp.shape[0]  # the array data to be filtered
        #print(n_ltp)  # 150
        #print(type(n_ltp))  # <class 'int'>

        # smoothening the curve
        ltp_s = smooth(ltp, (n+1), 3)
        ''' scipy.signal.savgol_filter(x, window_length, polyorder, deriv=0,
            delta=1.0, axis=-1, mode='interp', cval=0.0)   nb window_length
            must be a positive odd integer nb polyorder is the order of the
            polynomial used to fit the samples eg cubic in this case'''

        # taking a simple derivative
        ltp_d = np.zeros(n_ltp)  # Return a new array filled with zeros
        #print(ltp_d)  # an array of 150 x zeros as floats
        #print(type(ltp_d))  # <class 'numpy.ndarray'>

        ltp_d[1:] = np.subtract(ltp_s[1:], ltp_s[:-1])
        ''' subtract adjacent elements & insert the result in array ltp_d
        of <type 'numpy.ndarray'>  nb these values are floats'''

        resistance = []
        support = []

        for i in range(n_ltp - n):  # 150 - 20
            arr_sl = ltp_d[i:(i+n)] # copy 20 floats from ltp_d to arr_sl
            #print(type(arr_sl))  #  <class 'numpy.ndarray'>
            #print(arr_sl)  # an array of 20 floats
            first = arr_sl[:(int(n/2))] #first half
            #print('initial half',first)
            last = arr_sl[(int(n/2)):] #second half
            #print('last half',last)

            ''' if you don't cast n/2 to an int you get told not to use
            floats to index an array with a VisibleDeprecationWarning: using
            a non-integer number instead of an integer will result in an
            error in the future  '''

            r_1 = np.sum(first > 0) # the number elements in the first half that are more than zero
            r_2 = np.sum(last < 0) # the number of elements in second half that less than zero

            s_1 = np.sum(first < 0) # the number of elements in first half that less than zero
            s_2 = np.sum(last > 0) # the number of elements in second half that are more than zero


            #local maxima detection
            if (r_1 == (n/2)) and (r_2 == (n/2)):
                resistance.append(ltp[i+((int(n/2))-1)])
                #print('resistance at',resistance)
            '''if 50% of the elements in the first half are more than zero and
            50% in the second half are than zero then this is resistance so
            add this closing price to the list of resistance levels '''

            #local minima detection
            if (s_1 == (n/2)) and (s_2 == (n/2)):
                support.append(ltp[i+((int(n/2))-1)])
                #print('support at',support)
            '''if 50% of the elements in the first half are less than zero and
            50% in the second half are more than zero then this is support so
            add this closing price to the list of support levels '''


        return support, resistance

    suggested = supres(sample_min_max, 6)
    for vals in suggested[0]:
        print('support at blue line',vals)
        plt.axhline(y=vals, linewidth=1, color='blue')
    for vals in suggested[1]:
        print('resistance at red line',vals)
        plt.axhline(y=vals, linewidth=1, color='red')
    #print(suggested)
    # plt.axhline(y=suggested[0], linewidth=1, color='blue')
    # plt.axhline(y=suggested[1], linewidth=1, color='red')
    plt.axhline(y=latest, linewidth=1, color='black', linestyle = 'dashed')
    #print(suggested[0])
    #print(suggested[1])


ani = animation.FuncAnimation(fig, animate, interval=5000)
plt.show(block=True)




