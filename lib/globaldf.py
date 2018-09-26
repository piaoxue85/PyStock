
import pandas

#12 SEP 2018
#A MODULE FOR KEEPING ALL DATAFRAME IN A GLOBAL VARIABLE

global GLOBAL_LS_DF

GLOBAL_LS_DF = []

#df = [filepath,dataframe]
def update(df):

    global GLOBAL_LS_DF

    #df_ret = read(df[0],False)

    inList = False

    c = 0
    
    for i in GLOBAL_LS_DF:

        if i[0] == df[0]:       
            GLOBAL_LS_DF[c] = df
            inList = True

        c = c + 1
        
    if inList == False:
        GLOBAL_LS_DF.append(df)


    return df

def read(filepath, pfile=True):

    global GLOBAL_LS_DF

    df_ret = pandas.DataFrame()
    inCache = False
    
    for i in GLOBAL_LS_DF:
        if i[0] == filepath:
                df_ret = i[1]
                inCache = True

    if inCache == False and pfile == True:
        try:
            df_ret = pandas.read_csv(filepath)
            GLOBAL_LS_DF.append([filepath,df_ret])

        except Exception as e:
            print e
            pass


    return df_ret

def to_csv(filepath):

    print 'to_csv ' + filepath
    df = read(filepath,False)
    df.to_csv(filepath,index=False)        

    return

def all_to_csv():

    global GLOBAL_LS_DF
    
    for i in GLOBAL_LS_DF:
        i[1].to_csv(i[0], index=False)

    return

def clear():

    global GLOBAL_LS_DF

    GLOBAL_LS_DF = []

    return

    
    
