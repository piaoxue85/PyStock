import datetime as dt
import sharedfunctions as fn
from collections import OrderedDict


def apply(data, idx):

    headers = data[0]

    col = headers.index("MACD[12+ 26+ 9]+")
    vol3 = data[idx-2][col]
    vol2 = data[idx-1][col]
    vol1 = data[idx][col]


    signal  = ""
    comment = ""

    comment = "MACD IS " + str(vol1)

 
    return signal, comment


