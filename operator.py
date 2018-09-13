
import os
import sys, getopt

import itertools

from lib import sharedfunctions as fn
from lib import download as dl

from timeit import default_timer as timer
import datetime as dt

import pandas as pd
import numpy as np

import copy

import time

import subprocess


def main():

        dt_now = dt.datetime.now()

        h = dt_now.hour
        m = dt_now.minute

        ts = h *100 + m

        sfnn = "status\\operator.txt"

        ts2 = fn.readStatus(sfnn)	
		
        if len(ts2) > 0:
                ts2 = int(ts2)
                delta = ts - int(ts2)
                
        goahead = False 
        if delta < 0 or delta >= 60:
                goahead = True

        ##if goahead == False:
        ##        print "Wait for other instance started at " + str(ts2)
        ##        return                 
		
        fn.updateStatus(sfnn,str(h) + str(m).zfill(2))

        dl.googleData()
        dl.transactions()

        ##ASX trading hours     
        if ts >= 700 and ts < 1615:
                markets = ['ASX','HSI']

        ##HSI trading hours
        if ts >= 1615 and ts < 1830:
                markets = ['HSI','ASX']

        if ts >= 1830 and ts <= 2000:
                markets = ['NYSE','HSI']

        ##NYSE trading hours
        if ts >= 2000 or ts <= 700:
                markets = ['NYSE']

        for market in markets:
                updateQuote(market)
                analyse(market)
            
        for market in markets:
                appendPriceQuote(market)                    

        if goahead == True:
                updateHistorical()
                getTrade()
##
##                
##        if ts >= 1015 and ts <= 1430:
##                updateQuote("ASX")
##                analyse("ASX")
##
##        if ts >= 1015 and ts <= 1330:
##                updateQuote("HSI")
##                analyse("HSI")
##
##        if ts >= 1300 and ts < 1330:
##                updateQuote("NYSE")
##                appendPriceQuote('NYSE')
##                analyse("NYSE")
##                clearRAMDrive()                
##                updateHistorical()
##                predict("NYSE")                
##                                
##        if ts >= 1330 and ts < 1630:           
##                updateQuote("HSI")
##                analyse("HSI")
##                                
##        if ts >= 1600 and ts < 1630:     
##                updateHistorical()
##                updateQuote("NYSE")                
##                appendPriceQuote("NYSE")
##                analyse("NYSE")
##                appendPriceQuote("ASX")
##                reversersi("ASX")
##                analyse("ASX") 
##                predict("ASX")
##                analyse("ASX")                
##                        
##        if ts > 1700 and ts < 1730:                
##                updateQuote("HSI")
##                appendPriceQuote("HSI")
##                reversersi("HSI")
##                analyse("HSI")
##                predict("HSI")
##                analyse("HSI")
##                #getDayChart()

        #Before NYSE trading hours
        if ts >= 1900 < ts < 2130:
                clearRAMDrive()                
                
##        if ts >= 2030 or ts < 700: 
##                updateQuote("NYSE") 
##                analyse("NYSE")
##                updateQuote("ASX") 
##                analyse("ASX")
##                updateQuote("HSI") 
##                analyse("HSI")                
##                appendPriceQuote("NYSE")           
##                updateHistorical()
                
##        fn.updateStatus(sfnn,"-1000")

        return

def getTrade():
        filepath="/batch/trade.bat"
        callsub(filepath)
        return

def getDayChart():
        filepath="/batch/getDayChart.bat"
        callsub(filepath)
        return

def appendPriceQuote(arg):
        filepath="/batch/appendPriceQuote.bat " + arg
        callsub(filepath)
        return

def clearRAMDrive():
        filepath="/batch/clearRamDrive.bat"
        callsub(filepath)
        return

def analyse(arg):
        filepath="/batch/analyse.bat " + arg
        callsub(filepath)
        return

def updateHistorical():
        filepath="/batch/updateHistorical.bat"
        callsub(filepath)
        return

def reversersi(arg):
        filepath="/batch/reversersi.bat " + arg
        callsub(filepath)
        return

def predict(arg):
        filepath="/batch/predict.bat " + arg
        callsub(filepath)
        return

def updateQuote(arg):
        filepath="/batch/updateQuote.bat " + arg
        callsub(filepath)
        return

def callsub2(filepath):
        print filepath
        return
        
def callsub(filepath):

        dt_now = dt.datetime.now()
        filepath = 'G:\Python' + filepath
        print fmttime(dt_now) +  " " + filepath + " running"
        p = subprocess.Popen(filepath, shell=True, stdout = subprocess.PIPE)
        stdout, stderr = p.communicate()
        dt_now = dt.datetime.now()        
        if p.returncode == 0:
                print fmttime(dt_now) + " " + filepath + " completed"
        else:
                print fmttime(dt_now) +  " " + filepath + " failed"

        return

def fmttime(d):
        fmt = '%Y-%m-%d %H:%M:%S'
        d_string = d.strftime(fmt)
        d2 = dt.datetime.strptime(d_string, fmt)
        return str(d2)

main()


