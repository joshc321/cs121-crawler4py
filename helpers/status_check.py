'''
Checks status of response code and determines if it is a valid response
'''

def isValidStatus(resp):
    # needs to be implimented

    if (resp.status_code == 204):
        #No Content
        return False
    # elif (resp.status_code == 304):
    #     #Not Modified 
    #     return False
    elif (resp.status_code >= 600 or resp.status_code <= 606):
        #Cache Errors
        return False
    return True