import os
import sys, getopt

import itertools

from lib import sharedfunctions as fn
from lib import main as mn

from timeit import default_timer as timer
import datetime as dt

from lib import formatter as fileformatter
from lib import knndata

from datetime import datetime, timedelta
from lib import talibw
from lib import globaldf

import pandas as pd

import numpy as np
from numpy import array

import copy
import random
import time
import trade

global bfile
global sfile
global bheader
global sheader

#TAKE PROFIT, STOP LOSS
global fixedplfile
global fixedplheader

global sDate
global eDate
global brules
global srules
global bpatterns
global spatterns

sDate = '07/01/2015'
sDate = dt.datetime.strptime(sDate, '%m/%d/%Y').date()
        
eDate = '12/31/2018'
eDate = dt.datetime.strptime(eDate, '%m/%d/%Y').date()  

para  = ''
#ls_rules = [1,2,3,4,5,6,6.1,7,8,8.1,8.2,8.3,8.4,9,10,11,12,13, 14.93070,14.92080,14.143070,14.142080]

#BUY RULES
brules = [6,14.93070,14.143070,14.253070,16]
#brules = [14.93070,14.143070,14.253070, 16]
#SELL RULES
srules = brules

#BUY PATTERNS
patterns = talibw.getcdlpatterns()
bpatterns = []
brules = brules + bpatterns

#SELL PATTERNS
spatterns = bpatterns
srules = srules + spatterns

#TAKE PROFIT%
takeprofit = 0.02
#STOP LOSS% in integer 3% = 0.03
stoploss = 0.05

#INVESTMENT AMOUNT PER ORDER
iamt = 1000

#TARGET ROI PA in integer 1% = 0.01
targetROI = 0.1

ls_rules = brules

odir = "results\\autotrade\\"
rdir = "results\\backtest\\"


#DIRECTORY FOR BUY ORDERS
bdir = odir + "\\buy\\"

#DIRECTORY FOR SELL ORDERS
sdir = odir + "\\sell\\"

tdir = odir + "\\orders\\"

gdir = "data\\google\\"

market = ''

global df_googleData

def getSymbols():
        
        global df_googleData
            
        ls_symbols1 = fn.readsymbols(df_googleData,'HSI')
        ls_symbols2 = fn.readsymbols(df_googleData,'ASX')
        ls_symbols3 = fn.readsymbols(df_googleData,'NYSE')

        ls_symbols = ls_symbols1 + ls_symbols2 + ls_symbols3

        ls_symbols = random.sample(ls_symbols, 1)

        directory = "\\python\\data\\google\\"
        filepath = directory + "transactions.csv"

        df_trans = trade.readOrderFile(filepath)
        
        ls_symbols = df_trans.SYMBOL.unique()

        ls_symbols = ls_symbols1 + ls_symbols2 + ls_symbols3

        ls_symbols =['ASX-ASX']

        return ls_symbols

def readResults(ls_symbols):

        df_allstat = pd.DataFrame()

        for symbol in ls_symbols:

                fsymbol  = fn.filenameFormatter(symbol)
                bsfile = rdir + '\\' + fsymbol + '-STATS.csv'
                try:
                        df_stat = pd.read_csv(bsfile, dtype={'P.TYPE': 'S30', 'S.TYPE': 'S30'})
                        df_allstat = fn.dfconcat(df_allstat,df_stat)
                except Exception as e:
                        print "Cannot open " + bsfile

        df_results = findResults(df_allstat,targetROI)
        rfile = rdir + '\\' 'ROI-' + str(int(targetROI*100)) + '.csv'
        print str(len(df_results)) + " results"
        print 'Read ' + rfile
        #df_results.to_csv(rfile,index=False)

        df_output = df_results[['SYMBOL','P.TYPE','S.TYPE','STOPLOSS','TRADE-TO-TRADE','RZ.W.PCT','AVG.RZ.HOLD','AVG.RZ.PROFITPCT','AVG.RZ.PROFITPCT252D']]
        df_output.to_csv(rfile,index=False)
        #print df_display.to_html()

        return df_output
    
def main2():

        ls_symbols = getSymbols()

        #DATASOURCE
        #TRUE - GENERATE NEW TEST DATA
        #FALSE - FROM BACKTEST FILE
        if True == True:
                test(ls_symbols)

        readResults(ls_symbols)                

        return


