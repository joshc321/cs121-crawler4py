'''
Checks status of response code and determines if it is a valid response
'''

def isValidStatus(status):
    # needs to be implimented

    if (status == 204):
        #No Content
        return False
    # elif (resp.status_code == 304):
    #     #Not Modified 
    #     return False
    elif (status >= 600 and status <= 606):
        #Cache Errors
        return False
    return True