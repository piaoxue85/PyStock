import csv
import random
import math
import operator

import os
import sys, getopt

import itertools

from lib import sharedfunctions as fn
from lib import download as dl
from lib import formatter as fileformatter

from lib import knn
from lib import knndata 

from dateutil.relativedelta import relativedelta
from timeit import default_timer as timer
import datetime as dt
from datetime import timedelta

import pandas as pd
import numpy as np

import copy

para  = ''

import glob

def execute(symbol, arg_df_btrans, arg_df_strans, fromDate, toDate):
                
        df_trans = pd.DataFrame()
        df_stat = pd.DataFrame()

        df_btrans = arg_df_btrans.copy()
        df_strans = arg_df_strans.copy()

        headers = df_btrans.columns.values.tolist()
        headers = ['P.' + x for x in headers]                
        df_btrans.columns = [headers]

        headers = df_strans.columns.values.tolist()
        headers = ['S.' + x for x in headers]                
        df_strans.columns = [headers]

        df_btrans.index = range(len(df_btrans.index))
        df_strans.index = range(len(df_strans.index)) 

        df_trans = df_btrans.join(df_strans)
        
        df_trans = df_trans.rename(columns={'P.SYMBOL': 'SYMBOL'})

        df_trans['POSITION'] = np.where(df_trans['S.SHARES'] < 0, 'CLOSED', 'OPEN')
        
        del df_trans['S.SYMBOL']

        df_trans['ONHAND'] = np.where(df_trans['POSITION']=='CLOSED', 0, df_trans['P.SHARES'])
        
        df_pv = getdfpresentval(symbol,toDate)                 

        if len(df_pv) > 0:
                df_trans['VAL.DATE'] = np.where(df_trans['POSITION'] == 'CLOSED',np.NaN,df_pv['DATE'])
                df_trans['PRICE'] = np.where(df_trans['POSITION'] == 'CLOSED',np.NaN, df_pv['CLOSE'])
        else:
                df_trans['VAL.DATE'] = np.where(df_trans['POSITION'] == 'CLOSED',np.NaN, df_trans['P.DATE'])
                df_trans['PRICE'] =  np.where(df_trans['POSITION'] == 'CLOSED',np.NaN, df_trans['P.PRICE'])


        df_trans['VALUE'] = (df_trans['PRICE'] * df_trans['ONHAND'])

        df_trans['HOLDUNTIL'] = np.where(df_trans['POSITION'] == 'CLOSED', df_trans['S.DATE'], df_trans['VAL.DATE'])

        #https://github.com/pydata/xarray/issues/1143
        Ss_timedelta = df_trans['HOLDUNTIL'] - df_trans['P.DATE']
        ls_timedelta = Ss_timedelta.values.astype('timedelta64[d]').tolist()
        for i in range(0, len(ls_timedelta)):
                ls_timedelta[i] = (ls_timedelta[i].days / 1000) + 1                
        df_trans['HOLDDAYS'] = pd.Series(ls_timedelta)

        df_trans['CAPITAL.USED'] = df_trans['HOLDDAYS'] * df_trans['P.CASHONHAND']
        
        #https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.fillna.html
        df_trans.fillna(0)

        df_trans['RZ.PROFIT'] = np.where(df_trans['POSITION'] == 'CLOSED',df_trans['S.CASHONHAND'] + df_trans['P.CASHONHAND'],0)
        df_trans['RZ.PROFITPCT'] = np.where(df_trans['POSITION'] == 'CLOSED',(df_trans['S.CASHONHAND'] + df_trans['P.CASHONHAND']) / abs(df_trans['P.CASHONHAND']),0)
        df_trans['RZ.PROFITPCT'] = df_trans['RZ.PROFITPCT'] * 100
        df_trans['RZ.PROFITPCT1D'] = df_trans['RZ.PROFITPCT'] / df_trans['HOLDDAYS']
        df_trans['RZ.PROFITPCT252D'] = df_trans['RZ.PROFITPCT1D'] * 252        
        df_trans.fillna(0)
        
        df_trans['URZ.PROFIT'] = np.where(df_trans['POSITION'] == 'CLOSED', 0, df_trans['VALUE'] + df_trans['P.CASHONHAND']).astype(np.double).round(2)
        df_trans['URZ.PROFITPCT'] = np.where(df_trans['POSITION'] == 'CLOSED', 0, (df_trans['VALUE'] + df_trans['P.CASHONHAND']) / abs(df_trans['P.CASHONHAND']))
        df_trans['URZ.PROFITPCT'] = df_trans['URZ.PROFITPCT'] * 100
        df_trans['URZ.PROFITPCT1D'] = df_trans['URZ.PROFITPCT'] / df_trans['HOLDDAYS']
        df_trans['URZ.PROFITPCT252D'] = df_trans['URZ.PROFITPCT1D'] * 252    
        df_trans.fillna(0)

        df_trans['TOT.PROFIT'] = df_trans['RZ.PROFIT'] + df_trans['URZ.PROFIT']
        df_trans['TOT.PROFITPCT'] = df_trans['RZ.PROFITPCT'] + df_trans['URZ.PROFITPCT']
        df_trans['TOT.PROFITPCT1D'] = df_trans['RZ.PROFITPCT1D'] + df_trans['URZ.PROFITPCT1D']
        df_trans['TOT.PROFITPCT252D'] = df_trans['TOT.PROFITPCT1D'] * 252
        
        numcols = ['P.CASHONHAND','S.CASHONHAND','RZ.PROFITPCT','URZ.PROFITPCT','TOT.PROFITPCT','ONHAND','VALUE']
        df_trans = rounddf(df_trans, numcols, 2)

        df_stat = analyse(symbol, df_trans)
        df_stat['TOT.DAYS'] = (toDate - fromDate).days

        df_stat['TRADE-TO-TRADE'] = (df_stat['TOT.DAYS'] / df_stat['PURCHASE']).astype(np.double).round(2)

        return df_trans, df_stat

