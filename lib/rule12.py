import datetime as dt
import sharedfunctions as fn
from collections import OrderedDict


def apply(r, dt_today):

    rowText = ""

    signal = ""
    comment = ""

    if len(r.index) == 1:
        
            rm = r.iloc[0]['RESULTMONTHS']
            nrd = fn.readDate(r.iloc[0]['NEXTRESULTDATE'])
            rd = fn.readDate(r.iloc[0]['RECORDDATE'])
            d = r.iloc[0]['DIVIDENDS']
            
            try:
                delta1 = nrd - dt_today # > 0
                delta2 = rd - nrd # > 0
                delta3 = rd - dt_today
            except:
                delta1 = dt.timedelta(days=-365)
                delta2 = dt.timedelta(days=-365)
                delta3 = dt.timedelta(days=-365)

            if delta1.days > 0 and delta1.days < 60:        
                    comment = comment + str(delta1.days) + " DAYS TO RESULT ANNOUNCEMENT PLAN TRADING"
            elif delta1.days == 0:
                    comment = comment + "TODAY IS RESULT ANNOUNCEMENT DATE "
            elif delta1.days == 1:
                    comment = comment + "TOMORROW IS RESULT ANNOUNCEMENT DATE "
            elif delta1.days < -1 :     #RESULT DATE PASSED
                if delta3.days < 0 and delta2.days > 0:     #RECORD DATE PASSED
                    try:                #NEXT MONTH IS RESULT ANOUNCEMENT
                        ls_rm = rm.split(',')
                        i = ls_rm.index(str(dt_today.month+1))
                        comment = comment + "CHECK RESULT DATE AND PLAN TRADING"
                    except:
                        i = -1

            if delta3.days == 0:
                comment = comment + "TODAY IS DIVIDEND RECORD DATE "
            elif delta3.days > 0 and delta3.days < 14:
                comment = comment + str(delta3.days) + " DAYS TO DIVIDEND RECORD DATE "


    return signal, comment