#def readBuySignal(market):
def main(market='ASX'):

        global brules
        global srules
        global bpatterns
        global spatterns

        df_allstat = pd.DataFrame()
        df_alltrades = pd.DataFrame()         

        filepath = gdir + "gdata.csv"
        global df_googleData
        #df_googleData = pd.read_csv(filepath)
        df_googleData = globaldf.read(filepath)
        
        odir = "results\\listdata\\"
        ofilename = 'list-' + market + '.csv'
        filepath = odir + ofilename

        print filepath
        df_output = globaldf.read(filepath)
      
        df_prices = df_output[['SYMBOL','DATE','OPEN','HIGH','LOW','CLOSE','CLOSECHG']]
        df_prices = df_prices[df_prices['CLOSE'] > 0]
        df_prices['DATE'] =  pd.to_datetime(df_prices['DATE']).apply(lambda x: x.date())        

        srules = ls_rules
        spatterns = []
        bpatterns = []

        for rule in ls_rules:
                brules = [rule]
                colname = 'R' + str(rule)

                df_results = df_output[df_output[colname]=='BUY']
                ls_symbols = df_results['SYMBOL'].tolist()

                df_trades, df_stat  = test(ls_symbols)
                df_alltrades = fn.dfconcat(df_alltrades,df_trades)
                if len(df_stat) > 0:
                        df_selected = df_stat[(df_stat['AVG.RZ.PROFITPCT252D'] >= targetROI * 100) & (df_stat['RZ.W.PCT'] >= 80)]
                        df_allstat = fn.dfconcat(df_allstat,df_selected)                           

        if len(df_allstat) > 0:
                rdir2 = 'results\\' 
                rfile = rdir2 + 'orders-' + market + '.csv'                
                df_output = df_allstat[['SYMBOL','P.TYPE','S.TYPE','STOPLOSS','TRADE-TO-TRADE','RZ.W.PCT','AVG.RZ.HOLD','AVG.RZ.PROFITPCT','AVG.RZ.PROFITPCT252D']]
                df_orders = pd.merge(df_output, df_prices, on='SYMBOL', how='left')
                df_orders['STOPLOSSPRICE'] = (1 - df_orders['STOPLOSS']) * df_orders['CLOSE']
                df_orders['TARGETPRICE'] = (df_orders['AVG.RZ.PROFITPCT']/100) * df_orders['CLOSE'] + df_orders['CLOSE']
                #temp = df_orders['AVG.RZ.HOLD'].apply(np.ceil).apply(lambda x: pd.Timedelta(x, unit='D'))

                #ADDING DAYS TO ORDER DATE FOR SELL DATE.
                #REQUIRE TO DO IT IN A LIST UNLESS UPDATING NUMPY AND PANDAS
                #10 SEP 2018
                df_orders['SELLDATE'] = df_orders['DATE']
                Ss_date = df_orders['DATE']
                Ss_timedelta = df_orders['AVG.RZ.HOLD']
                ls_timedelta = Ss_timedelta.values.astype('timedelta64[D]').tolist()
                ls_selldate = []
                for i in range(0, len(ls_timedelta)):
                        try:
                                selldate = Ss_date[i] + ls_timedelta[i]
                        except Exception as e:
                                selldate = Ss_date[i]
                                
                        ls_selldate.append(selldate)                                                                
                df_orders['SELLDATE'] = pd.Series(ls_selldate)

                
                df_orders.to_csv(rfile,index=False)                  
                print 'See ' + rfile

        else:
                print 'No suggesting order'

        return

def test(ls_symbols):

        df_allstat = pd.DataFrame()
        df_alltrades = pd.DataFrame()        

        print "Symbols: " + ', '.join(ls_symbols)
        print "Test date range: " + str(sDate) + ' - ' + str(eDate)
        print "Target ROI: " + str(round(targetROI*100,0)) + "% pa"

        for symbol in ls_symbols:

                try:
                        print "Preparing data - " + symbol
                        #not to read knn cache, create new knn cache              
                        dataset = knndata.getData(symbol,sDate, eDate, True, False)
                        df_dataset = knndata.getdfdata(dataset)
                        createorder(symbol, dataset, df_dataset)
                        df_trades, df_stat = pairingorder(symbol, df_dataset)
                        df_alltrades = fn.dfconcat(df_alltrades,df_trades)
                        df_allstat = fn.dfconcat(df_allstat,df_stat)

                except Exception as e:

                        print symbol + ' - ' + str(e)

                except SystemExit as e:                        

                        print symbol + ' - ' + str(e)

                print "Completed - " + symbol          

        return df_alltrades, df_allstat

                
