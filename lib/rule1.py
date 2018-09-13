import matplotlib.pyplot as plt

import math
import copy
import csv
import sharedfunctions as fn

#B-BAND AND RSI DIVERGENCE

from collections import OrderedDict

def apply(data,row):

    headers = data[0]

    col = headers.index("B-BAND20")
    bb3 = data[row-2][col]        
    bb2 = data[row-1][col]    
    bb1 = data[row][col]
    rsitrend = fn.trend(data,row,col)
    
    col = headers.index("RSI9")
    rsi3 = data[row-2][col]
    rsi2 = data[row-1][col]
    rsi1 = data[row][col]
    bbtrend = fn.trend(data,row,col)

    signal = ""
    comment = ""
    
    #ABOVE UPPER BAND
    if bb1 >= 1:
        if rsitrend == 1:
            signal = "--"
            comment = "B-BAND IS ABOVE THE UPPER BAND [OVERBOUGHT] AND RSI (" + str(round(rsi1,2)) + ") IS MOVING DOWNWARD"
        elif rsitrend ==4:
            signal = "SELL"
            comment = "B-BAND IS ABOVE THE UPPER BAND [OVERBOUGHT] AND RSI (" + str(round(rsi1,2)) + ") IS IN DOWN TREND"
        
    #BELOW LOWER BAND
    elif bb1 <= 0:
        if rsitrend == 2:
            signal = "BUY"
            comment = "B-BAND IS BELOW THE LOWER BAND [OVERSOLD] AND RSI (" + str(round(rsi1,2)) + ") IS MOVING UPWARD"
        elif rsitrend == 3:
            signal = "BUY"
            comment = "B-BAND IS BELOW THE LOWER BAND [OVERSOLD] AND RSI (" + str(round(rsi1,2)) + ") IS IN UP TREND"            

    else:

        if bbtrend != rsitrend:
            #DOWNWARD
            if bbtrend == 1 or bbtrend ==4:
                if rsitrend ==2 or rsitrend ==3:
                    signal = "--"
                    comment = "DIVERGENCE. B-BAND IS GOING DOWNWARD AND RSI (" + str(round(rsi1,2)) + ") IS MOVING UPWARD"
            elif bbtrend == 2 or bbtrend ==3:
                if rsitrend ==1 or rsitrend ==4:
                    signal = "--"
                    comment = "DIVERGENCE. B-BAND IS GOING UPWARD AND RSI (" + str(round(rsi1,2)) + ") IS MOVING DOWNWARD"

    return signal, comment


