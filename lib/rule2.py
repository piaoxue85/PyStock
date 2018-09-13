import datetime as dt
import matplotlib.pyplot as plt

import math
import copy
import calendar

import sharedfunctions as fn

from collections import OrderedDict

def apply(data, idx, day, r, ob, os):
    #ob MONTHLY OVERBOUGHT COUNT
    #os MONTHLY OVERSOLD COUNT

    headers = data[0]

    colName =  "RSI" + str(day)
    col = headers.index(colName)

    rsi3 = data[idx-2][col]
    rsi2 = data[idx-1][col]
    rsi1 = data[idx][col]

    rsitrend = fn.trend(data,idx, col)

    signal = ""
    comment = ""
    comment2 = ""

    
    if rsi2 >= 70 and rsi1 >= 70:
        if rsitrend == 1:
            signal = "SELL"
            comment = colName + " (" + str(round(rsi2,2)) + ") WAS OVERBOUGHT BUT IS NOW WEAKENING (" + str(round(rsi1,2)) + ")."
        elif rsitrend == 4:
            signal = "SELL"
            comment =colName + " (" + str(round(rsi2,2)) + ") WAS OVERBOUGHT BUT IS NOW IN DOWNTREND(" + str(round(rsi1,2)) + ")."
        elif rsitrend == 2:
            signal = "HOLD, SET STOP LIMIT"
            comment = colName + " (" + str(round(rsi2,2)) + ") WAS OVERBOUGHT AND IS STILL STRENGTHENING (" + str(round(rsi1,2)) + ")."
        elif rsitrend == 3:
            signal = "HOLD, SET STOP LIMIT"
            comment = colName + " (" + str(round(rsi2,2)) + ") WAS OVERBOUGHT AND IS STILL IN UPTREND (" + str(round(rsi1,2)) + ")."
        elif rsitrend == 5:
            signal = "HOLD, SET STOP LIMIT"
            comment = "KEEP A CLOSE EYE. " +  colName + " (" + str(round(rsi1,2)) + ") IS OVERBOUGHT BUT IS STOPPED RISING."  

    if rsi2 >= 70 and rsi1 < 70:
            signal = "SELL"
            comment = colName + " (" + str(round(rsi2,2)) + ") WAS OVERBOUGHT BUT IS NOW WEAKENING (" + str(round(rsi1,2)) + ")."            

    if rsi2 < 70 and rsi1 >= 70:
     
        if rsitrend == 2 or rsitrend == 3:
            signal = "--"
            comment = colName + " (" + str(round(rsi1,2)) + ") IS OVERBOUGHT."        

    if rsi2 <= 30 and rsi1 >= 30:
        signal = "BUY"
        comment = colName + " (" + str(round(rsi2,2)) + ") WAS OVERSOLD BUT IS STRENGTHENING (" + str(round(rsi1,2)) + ")."
        
    if rsi2 <= 30 and rsi1 <=30:
        if rsitrend == 2:
            signal = "BUY"
            comment = colName + " KEEP A CLOSE EYE. RSI(" + str(round(rsi2,2)) + ") IS OVERSOLD BUT IS STRENGTHENING (" + str(round(rsi1,2)) + ")." 
        elif rsitrend == 3:
            signal = "BUY"
            comment = colName + " (" + str(round(rsi2,2)) + ") IS OVERSOLD AND IS STRENGTHENING (" + str(round(rsi1,2)) + ")." 
        elif rsitrend == 1 or rsitrend == 4:
            signal = "HOLD"
            comment = colName + " (" + str(round(rsi2,2)) + ") IS OVERSOLD AND IS STILL WEAKENING (" + str(round(rsi1,2)) + ")."
        elif rsitrend == 5:
            signal = "BUY"
            comment = "KEEP A CLOSE EYE. RSI (" + str(round(rsi1,2)) + " IS OVERSOLD AND IS STOPPED DROPPING."         

    if rsi2 > 30 and rsi1 <= 30:
     
        if rsitrend == 1 or rsitrend == 4:
            signal = "--"
            comment = colName + " (" + str(round(rsi1,2)) + ") IS OVERSOLD"     

    if comment == "":
        if rsitrend== 2 or rsitrend ==3:
            signal = "HOLD"
            comment = colName + " (" + str(round(rsi1,2)) + ") IS STRENGTHENING"
        elif rsitrend== 1 or rsitrend ==4:
            signal = "--"
            comment = colName + " (" + str(round(rsi1,2)) + ") IS WEAKENING"

    if len(r.index) == 1:
        monthName = calendar.month_name[r.iloc[0]['MONTH']].upper()
        if ob == 0:
            if rsi1 >= 70:
                comment2 = "NO OVERBOUGHT SIGNAL RECORDED IN " + monthName + " EVER IN HISTORY"
        if os == 0:
            if rsi1 <= 30:
                comment2 = "NO OVERSOLD SIGNAL RECORDED IN " + monthName + " EVER IN HISTORY"
        if ob > 0 and os > 0:
            if rsi1 >= 70 or rsi1 <= 30:
                comment2 = "OB/OS RATIO IN " + monthName + " IS " + str("%.2f" % round(ob,2)) + "/" + str("%.2f" % round(os,2))

    if len(comment2) > 0:
        comment = comment + " " + comment2
    
    return signal, comment

