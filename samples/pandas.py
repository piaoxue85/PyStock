import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da
import numpy as np

import math
import copy
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkstudy.EventProfiler as ep

import csv

import simulator as si
import sharedfunctions as fn
import analyzer as an

import pandas

from collections import OrderedDict

import technical_indicators as ti

def testrun():

    dataobj = da.DataAccess('Yahoo')
    ls_symbols = ['0002']
    #ldt_timestamps = fn.GenTimestamps(dt_start, dt_end, 16)

    dt_start = dt.datetime(2012, 12, 1)
    dt_end = dt.datetime(2014, 12, 31)  
    dt_timeofday = dt.timedelta(hours=16)
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)
    d_data, prices = fn.getData(ldt_timestamps, ls_symbols, 'actual_close')

    means = pandas.rolling_mean(prices,20,min_periods=20)
    std = pandas.rolling_std(prices, 20, min_periods=20)
    mx = pandas.rolling_max(prices, 252, min_periods=252)
    bb = (prices - means) / std
    fn.dprint(bb.values)
    fn.dprint(prices['0002'].values)

    bb.to_csv('bb.xls', sep='\t')
    fn.dprint("rolling max")
    fn.dprint(mx.values)
    fn.dprint(mx['0002'][-1])
    rsi = ti.rsi(prices['0002'].values, 9)
    sma = ti.sma(prices['0002'].values, 10)
        
    fn.dprint(rsi)

    fn.dprint(sma)
    
    return

if __name__ == '__main__':
    testrun()    