def pairingorder(symbol, df_tdata, keepoldresults = False):

        df_allstat = pd.DataFrame()
        df_alltrades = pd.DataFrame()

        fsymbol  = fn.filenameFormatter(symbol)

        bsfile = rdir + '\\' + fsymbol + '-STATS.csv'
        btfile = rdir + '\\' + fsymbol + '-TRANS.csv'        

        rules = []

        maxlosspct = 10

        for b in brules:
                for  s in srules:
                        rules.append([str(b),str(s), 0])
                        for mloss in range(2, maxlosspct, 1):
                                rules.append([str(b),str(s), float(mloss) / 100])                        
                rules.append([str(b),'FIXEDPL',stoploss])
                                          
        try:
                df_backtestResults = pd.read_csv(bsfile, dtype={'P.TYPE': 'S30', 'S.TYPE': 'S30'})
                gloabldf.update([bsfile,df_backtestResults])
                df_backtestTrans = pd.read_csv(btfile, dtype={'P.TYPE': 'S30', 'S.TYPE': 'S30'})
                gloabldf.update([btfile,df_backtestTrans])                
        
        except Exception as e:

                df_backtestResults = pd.DataFrame()
                df_backtestTrans = pd.DataFrame()

        oldresultscount = len(df_backtestResults)

        if keepoldresults  == True:
                for index, result in df_backtestResults.iterrows():
                        val = [str(result['P.RULE']),str(result['S.RULE'])],str(result['STOPLOSS'])
                        try:
                                rules.remove(val)
                                print str(val) + ' found in backtest results and is removed'
                        except Exception as e:
                                pass
                                #print str(val) + ' ' + str(e)

        ls_bfiles = []
        ls_sfiles = []

        dDate1 = df_tdata.iloc[0]['DATE']       #DATE OF FIRST DATA RECORD
        dDate2 = df_tdata.iloc[-1]['DATE']      #DATE OF LAST DATA RECORD

        for rule in rules:
  
                b = str(rule[0])
                s = str(rule[1])
                mloss = rule[2]

                print 'Processing ' + str(symbol) + ' - BUY: ' + b + ' SELL:' + s + ' MAX LOSS: ' + str(mloss)

                fnn = 'buy-' + str(symbol) + '-' + str(b)
                bfilename = bdir+ fnn + ".csv"
                ls_bfiles, dfB = openorderfile(ls_bfiles,bfilename)
                                
                bcount= len(dfB)
                
                if bcount > 0:

                        if s == 'FIXEDPL':
                        
                                fnn = 'fixedpl-' + str(symbol) + '-' + str(b)
                                plfilename = sdir+ fnn + ".csv"
                                #print plfilename
                                #Not required to save into a list. One pl file per each buy order file
                                df_strans = trade.readOrderFile(plfilename)                              
                                df_btrans = dfB.copy()

                        else:
                                                               
                                df_btrans = dfB.copy()
                                df_strans = pd.DataFrame()
                                fnn = 'sell-' + str(symbol) + '-' + str(s)
                                sfilename = sdir + fnn + ".csv"
                                ls_sfiles, dfS = openorderfile(ls_sfiles,sfilename)                                       
                                                         
                                for bindex in range(0,bcount):
                                        
                                        df_btran = dfB.iloc[bindex].copy()
                                        df_bmatch = pd.DataFrame()
                                        df_smatch = pd.DataFrame()                                        

                                        if len(dfS) > 0:
                                                df_bmatch = dfS[(dfS['DATE'] > df_btran['DATE']) & (dfS['SYMBOL'] == df_btran['SYMBOL'])]

                                        if len(df_bmatch) > 0:
                                                df_bmatch = df_bmatch.iloc[0]
                                                mdate = df_bmatch['DATE']

                                        #APPLY STOP LOSS
                                        df_loss = pd.DataFrame()
                                        if mloss > 0:
                                                slp = df_btran['PRICE'] * (1 - mloss)
                                                df_profit, df_loss, df_pl, sprice = trade.get_dfstopprofit_dfstoploss(df_tdata, df_btran['DATE'], 0, slp)

                                        if len(df_loss) > 0:
                                                ldate = df_loss['DATE']

                                        loss = True
                                        if len(df_loss) > 0 and len(df_bmatch) > 0:
                                                if ldate > mdate:
                                                        loss = False

                                        if len(df_loss) == 0:
                                                loss = False

                                        if loss == True:                                                
                                                remark = 'STOP LOSS' + str(stoploss) + '%'
                                                ldate = df_loss['DATE']
                                                df_smatch = trade.formatOrder(df_btran['SYMBOL'],ldate ,sprice,-df_btran['SHARES'],remark)                                                
                                        else:
                                                if len(df_bmatch) > 0:
                                                        df_smatch = trade.formatOrder(df_bmatch['SYMBOL'],mdate,df_bmatch['PRICE'],-df_btran['SHARES'],s)

                                        df_strans = fn.dfconcat(df_strans,df_smatch)  


                                #No sell matched, create a dummy transaction for execute
                                if len(df_strans) == 0:                                        
                                        df_strans = trade.formatOrder(symbol,np.nan,0,0,s)
                                        
                                
                else:

                        #No buy / sell, create a dummy transaction for execute
                        print "No buy order by rule " + str(b)                        
                        df_dtrans = trade.formatOrder()
                        df_btrans = df_dtrans
                        df_strans = df_dtrans


                df_trades, df_stat = trade.execute(symbol,df_btrans, df_strans, dDate1, dDate2)
                df_trades['P.TYPE'] = b
                df_trades['S.TYPE'] = s
                df_trades['STOPLOSS'] = mloss
                df_stat['P.TYPE'] = b
                df_stat['S.TYPE'] = s
                df_stat['STOPLOSS'] = mloss
                
