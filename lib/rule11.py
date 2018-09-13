import datetime as dt
import sharedfunctions as fn
from collections import OrderedDict


def apply(data, idx):

    headers = data[0]

    col = headers.index("TREND")
    val = int(data[idx][col])

    col1 = headers.index("TRENDCHG")
    val1 = int(data[idx][col])

    comment = ""
    signal = ""

    if val >=2:
        comment = str(val) + " DAYS RALLIES IN A ROW (" + str(val1) + ")"
    elif val <= -2:
        comment = str(abs(val)) + " DAYS DECLINE IN A ROW (" + str(val1) + ")"

    return signal, comment


