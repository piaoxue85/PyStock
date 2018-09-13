import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from numpy import *
import math
import copy
import csv
import sharedfunctions as fn

#B-BAND AND RSI DIVERGENCE

from collections import OrderedDict

def apply(data,row, day=9, th1=30, th2=70):

    headers = data[0]
    
    col = headers.index("RSI" + str(day))
    rsi3 = data[row-2][col]
    rsi2 = data[row-1][col]
    rsi1 = data[row][col]

    col = headers.index("RSI"+ str(day) +"CHG")
    rsi1chg = data[row][col]

    col = headers.index("HRSI" + str(day))
    hrsi1 = data[row][col]

    col = headers.index("HRSI" + str(day) + "CHG")
    hrsi1chg = data[row][col]    

    col = headers.index("LRSI" + str(day))
    lrsi1 = data[row][col]

    col = headers.index("LRSI" + str(day) + "CHG")
    lrsi1chg = data[row][col]

    signal = ""
    comment = ""

    if rsi2 <= th1 and hrsi1 >= th1 and hrsi1chg > 1:
        signal = "ATTNBUY"
        comment = "DAY HIGH PIVOT - RSI" + str(day) + " - " + str(hrsi1)
    
    if rsi2 <= th1 and rsi1chg > 1:
        signal = "BUY"
        comment = "OVERSOLD PIVOT - RSI" + str(day) + " - " + str(rsi1) 

    if rsi2 >= th2 and rsi1chg < 1:
        signal = "SELL"
        comment = "OVERBOUGHT PIVOT - RSI" + str(day) + " - " + str(rsi1)   

    if rsi2 >= th2 and lrsi1 >= th2 and lrsi1chg < 1:
        signal = "ATTNSELL"
        comment = "DAY LOW PIVOT - RSI" + str(day) + " - " + str(lrsi1)
		
    return signal, comment


