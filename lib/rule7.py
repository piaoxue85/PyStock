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

def apply(data, idx):

    #high = df_high[s].max()
    #highidx = df_high[s].argmax()
    #low = df_low[s].min()
    #lowidx = df_low[s].argmin()

    headers = data[0]
    
    col = headers.index("HIGH")
    high2 = data[idx-1][col]
    high1 = data[idx][col]

    col = headers.index("LOW")
    low2 = data[idx-1][col]
    low1 = data[idx][col]

    col = headers.index("LV252")
    lv2 = data[idx-1][col]
    lv1 = data[idx][col]


    signal = ""
    comment = ""

    if lv1 >= 1:
        signal = "BUY"
        comment = "BREAKING THE MENTAL BARRIER 52 WEEKS HIGHEST(" + str(high1)+ "). " 

        if lv2 >= 1:
            comment = "KEEP BREAKING THE MENTAL BARRIER 52 WEEKS HIGHEST(" + str(high2) + ") NEW HIGHEST (" + str(high1)+ "). "

        #if close1 < rhigh2:
        #    comment = comment + "THIS MENTAL BARRIER KEEP PRICES COMPRESSED. A JUMP AHEAD"
        
    #It seems excess gains come from investor under-reaction to positive news when a stock is nearing the 52-week high.
    #While the stock should be trading at a certain level based on available information, the fear of the stock nearing 52-week high resistance weighs down share prices.
    #Once the 52-week high resistance is finally breached, the stock pops upwards to its "correct" pricing.
    #This action in price movement goes against the efficient market hypothesis, which argues that prices trade at their inherent value at all times.
    if lv2 >=1 and lv1  < 1:
        signal = "SELL"
        comment = "LEAVING 52 WEEKS HIGHEST(" + str(high1) + "). SEE ANY SELL SIGNAL."
        
    if lv1 == 0:
        signal = "--"
        comment = "BREAKING 52 WEEKS LOWEST (" + str(low1) + "). WAIT UNTIL PRICE STOPPED DROPPING"

    if lv2 == 0:
        signal = "BUY"
        comment = "BOUNCING AT 52 WEEKS LOWEST (" + str(low1) + "). CONSIDER (" + str(low1) + ") AS MENTAL SUPPORT"
        
    return signal, comment

