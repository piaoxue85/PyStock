import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sharedfunctions as fn

from numpy import *

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


    if hightrend == 1:
        signal = "--"
        comment = "DAY HIGH (" +  str(round(high1,2)) +") IS LOWER THAN YESTERDAY HIGH (" + str(round(high2,2)) + ") LOOK FOR SELL SIGNAL"    
    elif hightrend == 2:
        signal = "--"
        comment = "DAY HIGH (" +  str(round(high1,2)) +") IS HIGHER THAN YESTERDAY HIGH (" + str(round(high2,2)) + ")"
    elif hightrend == 3:
        signal = "--"
        comment = "DAY HIGH (" +  str(round(high1,2)) +") IS 3 DAYS HIGHEST."
    elif hightrend == 4:
        signal = "--"
        comment = "DAY HIGH (" +  str(round(high1,2)) +") IS 3 DAYS LOWEST."
    elif hightrend == 5:
        if low1 <> low2:
            signal = "--"
            comment = "DAY HIGH STOPPED AT (" +  str(round(high1,2)) +"). LOOK FOR SELL SIGNAL"

    return signal, comment

