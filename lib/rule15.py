def apply(data, row, pprice, stopprofit=1.03, stoploss = 0.97):

    headers = data[0]
    
    col = headers.index("CLOSE")
    close = data[row][col]  #Latest price

    profit = pprice / close

    signal = ""
    comment = ""    

    if profit >= stopprofit:
        signal = "SELL"
        comment = "TAKE PROFIT"

    if profit <= stoploss:
        signal = "SELL"
        comment = "STOP LOSS"
		
    return signal, comment


