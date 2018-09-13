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

    col = headers.index("HIGHLOWCHG")
    highlow3 = (high3 - low3) / low3
    highlow2 = (high2 - low2) / low2
    highlow1 = (high1 - low1) / low1
    highlowtrend = fn.trend(data,idx,col)

    signal = ""
    comment = ""

    if highlowtrend == 2 or highlowtrend == 3:
        signal = "--"
        comment = "THE HIGH/LOW VOLATILITY (" + str(round(highlow1,4)*100)+ "%) IS INCREASING. "
    elif highlowtrend == 1 or highlowtrend == 4:
        signal = "--"
        comment = "THE HIGH/LOW VOLATILITY (" + str(round(highlow1,4)*100) + "%) IS DECREASING. CHANGING TREND. " 

    if hightrend == 3 and lowtrend == 3:
        signal = "--"
        comment = comment + "UPTREND HIGHER HIGH AND HIGHER LOW IN LAST 3 DAYS"
    elif hightrend == 2 and lowtrend == 2:
        signal = "--"
        comment = comment + "ENTERING UPTREND. HIGHER HIGH AND HIGHER LOW"
    elif hightrend == 4 and lowtrend == 4:
        signal = "--"
        comment = comment + "DOWNTREND LOWER HIGH AND LOWER LOW IN LAST 3 DAYS"
    elif hightrend == 1 and lowtrend == 1:
        signal = "--"
        comment = comment + "ENTERING DOWNTREND. LOWER HIGH AND LOWER LOW"


    return signal, comment