def rounddf(df,cols,dp):

        for col in cols:
                df[col] = df[col].astype(np.double).round(dp)

        return df


def analyse(symbol, arg_df_trans):

        df_trans = arg_df_trans.copy()
        
        df_open = df_trans[(df_trans['POSITION']=='OPEN')]
        df_closed = df_trans[(df_trans['POSITION']=='CLOSED')]
        
        bcount = df_trans[(df_trans['P.SHARES']>0)]['P.DATE'].count()
        scount = df_trans[(df_trans['S.SHARES']<0)]['S.DATE'].count()
        ocount = bcount - scount   #OPEN POSITION
        #symbol = df_trans.iloc[0]['SYMBOL']

        ls_shd = []
        ls_stat = []

        ls_shd.append('SYMBOL')
        ls_stat.append(symbol)

        ls_shd.append('PURCHASE')
        ls_stat.append(bcount)

        ls_shd.append('CLOSE.POS')
        ls_stat.append(scount)

        ls_shd.append('OPEN.POS')
        ls_stat.append(ocount)

        ls_shd.append('SUM.RZ.HOLD')
        sumrzhdays = 0
        if scount > 0:
                sumrzhdays = round(df_closed["HOLDDAYS"].sum() ,0)
        ls_stat.append(sumrzhdays)

        ls_shd.append('SUM.URZ.HOLD')
        sumurzhdays = 0
        if ocount > 0:
                sumurzhdays = round(df_open["HOLDDAYS"].sum() ,0)
        ls_stat.append(sumurzhdays)

        ls_shd.append('SUM.HOLD')
        sumtothdays = round(sumurzhdays + sumrzhdays ,0)
        ls_stat.append(sumtothdays)      

        ls_shd.append('AVG.RZ.HOLD')
        avgrzhdays = 0
        if scount > 0:
                avgrzhdays = round(df_closed["HOLDDAYS"].mean() ,1)
        ls_stat.append(avgrzhdays)

        ls_shd.append('AVG.URZ.HOLD')
        avgurzhdays = 0
        if ocount > 0:
                avgurzhdays = round(df_open["HOLDDAYS"].mean() ,1)
        ls_stat.append(avgurzhdays)

        ls_shd.append('AVG.HOLD')
        avghdays = round(df_trans["HOLDDAYS"].mean() ,1)
        ls_stat.append(avghdays)

        ls_shd.append('RZ.W.COUNT')
        rzwcount = df_trans[(df_trans['RZ.PROFITPCT']>0)]['S.DATE'].count()
        ls_stat.append(rzwcount)

        ls_shd.append('RZ.W.PCT')
        rzwpct = 0
        if scount > 0:
                rzwpct = round((float(rzwcount) / float(scount))*100,2)                
        ls_stat.append(rzwpct)                

        ls_shd.append('URZ.W.COUNT')
        urzwcount = df_trans[(df_trans['URZ.PROFITPCT']>0)]['VAL.DATE'].count()
        ls_stat.append(urzwcount)

        ls_shd.append('URZ.W.PCT')
        urzwpct = 0
        if ocount > 0:
                urzwpct = round((float(urzwcount) / float(ocount))*100,2)                
        ls_stat.append(urzwpct)

        ls_shd.append('W.COUNT')
        wcount = rzwcount + urzwcount
        ls_stat.append(wcount)

        ls_shd.append('W.PCT')
        wpct = 0
        if bcount > 0:
                wpct = round((float(wcount) / float(bcount))*100,2)                
        ls_stat.append(wpct)

        #REALISED

        ls_shd.append('AVG.RZ.PROFITPCT')
        avgrzprofitpct = 0
        if scount > 0:
                avgrzprofitpct = round(df_closed["RZ.PROFITPCT"].mean() ,2)
        ls_stat.append(avgrzprofitpct)

        ls_shd.append('AVG.RZ.PROFITPCT1D')
        avgrzdayprofitpct = 0
        if scount > 0:
                avgrzdayprofitpct = round(df_closed["RZ.PROFITPCT1D"].mean() ,2)
        ls_stat.append(avgrzdayprofitpct)

        ls_shd.append('AVG.RZ.PROFITPCT252D')
        avgrzprofitpct252d = avgrzdayprofitpct * 252
        ls_stat.append(avgrzprofitpct252d)       
        
        ls_shd.append('SUM.RZ.PROFITPCT')
        sumrzprofitpct = 0
        if scount > 0:
                sumrzprofitpct = round(df_closed["RZ.PROFITPCT"].sum() ,2)
        ls_stat.append(sumrzprofitpct)
        
        ls_shd.append('SUM.RZ.PROFIT')
        sumrzprofit = 0
        if scount > 0:
                sumrzprofit = round(df_closed["RZ.PROFIT"].sum(),2)
        ls_stat.append(sumrzprofit)

        #UNREALISED
        ls_shd.append('AVG.URZ.PROFITPCT')
        avgurzprofitpct = 0
        if ocount > 0:
                avgurzprofitpct = round(df_open["URZ.PROFITPCT"].mean() ,2)
        ls_stat.append(avgurzprofitpct)

        ls_shd.append('AVG.URZ.PROFITPCT1D')
        avgurzdayprofitpct = 0
        if ocount > 0:        
                avgurzdayprofitpct = round(df_open["URZ.PROFITPCT1D"].mean() ,2)
        ls_stat.append(avgurzdayprofitpct)

        ls_shd.append('AVG.URZ.PROFITPCT252D')
        avgurzprofitpct252d = avgurzdayprofitpct * 252
        ls_stat.append(avgurzprofitpct252d)        
        

        ls_shd.append('SUM.URZ.PROFITPCT')
        sumurzprofitpct  = 0
        if ocount > 0:        
                sumurzprofitpct = round(df_open["URZ.PROFITPCT"].sum() ,2)
        ls_stat.append(sumurzprofitpct)
        
        ls_shd.append('SUM.URZ.PROFIT')
        sumurzprofit = 0
        if ocount > 0: 
                sumurzprofit = round(df_open["URZ.PROFIT"].sum(),2)
        ls_stat.append(sumurzprofit)        

        #TOTAL
        ls_shd.append('INVESTED')       
        suminvestedamt = round(-df_trans["P.CASHONHAND"].sum(),2)
        ls_stat.append(suminvestedamt)

        ls_shd.append('CAPITAL.USED')       
        sumcapitalusedamt = round(df_trans["CAPITAL.USED"].sum(),2)
        ls_stat.append(sumcapitalusedamt)        

        ls_shd.append('PROFIT')       
        sumprofit = round(sumrzprofit + sumurzprofit,4)
        ls_stat.append(sumprofit)

        ls_shd.append('PROFITPCT')
        profitpct = 0
        if suminvestedamt <> 0:
                profitpct = round((sumprofit/ suminvestedamt) * 100,2)
        ls_stat.append(profitpct)                

        ls_shd.append('AVG.PROFITPCT1D')
        avgdayprofitpct = 0
        if bcount > 0:
                avgdayprofitpct = round(((avgurzdayprofitpct * ocount) + (avgrzdayprofitpct * scount))/bcount,4)
        ls_stat.append(avgdayprofitpct)                

        ls_shd.append('AVG.PROFITPCT252D')
        avgdayprofitpct252d = avgdayprofitpct * 252
        ls_stat.append(avgdayprofitpct252d)  
        
        df_stat = pd.DataFrame([ls_stat], columns=ls_shd)

        return df_stat
                        

