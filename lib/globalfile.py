
#16 SEP 2018
#A MODULE FOR KEEPING FILES IN A GLOBAL VARIABLE

global GLOBAL_LS_FILE

GLOBAL_LS_FILE = []

#f = [filepath,lines]
def update(f,pfile=False):

    global GLOBAL_LS_FILE

    inList = False

    c = 0
    
    for i in GLOBAL_LS_FILE:

        if i[0] == f[0]:            
            GLOBAL_LS_FILE[c] = f
            inList = True

        c = c + 1
        
    if inList == False:
        GLOBAL_LS_FILE.append(f)

    if pfile== True:
        writefile(f)       

    return f

def read(filepath, pfile=True):

    global GLOBAL_LS_FILE

    ret = []
    inCache = False
    
    for i in GLOBAL_LS_FILE:
        if i[0] == filepath:
                ret = i[1]
                inCache = True

    if inCache == False and pfile == True:
        try:
            print 'Read from file'
            f = open(filepath)
            ret = f.readlines()
            f.close()
            
        except Exception as e:
            print e
            pass

    return ret

def writefile(f, mode='w'):

    wf = open(f[0],mode)
    wf.write("".join(f[1]))
    wf.close()

    return f

def save(filepath,mode="w"):

    lines = read(filepath,False)
    print 'Saving ' + filepath
    writefile([filepath,lines])

    return

def saveall(mode="w"):

    global GLOBAL_LS_FILE
    
    for i in GLOBAL_LS_FILE:
        f = open(i[0],mode)
        f.write(i[1])
        f.close()

    return

def clear():

    global GLOBAL_LS_FILE

    GLOBAL_LS_FILE = []

    return

    
    
