import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from numpy import *

import math
import copy

import csv
import pandas

from collections import OrderedDict

def apply(data, smaInterval, idx):

#The moving averages by themselves will give you a great roadmap for trading the markets.  
#But what about moving average crossovers as a trigger for entering and closing trades.  
#Let me take a clear stance on this one and say I'm not a fan for this strategy.  
#First the moving average by itself is a lagging indicator, now you layer in the idea that you have to wait for a lagging indicator to cross another lagging indicator is just too much delay for me.  
#If you look around the web one of the most popular simple moving averages to use with a crossover strategy is the 50 and 200 day.  
#When the 50 simple moving average crosses above the 200 simple moving average it generates a golden cross.  
#Conversely, when the 50 simple moving average crosses beneath the 200 simple moving average it creates a death cross.  
#I only mention this so you are aware of the setup, which maybe applicable for long-term investing.  
#Since Tradingsim focuses on day trading let me at least run through some basic crossover strategies. - 
#See more at: http://tradingsim.com/blog/simple-moving-average/#sthash.2usGAzso.dpuf

#CLOSESMA10CHG
#CLOSESMA5CHG
    headers = data[0]
    
    col = headers.index("SMA" + str(smaInterval))
    sma3 = data[idx-2][col]
    sma2 = data[idx-1][col]
    sma1 = data[idx][col]

    col = headers.index("CLOSE")
    val3 = data[idx-2][col]
    val2 = data[idx-1][col]
    val1 = data[idx][col]

    maxVal = max(sma1, sma2, val1, val2)
    minVal = min(sma1, sma2, val1, val2)

    signal  = ""
    comment = ""

    if minVal == val2 and maxVal == val1:
        signal = 'BUY'
        comment = "PRICE (" + str(round(val1,2)) + ") IS UP CROSSING SMA" + str(smaInterval) + " (" + str(round(sma1,2)) + ")"
 
    elif minVal == val2 and maxVal == val2:
        signal = "SELL"
        comment = "PRICE (" + str(round(val1,2)) + ") IS DOWN CROSSING SMA"+ str(smaInterval) + " (" + str(round(sma1,2)) + ")"

    return signal, comment

