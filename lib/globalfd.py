
#12 SEP 2018
#A MODULE FOR KEEPING ALL FIELD DESCRIPTIONS IN A GLOBAL VARIABLE

global GLOBAL_LS_FIELDESC

GLOBAL_LS_FIELDESC = []

#fielddesc = [fieldname,description]
def add(fielddesc):

    global GLOBAL_LS_FIELDESC
    GLOBAL_LS_FIELDESC.append(fielddesc)

    return fielddesc

def find(fieldname):

    global GLOBAL_LS_FIELDESC

    ls_ret = []
    
    for i in GLOBAL_LS_FIELDESC:
        if i[0] == fieldname:
                #Return from list
                fielddesc = i
                ls_ret.append(fielddesc)

    return ls_ret
    