def pair(df_trans, sDate, eDate):
        
        l = len(df_trans)

        #PREPARE 2 LISTS
        #A BUY LIST AND A SELL LIST
        blist = []
        slist = []

        #BUY AND SELL PAIRED TRANSACTIONS
        ls_btrans = []
        ls_strans = []
        ls_transhd = []

        dt_timeofday = dt.timedelta(hours=16)
        dt_today = dt.datetime.now().date()
        dt_end = dt.datetime(dt_today.year, dt_today.month, dt_today.day)
        dt_date = dt.datetime.now() - dt.timedelta(hours=24)                

        beginDate = sDate - dt.timedelta(days=960)
        endDate = dt_end.date()
              
        #FOR EACH SYMBOL
        #       FOR EACH BUY TRANSACTION
        #               LOOK FOR SELL TRANSACTION
        #               SPLIT BUY TRANSACTION IF SELL TRANSACTION AMOUNT IS SMALLER THAN BUY TRANSACTION
        for i in range(0, l):
                
                symbol = df_trans.iloc[i]['SYMBOL']
                shares = df_trans.iloc[i]['SHARES']
                price = df_trans.iloc[i]['PRICE']
                amount = df_trans.iloc[i]['CASHONHAND']
                tdate = df_trans.iloc[i]['DATE']
              
                try:
                    shares = float(str(shares).replace(",", ""))
                except:
                    shares = 0

                try:
                    price = float(str(price).replace(",", ""))
                except:
                    price = 0

                try:
                    amount = float(str(amount).replace(",",""))
                except:
                    amount = 0

                try:    #WITH COMMISSION INCLUDED
                    aprice = round(abs(amount / shares),4)
                except:
                    aprice = 0

                try:
                        tdate = dt.datetime.strptime(tdate, '%Y-%m-%d').date()
                        ls_transhd = ['SYMBOL','DATE','SHARES','PRICE','CASHONHAND']
                        trans = [symbol,tdate,shares,aprice,amount]

                        if shares > 0:
                                if tdate >= sDate and tdate < eDate:
                                        blist.append(trans)
                        #SELL
                        elif shares <0:
                                slist.append(trans)

                except Exception as e:
                        
                        print symbol + ' - ' + str(e)

        p = len(blist)
        q = len(slist)

        j = 0
        c = 0   #sell list cursor

        if p > 0:
                bdate = blist[0][1]                
                
        for i in range(0,p):

                s = 0   #SHARES

                if q > 0:  #NUMBER OF SELL
                        s = slist[c][2]

                if s == 0 and q > c + 1:
                        s = slist[c+1][2]
                
                while blist[i][2] <> 0 and s <> 0:

                        bdate = blist[i][1]

                        for j in range(0,q):

                                sdate = slist[j][1]
                                
                                if blist[i][2] > 0 and slist[j][2] < 0 and sdate >= bdate:
                                        rm = blist[i][2] + slist[j][2]
                                        
                                        if rm > 0: #BUY > SELL
                                                sqty = -slist[j][2]
                                                slist[j][2] = 0
                                                blist[i][2] = rm
                                                
                                        elif rm < 0: #SELL > BUY                                              
                                                sqty = -blist[i][2]
                                                slist[j][2] = rm
                                                blist[i][2] = 0
                                                
                                        elif rm == 0: #BUY = SELL                                                
                                                sqty = slist[j][2]
                                                slist[j][2] = 0
                                                blist[i][2] = 0

                                        btrans = copy.copy(blist[i])
                                        btrans[2] = abs(sqty)

                                        strans = copy.copy(slist[j])
                                        strans[2] = -abs(sqty)                                        

                                        bamt = blist[i][3] * abs(sqty)					
                                        samt = slist[j][3] * abs(sqty)

                                        btrans[-1] = -abs(bamt)
                                        strans[-1] = abs(samt)

                                        ls_btrans.append(btrans)
                                        ls_strans.append(strans)

                                        s = slist[j][2]                                                                     
                                
                                s = 0
                                c = j

                #NO MATCHING SELL RECORD,
                if blist[i][2] > 0:

                        bdate = blist[i][1]
                        sdate = bdate
                        sqty = blist[i][2]
                        bamt = blist[i][3] * abs(sqty)

                        btrans = copy.copy(blist[i])
                        btrans[2] = abs(sqty)
                        btrans[-1] = -abs(bamt)

                        ls_btrans.append(btrans)

        #ADD COLUMN HEADER FOR DATAFRAME
        ls_btrans.insert(0,ls_transhd)
        ls_strans.insert(0,ls_transhd)

        df_btrans = knndata.getdfdata(ls_btrans)
        df_strans = knndata.getdfdata(ls_strans)
        
        return df_btrans, df_strans

