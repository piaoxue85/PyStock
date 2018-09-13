
import csv
import random
import math
import operator

import os
import sys, getopt

import itertools

import sharedfunctions as fn

import download as dl

from timeit import default_timer as timer
import datetime as dt

import pandas as pd
import numpy as np

import copy

import time

import daychart

import formatter

global ls_symbols
global argv
global ofilename
global df1

from shutil import copyfile


para  = ''

import glob

global ls_ca_file
global ls_ca_comment
global ls_ca_pricelevel

ls_ca_file = []
ls_ca_comment = []
ls_ca_pricelevel = []



def run(market=''):

        global ls_symbols
        global dt_today
        global para

        global ofilename

        global df1

        dt_today = dt.datetime.now().date()

        directory = "data\\google\\"
        filepath = directory + "gdata.csv"
        global df_googleData
        df_googleData = pd.read_csv(filepath)

        symlist = ''

        #onhand
        directory = "data\\google\\"
        filepath = directory + "transactions.csv"
        df_trans = pd.read_csv(filepath)
        ls_symbols = fn.onhandsymbols(df_trans)
        ofilename = 'OnHand'
        main()

        #with trading history
        ls_symbols = df_trans.SYMBOL.unique()
        ofilename = 'Traded'
        main()

        if market <> '':

                #directory = "results\\"
                #filepath = directory + ofilename + ".csv"
                #df1 = pd.read_csv(filepath)
                #dfA = df1[(df1['ONHAND'] > 0) & (df1['MARKET']==market)]
                #daychart.run(dfA,ofilename,ofilename,market)
                
                symlist = market
                ls_symbols = fn.readsymbols(df_googleData, symlist)
                ofilename = 'output-' + market
                ls_file, ls_analysis, ls_pricelevel = main()
                ls_output = []
                for item in ls_file:
                        ls_output.append(item.split(','))                                
                headers = ls_output[0]
                data = ls_output[1:]
                df_output = pd.DataFrame.from_records(data, columns=[headers])
                df_output = fn.dfastype(df_output)
                odir = 'results\\listdata\\'
                filepath = odir + 'LIST-' + market + '.csv'
                df_output.to_csv(filepath, index=False)
                
                select(market, df_output)

                #group list
                directory = "data\\google\\"
                filepath = directory + "symbolgroup.csv"
                global df_symbolGroup
                df_symbolGroup = pd.read_csv(filepath)

                groups = df_symbolGroup.GROUPNAME.unique()

                for g in groups:
                        ls_symbols = df_symbolGroup.loc[df_symbolGroup['GROUPNAME'] == g]['SYMBOL'].tolist()
                        ofilename = g
                        main()
        
        return

def select(market, df_output):

        global ls_symbols
        global ofilename
        global dt_today
        global df1
        
        dt_today = dt.datetime.now().date()
        
        df1 = df_output
                
        df2 = df1[(df1['RSI9'] >= 70)]
        df2 = df2.sort(['RSI9','PE'])
        ls_symbols = df2['SYMBOL'].tolist()        
        ofilename = 'Overbought-' + market 
        main()
        #daychart.run(df2,ofilename,ofilename,market)

        df2 = df1[(df1['RSI9'] < 30)]   
        df2 = df2.sort(['RSI9','PE'])
        ls_symbols = df2['SYMBOL'].tolist()
        
        ofilename = 'Oversold-' + market
        main()
        #daychart.run(df2,ofilename,ofilename,market)

        #rules = [14.9307,14.14307,14.25307,16]

        ofilename = 'Sell-' + market 
        createSignalFile(df1,'SELL')

        ofilename = 'Buy-' + market 
        createSignalFile(df1,'BUY')

        #ls_symbols = df1.loc[(df1['LTREND'] < 0) &(df1['TREND'] > 0) and df1['ONHAND'] <= 0]['SYMBOL'].tolist()
        df2 = df1
        df2 = df2.loc[df2['ONHAND'] == 0]
        df2 = df2.loc[(df2['LTREND'] < 0) &(df2['TREND'] > 0)]
        df2 = df2.loc[df2['LSELLPCT'] > 1]
        ls_symbols = df2['SYMBOL'].tolist()
        ofilename = 'BuyBack-' + market 
        main()
        
        ls_symbols = df1.loc[(df1['LTREND'] < 0) &(df1['TREND'] > 0)]['SYMBOL'].tolist()
        ofilename = 'PiUP-' + market 
        main()

        ls_symbols = df1.loc[(df1['LTREND'] > 0) &(df1['TREND'] < 0)]['SYMBOL'].tolist()
        ofilename = 'PiDown-' + market
        main()

        ls_symbols = df1.loc[(df1['RSI9CHG'] > 1)]['SYMBOL'].tolist()
        ofilename = 'Up-' + market 
        main()

        ls_symbols = df1.loc[(df1['RSI9CHG'] < 1)]['SYMBOL'].tolist()
        ofilename = 'Down-' + market
        main()

