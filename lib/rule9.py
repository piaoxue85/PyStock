import datetime as dt
import sharedfunctions as fn
from collections import OrderedDict


def apply(data, idx):

    headers = data[0]

    col = headers.index("VOLUME")
    vol3 = data[idx-2][col]
    vol2 = data[idx-1][col]
    vol1 = data[idx][col]
    vt = fn.trend(data, idx, col)
        
    col = headers.index("CLOSE")
    close3 = data[idx-2][col]
    close2 = data[idx-1][col]
    close1 = data[idx][col]
    ct = fn.trend(data, idx, col)


    signal  = ""
    comment = ""

    volumeChg = (float(vol1) - vol2) / vol2

    if volumeChg > 0.4:
            signal = "---"
            comment = "VOLUME INCREASED BY " + str("%.1f" % round(volumeChg * 100,2)) + '%'
            
    if volumeChg < -0.4:
            signal = "---"
            comment = "VOLUME DECREASED BY " + str("%.1f" % round(volumeChg * 100,2)) + '%'

    
#Simply stated, volume should expand or increase in the direction of the major trend.
#In a major uptrend, volume would then increase as prices move higher,and diminish as prices fall.
#In a downtrend, volume should increase as prices drop and diminish as they rally.

    if vt == ct:
        if vt == 3:
            signal = "BUY"
            comment = "UPTREND." + comment + " PRICE RALLIES AS VOLUME INCREASES"
        if vt ==4:
            signal = "SELL"            
            comment = "DOWNTREND." + comment + " SEEKING SUPPPORT PRICE"
            
    if vt <> ct:
        if vt == 3 and ct ==4:
            signal = "BUY"                   
            comment = "" + comment +  " CLOSE TO SUPPORT PRICE. LOOK FOR BUY SIGNAL"
        elif vt ==4 and ct ==3:
            signal = "SELL"                
            comment = "" + comment +  " CLOSE TO RESISTANT PRICE. LOOK FOR SELL SIGNAL"
 
    return signal, comment