##2 SEP 2018
##INVALID LOGIC - TO BE REVISED
##                df_stat['SUM.CAPITAL.TOT'] = df_stat['TOT.DAYS'] * iamt
##                df_stat['CAP.UTIL.PCT'] = (df_stat['SUM.CAPITAL.USED'] / df_stat['SUM.CAPITAL.TOT'] * 100).astype(np.double).round(2)
                df_alltrades = fn.dfconcat(df_alltrades,df_trades)
                df_allstat = fn.dfconcat(df_allstat,df_stat)
                if oldresultscount > 0:
                        try:
                                df_backtestResults = df_backtestResults[(df_backtestResults['P.TYPE'] != b) & (df_backtestResults['S.TYPE'] != s) & (df_backtestResults['STOPLOSS'] != mloss)]
                        except Exception as e:
                                print 'Removing backtest results BUY:' + b + ' SELL:' + s + ' ' + str(e)

        if len(df_allstat) > 0:
                df_allstat['FROMDATE'] = dDate1
                df_allstat['TODATE'] = dDate2
                df_allstat['TESTDATE'] = datetime.today().strftime('%Y-%m-%d')

                df_backtestResults = fn.dfconcat(df_backtestResults,df_allstat)
                df_backtestTrans = fn.dfconcat(df_backtestTrans,df_alltrades)

                df_alltrades.to_csv(btfile, index=False)
                df_backtestResults.to_csv(bsfile, index=False)
        
        return df_alltrades, df_allstat

#31 AUG 2018
#Open each order file for one time only 
#Stored file opened in a list for reuse
def openorderfile(ls_files,filename):

        df_orders = pd.DataFrame()
        flag = False
                
        for i in ls_files:
                if i[0] == filename:
                        #Return from list
                        df_orders = i[1]
                        flag = True

        if flag == False:
                #Read physical file
                df_orders = trade.readOrderFile(filename)
                ls_files.append([filename,df_orders])                

        return ls_files, df_orders
                        

def createorder(symbol, dataset, df_dataset):      

        global df_googleData
        info = mn.GetGoogleData(df_googleData,symbol)

        for rule in ls_rules:
                if rule in patterns:
                        df_b, df_s, df_pl = findpattern(symbol, df_dataset, rule)
                else:
                        df_b, df_s, df_pl = select(symbol,dataset, df_dataset, info,rule)

                bfile = bdir + 'buy-' + str(symbol) + '-' + str(rule) + '.csv'
                globaldf.update([bfile,df_b])
                #df_b.to_csv(bfile,index=False)
                
                sfile = sdir + 'sell-' + str(symbol) + '-' + str(rule) + '.csv'
                globaldf.update([sfile,df_s])
                #df_s.to_csv(sfile,index=False)

                plfile = sdir + 'fixedpl-' + str(symbol) + '-' + str(rule) + '.csv'
                globaldf.update([plfile,df_pl])
                #df_pl.to_csv(plfile,index=False)                
 
        return

#TAKE PROFIT AND STOP LOSS
#13 AUG 2018
def takepl(df_tdata, df_btrans):

        bprice = df_btrans['PRICE'].iloc[0] 
        bdate = df_btrans['DATE'].iloc[0]
        
        sdate = bdate
        
        tpp = bprice * (1 + takeprofit)
        slp = bprice * (1 - stoploss)

        df_profit, df_loss, df_pl, sprice = trade.get_dfstopprofit_dfstoploss(df_tdata, bdate, tpp, slp)        

        if sprice == 0:
                sprice = bprice
                result = 'HOLD'
        elif sprice == tpp:
                result ='PROFIT'
                sdate = df_pl['DATE']
        elif sprice == slp:                
                result = 'LOSS'
                sdate = df_pl['DATE']                
                
        #print result, bdate, sdate, sdate - bdate, bprice, sprice, sprice - bprice
                                
        return df_pl, sprice