def calc_annualised_pl(bdate, bamt, sdate, samt):

        hdays = (sdate - bdate).days + 1
        p = samt - bamt
        pct = p/bamt/hdays*365
        pct = round(pct * 100,2)        
        return hdays, pct


def get_dfmindate_dfmaxdate(df_tdata, bdate):

        try:
                df_filtered = df_tdata[(df_tdata.DATE >= bdate)]

                df_mindate= df_filtered.loc[df_filtered['LOW'].idxmin()]                
                df_maxdate= df_filtered.loc[df_filtered['HIGH'].idxmax()]
        except:
                df_mindate = df_tdata.iloc[-1]
                df_maxdate= df_tdata.iloc[-1]

        return df_mindate, df_maxdate

def get_dfstopprofit_dfstoploss(df_tdata, bdate, tpp, slp):
#bdate DATE OF BUY ORDER
#tpp TAKE PROFIR PRICE
#slp STOP LOSS PRICE
        
        df_profit = pd.DataFrame()      #TAKE PROFIT DATE
        df_loss = pd.DataFrame()        #STOP LOSS DATE
        df_pl = pd.DataFrame()          #ACTUAL DATE, EITHER TAKE PROFIT OR STOP LOSS
        sprice = 0                      #SELL PRICE

        try:
                df_filtered = df_tdata.loc[(df_tdata.DATE > bdate)]

                if tpp > 0:
                        df_profit= df_filtered.loc[(df_tdata.HIGH >= tpp)]

                if slp > 0:
                        df_loss = df_filtered.loc[(df_tdata.LOW <= slp)]

                if len(df_profit) > 0:
                        df_profit = df_profit.iloc[0]
                        df_pl = df_profit
                        sprice = tpp                        

                if len(df_loss) > 0:
                        df_loss = df_loss.iloc[0]
                        df_pl = df_loss
                        sprice = slp                        

                if len(df_profit) > 0 and len(df_loss) > 0:
                        #TAKE PROFIT
                        if df_loss['DATE'] >= df_profit['DATE'] and df_profit['HIGH'] >= tpp:
                                df_pl = df_profit
                                sprice = tpp

                        #STOP LOSS
                        if df_profit['DATE'] >= df_loss['DATE']  and slp >= df_loss['LOW']:
                                df_pl = df_loss
                                sprice = slp

        except Exception as e:
                print "get_dfstopprofit_dfstoploss " + str(e)
                df_profit = pd.DataFrame()
                df_loss = pd.DataFrame()
                df_pl = pd.DataFrame()


        return df_profit, df_loss, df_pl, sprice

        
