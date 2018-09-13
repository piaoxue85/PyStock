import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from numpy import *
import sharedfunctions as fn
import math
import copy

from collections import OrderedDict

def apply(data, idx):

    headers = data[0]
    col = headers.index("HIGH")
    high3 = data[idx-2][col]
    high2 = data[idx-1][col]
    high1 = data[idx][col]
    hightrend = fn.trend(data,idx,col)
    
    col = headers.index("LOW")
    low3 = data[idx-2][col]
    low2 = data[idx-1][col]
    low1 = data[idx][col]
    lowtrend = fn.trend(data,idx,col)

    signal = ""
    comment = ""
    
    if lowtrend == 1:
        signal = "--"
        comment = "DAY LOW (" +  str(round(low1,2)) +") IS LOWER THAN YESTERDAY LOW (" + str(round(low2,2)) + ") LOOK FOR SELL SIGNAL"
    elif lowtrend == 2:
        signal = "--"
        comment = "DAY LOW (" +  str(round(low1,2)) +") IS HIGHER THAN YESTERDAY LOW (" + str(round(low2,2)) + ") LOOK FOR BUY SIGNAL" 
    elif lowtrend == 3:
        signal = "--"
        comment = "DAY LOW (" +  str(round(low1,2)) +") IS 3 DAYS HIGHEST."
    elif lowtrend == 4:
        signal = "--"
        comment = "DAY LOW (" +  str(round(low1,2)) +") IS 3 DAYS LOWEST."  
    elif hightrend == 5:
        if high1 <> high2:
            signal = "--"
            comment = "DAY LOWS STOPPED AT (" +  str(round(low1,2)) +"). LOOK FOR BUY SIGNAL"


    return signal, comment

