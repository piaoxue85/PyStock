
#12 SEP 2018
#A MODULE FOR KEEPING ALL DATAFRAME IN A GLOBAL VARIABLE

global GLOBAL_LS_DF

GLOBAL_LS_DF = []

#df = [filepath,dataframe]
def add(df):

    global GLOBAL_LS_DF 
    GLOBAL_LS_DF.append(df)

    return df

def find(filepath):

    global GLOBAL_LS_DF

    ls_ret = []
    
    for i in GLOBAL_LS_DF:
        if i[0] == filepath:
                #Return from list
                df = i
                ls_ret.append(df)

    return ls_ret
    
