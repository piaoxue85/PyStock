
import os
import sys, getopt

import itertools

from lib import sharedfunctions as fn
from lib import download as dl
from lib import main as mn
from lib import consolidate as consol
from lib import knndata as data

from timeit import default_timer as timer
import datetime as dt

import pandas as pd
import numpy as np

import copy

import time

global ls_symbols
global argv
global ofilename

para  = ''

def run():

        for s in ls_symbols:

                beginDate = '2014-11-09'
                endDate = '2016-12-31'

                data1 = data.getData(s,beginDate, endDate)

                df = pd.DataFrame(data1[1:], columns=data1[0])

                beginDate = '2016-11-09'
                endDate = '2016-12-31'
                
                df = df[(df['DATE'] >= beginDate) & (df['DATE'] <= endDate)] 

                close1 = df.iloc[0]['CLOSE']
                close2 = df.iloc[-1]['CLOSE']                
                closechg = ( close2- close1) / close1 * 100
                print fn.symbolFormatter(s) + ' '  + str(close1) + ' ' + str(close2) + ' ' + str(closechg)
                        
        return

def main():

        global ls_symbols


        argv = sys.argv
        if len(argv)>1:
                para = ",".join(argv)

        directory = "data\\google\\"
        filepath = directory + "gdata.csv"
        global df_googleData
        df_googleData = pd.read_csv(filepath)

        symlist = ''

        market = 'HSI'

        ls_symbols = fn.readsymbols(df_googleData,market)
        print ls_symbols
        run()


       


main()
