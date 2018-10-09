
import os
import sys, getopt

import itertools

from lib import sharedfunctions as fn
from lib import download as dl
from lib import main as mn
from lib import consolidate as consol

from timeit import default_timer as timer
import datetime as dt

import pandas as pd
import numpy as np

import copy

import time

global argv

#For storing processed symbols
global ls_symbols3

import sys

para  = ''
markets = ['HSI','ASX','NYSE']

ls_symbols3 = []

def run(ls_symbols, dfs):
        global ls_symbols3

        #removing processed symbols, i.e. onhand
        for s in ls_symbols3:
                try:
                        ls_symbols.remove(s)                       
                except:
                        pass        
        
        for s in ls_symbols:
                ls_symbols3.append(s)
                try:
                        mn.run(s,dfs)
                except SystemExit as e:
                        print "SystemExit " + s + " " + str(e)
                except Exception as e:
                        print "Main exception " + s + " " + str(e)
        return

def runOnhand():

        market = 'onhand'
        dfs = mn.prepareRefDf(market)
        df_trans = dfs[1]
        ls_symbols1 = fn.onhandsymbols(df_trans)
        ofilename = 'onhand'        
        run(ls_symbols1,dfs)
        consol.run()
        return

def main(market):

        dt_today = dt.datetime.now().date()
        dfs = mn.prepareRefDf(market)
        df_googleData = dfs[0]
        symlist = ''
        ls_symbols2 = fn.readsymbols(df_googleData,market)
        ofilename = 'output-' + market
        run(ls_symbols2, dfs)
        consol.run(market)
        return
             

argv = sys.argv

if len(argv)>1:
        print argv[1]
        runOnhand()
        main(argv[1])
else:
        dl.googleData()
        dl.transactions()       
        runOnhand()
        dl.symbolgroup()        
        for market in markets:
                main(market)
                ls_symbols3 = []
