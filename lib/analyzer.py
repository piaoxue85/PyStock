
import math

def pricedist(ls_data, spreadcount, days):

    headers = ls_data[0]
	
    ls_count = []  
    ls_price = []
 
    for i in range(spreadcount):
        ls_count.append(0)

    low = ls_data[-1][headers.index("LOW")]
    high = ls_data[-1][headers.index("HIGH")]
    close = ls_data[-1][headers.index("CLOSE")]

    for i in range(-days, 0):
        if ls_data[i][headers.index("HIGH")] > high:
            high = ls_data[i][headers.index("HIGH")]
        if  ls_data[i][headers.index("LOW")] < low:
            low = ls_data[i][headers.index("LOW")]
            
    spread = (high - low) / (spreadcount-1)

    for i in range(0, spreadcount):
        ls_price.append(round(low + spread*i,2))

    for i in range(-days, 0):
        j = 0
        for p in ls_price:
            if ls_data[i][headers.index("HIGH")] >= p and ls_data[i][headers.index("LOW")] <= p:
                ls_count[j] =  ls_count[j] + 1
            j = j + 1
            
    #position of current price
    position = math.floor((close - low) / spread)

    #distribution in percentage
    ls_dist = []
    t = sum(ls_count)
    pct = 0.00
    for c in ls_count:
        pct = float(c) / float(t) * 100
        ls_dist.append(pct)
        
    return spread, high, low, ls_price, ls_count, ls_dist, position
