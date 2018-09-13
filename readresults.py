
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

def main(argv):

        directory = "F:\\results\\historical\\"
        filepath = directory + "consol-buy.txt"
        df_buy = readlist(filepath)

        df_buy['SHARE'] = 100
        df_buy['AMOUNT'] = df_buy['SHARE'] * df_buy['CLOSE']

        directory = "F:\\results\\historical\\"
        filepath = directory + "consol-sell.txt"
        df_sell = readlist(filepath)

        df_sell['SHARE'] = -100
        df_sell['AMOUNT'] = df_sell['SHARE'] * df_sell['CLOSE']

        dfs = [df_buy, df_sell]
        df_consol = pd.concat(dfs)

        df_consol = df_consol.sort(['SYMBOL','DATE'])

        ofilename = "results\\resultanalysis\\autotrade.csv"
        df_consol.to_csv(ofilename, index=False)

        


def readlist(filepath):

        df_files = pd.read_csv(filepath)

        df_result = read(df_files.iloc[0]['FILEPATH'])
        flist = df_files['FILEPATH'][1:].tolist()

        for f in flist:
                print f
                df = read(f)
                dfs = [df_result, df]
                df_result = pd.concat(dfs)
                
        return df_result

def read(filepath):

        columns = ['SYMBOL','DATE','CLOSE','RSI9']

        df = pd.read_csv(filepath)
        df1 = df[(df['CLOSE'] > 0)]
        df2 = df1[columns]
        return df2

if __name__ == '__main__':

    argv = sys.argv

    
    if len(argv)>1:
        para = ",".join(argv)
        main(argv[1])
        print "[" + para + "]"
    else:
        main('F:\\results\\historical\\Buy-HSI-2018-01-22.txt')
