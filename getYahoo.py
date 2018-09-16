
import itertools

from lib import main as mn
from lib import sharedfunctions as fn
from lib import globalfile
from lib import globaldf
from lib import knndata

import datetime as dt
import os

def getSymbols(market):

        if market == 'OnHand':
                directory = "data\\google\\"
                filepath = directory + "transactions.csv"
                df_trans = globaldf.read(filepath)
                ls_symbols = fn.onhandsymbols(df_trans)
        else:
                directory = "data\\google\\"
                filepath = directory + "gdata.csv"
                df_googleData = globaldf.read(filepath)
                ls_symbols = fn.readsymbols(df_googleData,market)
                
        return ls_symbols[0:10]

def symformatter(symbol,market='HSI'):

        ret = symbol        
        if symbol.isdigit():     #HSI
                ret = symbol + '.HK'

        if symbol[0:3] == 'ASX':        #ASX
                ret = symbol[4:] + '.AX'                

        return ret

def removeDataFile(ls_symbols):

        print 'Removing data files'
        df_confile = globaldf.read('getyahoo.cfg')
        ddir = df_confile[df_confile.KEY=='DDIR'].iloc[0]['VALUE']
        ls_symbols = getSymbols(market)
        for symbol in ls_symbols:
                symbol = symformatter(symbol,market)
                path = ddir + symbol + '.csv'
                try:
                        print 'Removing ' + path
                        os.remove(path)
                except Exception as e:
                        continue

def readDataFile(ls_symbols):

        df_confile = globaldf.read('getyahoo.cfg')
        ddir = df_confile[df_confile.KEY=='DDIR'].iloc[0]['VALUE']
        odir = df_confile[df_confile.KEY=='ODIR'].iloc[0]['VALUE']
        for symbol in ls_symbols:
                fsymbol = symformatter(symbol)
                path = ddir + fsymbol + '.csv'
                try:
                        df_yahoo = globaldf.read(path)
                        df_yahoo = knndata.formatYahooData(df_yahoo)
                        opath = odir + symbol + '.csv'
                        globaldf.update([opath,df_yahoo])
                        globaldf.save(opath)
                except Exception as e:
                        print "Data error " + path + ' ' + str(e)
                        continue
                
        return
        

def genDownloadFile(ls_symbols,fname):

        cookies = 'vzirKUmjia0'

        url = 'https://query1.finance.yahoo.com/v7/finance/download/symbol?period1=1284559200&period2=1537022868&interval=1d&events=history&crumb=' + cookies


        pycode = ''
        for symbol in ls_symbols:
                symbol = symformatter(symbol)
                pycode = pycode +  '"' + symbol + '",\n'

        pycode = pycode[:-2]
                
        lines = globalfile.read('data\\yahoo\\template.htm')

        fdata = []

        for line in lines:
                line = line.replace('//#URL//',url)
                line = line.replace('//#Symbols//',pycode)
                line = line.replace('//#Market//', fname)
                fdata.append(line)

        fname = 'data\\yahoo\\yahoodata-' + fname + '.htm'
        fdata = fdata
        f = [fname,fdata]
        globalfile.update(f,True)
        print fname + ' generated'

        return

def main():

        print "1. Remove old data file"
        print "2. Generate download page"
        print "3. Read data file"
        print "4. Exit"
        sel = input("Selection: ")

        markets = ['OnHand','NYSE','HSI','ASX']
        #TO BE ADDED - ONHAND SYMBOL,PROBLEM TO BE SOLVED

        for market in markets:
                ls_symbols = getSymbols(market)
                if sel==1:
                        removeDataFile(ls_symbols)
                elif sel==2:
                        genDownloadFile(ls_symbols, market)
                elif sel==3:
                        readDataFile(ls_symbols)

main()