def run(sDate, eDate, orderfile, outputid,usecache=False):

        df_trans = pd.read_csv(orderfile)
        stats = []
        ls1 = df_trans.SYMBOL.unique()

        print orderfile

        df_results = pd.DataFrame()
        df_stats = pd.DataFrame()
        
        for sym in ls1:

                fsym = str(sym)
                fsym = fn.symbolFormatter(fsym)

                print "Trading - " + fsym
                
                df_symboltrans = df_trans[(df_trans.SYMBOL == sym)]
                df_btrans, df_strans = pair(df_symboltrans,sDate,eDate)

                if len(df_btrans) > 0:
                        df_result, df_stat = execute(sym, df_btrans, df_strans, sDate, eDate)
                        df_stats = fn.dfconcat(df_stats,df_stat)
                        df_results = fn.dfconcat(df_results,df_result)
                
        fpath = 'results\\transanalysis\\stat-' + outputid + '.csv'
        df_stats.to_csv(fpath,index=False)

        fpath = 'results\\transanalysis\\trans-' + outputid + '.csv'
        df_results.to_csv(fpath,index=False)
        
        return df_results, df_stats


def getdfpresentval(symbol,vDate):
        #Present value for calculating unrealised PL
        df_pv = pd.DataFrame()
        try:
                fsym = fn.symbolFormatter(symbol)
                df_pv = knndata.getRawData(fsym)
                df_pv = df_pv[(df_pv.DATE <= vDate)].iloc[-1]
        except:
                df_pv = pd.DataFrame()

        return df_pv

