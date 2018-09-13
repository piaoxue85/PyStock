import datetime as dt


def isTradingHour():

    days = [0,1,2,3,4,5]
    ohr = 9
    ehr = 16
    
    retVal = -1
    dt_now = dt.datetime.now()
    if dt_now.weekday() in days:
        if dt_now.hour >= ohr and dt_now.hour <= ehr:
            retVal = 1
            
    return retVal



if __name__ == '__main__':
    print isTradingHour()

