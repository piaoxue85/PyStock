
#19 SEP 2018
#Find value in a list by prefix
def findByPrefix(ls, ls_prefix):

    ls_rets = []

    for item in ls:
            for prefix in ls_prefix:
                    l = len(prefix)
                    if item[0:l] == prefix:
                            ls_rets.append(item)

    return ls_rets
  
