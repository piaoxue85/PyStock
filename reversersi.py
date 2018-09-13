
import os
import sys, getopt

import itertools

from lib import sharedfunctions as fn
from lib import main as mn
from lib import knndata

from timeit import default_timer as timer
import datetime as dt

from datetime import datetime

from lib import technical_indicators as ti

import pandas as pd
import numpy as np
from numpy import array

import copy

import time

global argv
global ofilename

para  = ''

def main(market):

        directory = "data\\google\\"
        filepath = directory + "gdata.csv"
        global df_googleData
        df_googleData = pd.read_csv(filepath)

        ls_symbols = fn.readsymbols(df_googleData,market)

        odir = "results\\reversersi\\"
        ofilename = "reversersi-" + market
        outputfile = odir + ofilename + '.csv'

        period = 9

        text_file = open(outputfile, "w")
        headers = "SYMBOL,ASAT,PRICE,OVERBOUGHT,OVERSOLD,OBCHG%,OSCHG%,OBOSDIFF"
        text_file.write(headers + "\n")
      
        for s in ls_symbols:

                try:
                        ret = reversersi(s, period)
                        if ret[1] > 0:
                                tsr = ret
                                str1 = ','.join(str(e) for e in tsr)
                                text_file.write(str1 + "\n")
                except SystemExit as e:

                        print "SystemExit " + str(e)

                except Exception as e:
                        print "Main exception " + str(e)
        text_file.close()
        print "Open " + outputfile

def reversersi(s, period=9):
        
        dt_timeofday = dt.timedelta(hours=16)
        dt_today = dt.datetime.now().date()
        
        beginDate = dt.datetime.now() - dt.timedelta(days=960)
        #beginDate = str(beginDate.year) + '-' + str(beginDate.month) + '-' + str(beginDate.day)

        dt_end = dt.datetime.now() - dt.timedelta(days=0)
        #endDate = str(dt_end.year) + '-' + str(dt_end.month) + '-' + str(dt_end.day)
        #beginDate = dt.datetime.now() - dt.timedelta(days=960)
        
        beginDate = beginDate.date()
        endDate = dt_end.date()

        ls_data = knndata.getData(s, beginDate, endDate)

        headers = ls_data[0]

        vals = []
        hb = len(ls_data)
        
        for i in range(1, hb):
                tdt = ls_data[i][headers.index("DATE")]
                vals.append(float(ls_data[i][headers.index("CLOSE")]))

        ret1, ret2 = knndata.reversersi(vals, period)

        asat = ls_data[i][headers.index("DATE")]
        price = float(ls_data[-1][headers.index("CLOSE")])
        
        fs = fn.symbolFormatter(s)
        
        ret = [fs, asat, price]+ ret2

        return ret

if __name__ == '__main__':

    argv = sys.argv
    para = ""
    if len(argv)>1:
        main(argv)            
    else:
        main('NYSE')