def createSignalFile(df1, signal):

        global ls_symbols
        rules = [14.9307,14.14307,14.25307,16]

        ls_symbols = []
        for rule in rules:
                ls_symbols = ls_symbols + readSignal(df1,rule,signal)


        df2 = df1[df1['SYMBOL'].isin(ls_symbols)]        
        
        df2 = df2.sort(['LV252','PE'])
        
        ls_symbols = df2['SYMBOL'].tolist()        

        #unique symbols
        #ls_symbols = list(set(ls_symbols))
        #ls_symbols.sort()

        main()
        
        return

def readSignal(df1, rule, signal='BUY'):

        fldName = 'R' + str(rule)
        dfR = df1[(df1[fldName] == signal)]        
        symbols = dfR['SYMBOL'].tolist()
        return symbols

#9 SEP 2018
#Open each file for one time only 
#Stored file opened in a list for reuse
def readFile(filename,ls_files):

        ls_lines = []
        flag = False

        #print 'Reading ' + filename
                
        for i in ls_files:
                if i[0] == filename:
                        #Return from list
                        ls_lines = i[1]
                        flag = True

        if flag == False:
                #Read physical file
                try:
                        f = open(filename)
                        ls_lines = f.readlines()
                        ls_files.append([filename,ls_lines])
                        f.close()
                except Exception as e:
                        print 'Cannot open ' + filename
                
        return ls_files, ls_lines
        

def main():
        
        global ls_symbols
        global ls_ca_file
        global ls_ca_comment
        global ls_ca_pricelevel        

        ls_file = []
        ls_analysis = []
        ls_pricelevel = []
        header = ''
        
        for s in ls_symbols:

                odir = "results\\listdata\\"
                fnn = fn.filenameFormatter(s)
                ofile = odir + fnn + '.csv'

                try:
                        ls_ca_file, lines = readFile(ofile,ls_ca_file)                            
                        ls_file.append(lines[-1])
                        if header == '':
                                colheaders = lines[0].split(',')
                                if colheaders[0] == 'SYMBOL':
                                        header = lines[0]

                except:
                        print 'Error in opening ' + ofile
                        continue


                odir = "results\\comment\\"
                ofile = odir + fnn + '.csv'
                try:

                        ls_ca_comment, lines = readFile(ofile,ls_ca_comment)   
                        for line in lines:
                                ls_analysis.append(line)

                except:
                        print 'Error in opening ' + ofile
                        continue                        
                                

                odir = "results\\pricelevel\\"
                ofile = odir + fnn + '.csv'
                ls_ca_pricelevel, lines = readFile(ofile,ls_ca_pricelevel)                 
                try:    

                        for line in lines:
                                ls_pricelevel.append(line)                               
                except:
                        print 'Error in opening ' + ofile
                        continue                        

        openFile()

        if header <> '':
                ls_file.insert(0, header)
                
        for r in ls_file:
                printout (r)

        printout("\n")

        for r in ls_analysis:
                printout(r)

        printout("\n")

        for r in ls_pricelevel:
                printout(r)
				
        url = "<a href=\"https://www.interactivebrokers.com/calendar/\" target=\"blank\">Trading Calendar</a>&nbsp"
        printout(url)
        printout("Source: Galileo Stock Analyzer")

        closeFile()
                
        odir = "results\\"
        sfile = odir + ofilename + '.csv'
        hfile = odir + ofilename + '.htm'
        formatter.convertfile(sfile,hfile)
                        
        return ls_file, ls_analysis, ls_pricelevel

def GetGoogleData(s):
    r = df_googleData[(df_googleData.SYMBOL == s)]
    return r

def openFile():

        global outputfile1
        global outputfile2
        global outputfile3
        global outputfile4
        global outputfile

        global text_file1
        global text_file2
        global text_file3
        global text_file4

        global para

        odir = "results\\"
        outputfile1 = odir + ofilename + '.csv'
        #outputfile2 = odir + 'output\\' + ofilename + '.csv'
        outputfile3 = odir + ofilename + '.txt'
        outputfile4 = odir + 'historical\\' + ofilename + '-' + str(dt_today) + '.txt'
        
        try:
            text_file1 = open(outputfile1, "w")
            outputfile = outputfile1
        except:
            print "Error in opening " + outputfile1
            text_file1 = open(outputfile3, "w")
            outputfile = outputfile3
            
        return

def printout(str):

        try:
                text_file1.write(str)
        except:
                print "Error in writing " + outputfile1

        return

def closeFile():

        global outputfile
        global outputfile4
    
        try:
                text_file1.close()
        except:
                print "Error in closing " + outputfile

        print "Copying to " + outputfile4
        copyfile(outputfile, outputfile4)

        return


