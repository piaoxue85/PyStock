import datetime as dt
import sharedfunctions as fn
from collections import OrderedDict

#ADR

def apply(data, info):

    t = str(info.iloc[0]['TAG'])
    signal = ""
    comment = ""

    if t.find("#ADR") > -1:
            headers = data[0]
            col = headers.index("CLOSECHG")
            v = data[-1][col]
            if v > 1:
                signal = "BUY"
                comment = "PLACE HSI MORNING AUCTION ORDER BEFORE 0915. MATCH THE HIGHEST BID."

    return signal, comment