#TO BE REMOVED - 3 SEP 2018
def writetransactionlist_toberemoved(dtlist, outputfile):

        hheaders = ['SYMBOL','DATE','SHARES','MARKED PRICE','NET PRICE','AMOUNT','R.TOTAL']

        text_file = open(outputfile, "w")

        dtlist = sorted(dtlist, key=lambda x: dt.datetime.strptime(x[1], '%m/%d/%Y'))

        rtotal = 0
        dtlist.insert(0,hheaders)

        for trans in dtlist:
                str1 = ','.join(str(e) for e in trans)
                if trans[-1] <> hheaders[-1]:   #EXCLUDE HEADER
                        rtotal = rtotal + float(trans[-1])
                        str1 = str1 + ',' + str(round(rtotal,2))
                text_file.write(str1 + "\n")

        text_file.close()

        return

def writeExcel():

        writer = pd.ExcelWriter('simple-report.xlsx', engine='xlsxwriter')
        df.to_excel(writer, index=False)
        df_footer.to_excel(writer, startrow=6, index=False)
        writer.save()

def main():

        sDate = '07/01/2010'
        sDate = dt.datetime.strptime(sDate, '%m/%d/%Y').date()

        eDate = '12/31/2018'
        eDate = dt.datetime.strptime(eDate, '%m/%d/%Y').date()

        directory = "\\python\\data\\google\\"
        filepath = directory + "transactions.csv"

        dl.transactions()

        outputid = str(eDate.year) + str(eDate.month).zfill(2)
        
        run(sDate,eDate, filepath, outputid,False)
                  
        print "ENDED -" + dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		
def readOrderFile(filepath):
        df = formatOrder()
        try:
                df = pd.read_csv(filepath,dtype={'SYMBOL': object})
                df['DATE'] =  pd.to_datetime(df['DATE']).apply(lambda x: x.date())
        except Exception as e:
                print "Cannot open " + filepath
        
        return df

def formatOrder(symbol='',odate='',price=0,quantity=0,transtype=''):
        
        colheader = "SYMBOL"
        data = str(symbol)

        colheader = colheader + ",DATE" 
        try:
                fdate = odate.strftime('%Y-%m-%d')
        except:
                fdate = ''

        data = data + "," + fdate

        colheader = colheader + ",SHARES"
        data = data + "," + str(round(quantity,2))
        
        colheader = colheader + ",PRICE"
        price = round(price,2)
        data = data + "," + str(price)
        
        colheader = colheader + ",COMMISSION"
        commission = abs(price * quantity) * 0.0031
        data = data + "," + str(commission)
                      
        colheader = colheader + ",CASHONHAND"
        amount = round((-quantity * price) - commission,2)
        data = data + "," + str(amount)

##        colheader = colheader + ",TURNOVER"
##        data = data + "," + str(abs(amount))
##                      
##        colheader = colheader + ",PERIOD"
##        period = odate.strftime("%Y%m")
##        data = data + "," + str(period)
                                            
        colheader = colheader + ",TYPE"
        data = data + "," + str(transtype)

        ls_colheader = colheader.split(",")
        ls_data = [data.split(",")]
        
        if fdate <> '':
                df_ret = pd.DataFrame(ls_data,columns=ls_colheader,dtype=float)
                df_ret['DATE'] =  pd.to_datetime(df_ret['DATE']).apply(lambda x: x.date())        
        else:
                df_ret = pd.DataFrame(columns=ls_colheader,dtype=float)  

        return df_ret
        
if __name__ == '__main__':
    
    os.system('cls')
    os.system('@echo Loading data...')
    main()
   