def findpattern(symbol,df_tdata,pattern):

        pt = talibw.recg_pattern(df_tdata,pattern)

        buysignal = False
        sellsignal = False

        if pattern in bpatterns:
                buysignal = True

        if pattern in spatterns:
                sellsignal = True

        c = 0

        df_bresults = pd.DataFrame()
        df_sresults = pd.DataFrame()
        df_plresults = pd.DataFrame()

        for p in pt:

                if p <> 0:
                        df_data = df_tdata.iloc[c]
                        price = df_data['CLOSE']
                        quantity = iamt / round(price,2)

                        if buysignal == True:
                                df_btrans = trade.formatOrder(symbol, df_data['DATE'],price,quantity,pattern)
                                df_bresults = fn.dfconcat(df_bresults,df_btrans)                                
                                df_pl, sprice = takepl(df_tdata,df_btrans)                                                    

                                if len(df_pl) > 0:
                                        df_pltrans = trade.formatOrder(symbol, df_pl['DATE'], sprice,-quantity,'FIXEDPL')
                                else:
                                        #NO ACTION TAKEN
                                        df_pltrans = trade.formatOrder(symbol, np.nan,0,0,'FIXEDPL')

                                df_plresults = fn.dfconcat(df_plresults,df_pltrans)                                        
                                        
                        if sellsignal == True:                                
                                df_strans = trade.formatOrder(symbol, df_data['DATE'],price,-quantity,pattern)
                                df_sresults = fn.dfconcat(df_sresults,df_strans)
                        
                
                c = c + 1
        
        return df_bresults, df_sresults, df_plresults


def select(symbol, dataset, df_tdata, info, rule):
        
        l = len(dataset)

        df_bresults = pd.DataFrame()
        df_sresults = pd.DataFrame()
        df_plresults = pd.DataFrame()        
        
        for i in range(3,l):

                buy = False
                sell = False

                data = dataset[i]
                
                try:
                        signal, comment = mn.applyrule(rule,dataset,info,i)
                        price = float(data[4])
                        quantity = iamt / round(price,2)
                        tdate = dt.datetime.strptime(data[0], '%Y-%m-%d').date()
                        
                        if signal == 'BUY' and rule in brules:
                                df_btrans = trade.formatOrder(symbol, tdate,price,quantity,rule)
                                df_bresults = fn.dfconcat(df_bresults,df_btrans)                             
                                
                                df_pl, sprice = takepl(df_tdata,df_btrans)

                                if len(df_pl) > 0:
                                        df_pltrans = trade.formatOrder(symbol, df_pl['DATE'],sprice,-quantity,'FIXEDPL')
                                else:
                                        #NO ACTION TAKEN
                                        df_pltrans = trade.formatOrder(symbol, np.nan,0,0,'FIXEDPL')

                                df_plresults = fn.dfconcat(df_plresults,df_pltrans)                                      

                        if signal == 'SELL' and rule in srules:                           
                                df_strans = trade.formatOrder(symbol, tdate,price,-quantity,rule)
                                df_sresults = fn.dfconcat(df_sresults,df_strans)
                                
                                
                except Exception as e:
                        print str(e)
                        signal = ''
                        comment = ''
  
        return df_bresults, df_sresults, df_plresults



def findResults(df, pctpa):

        mindailyprofitpct = (pctpa*100) / 252
        print 'Looking for trading rules with profit over ' + str(pctpa*100) + '% pa, ' + str(round(mindailyprofitpct,2)) + '% per day'
        #df = df[(df['AVG.RZ.DAYPROFITPCT'] >= mindailyprofitpct) & (df['RZ.W.PCT'] >= 80) & (df['P.TYPE'] == '16') & (df['S.TYPE'] == '16')]
        df = df[(df['AVG.RZ.PROFITPCT1D'] >= mindailyprofitpct) & (df['RZ.W.PCT'] >= 80)]
                
        return df
        
#DIRECT EXECUTION
if __name__ == '__main__':

        filepath = gdir + "gdata.csv"
        global df_googleData
        #df_googleData = pd.read_csv(filepath)
        df_googleData = globaldf.read(filepath)        

        argv = sys.argv    
        if len(argv)>1:
                para = ",".join(argv)
                market = argv[1]
                main()
                print "[" + para + "]"
        else:

                #Parameters:
                #Run symbols if ls_symbols contains values
                markets = ['ASX','HSI']
                ls_symbols = []

                if len(ls_symbols) > 0:
                        test(ls_symbols)
                else:
                        for market in markets:
                                main(market)
        
