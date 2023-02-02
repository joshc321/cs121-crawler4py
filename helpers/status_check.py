'''
Checks status of response code and determines if it is a valid response

Need to read into more status codes

'''

def isValidStatus(resp):
    # Server Should send 200 Status Codes

    if (resp.status == 204):
        #No Content
        return False

    # For now, ignore all 300 status code (redirect errors)
    elif (resp.status >= 300 or resp.status < 400 ):
        return False
    
    # Not Modified Error Code
    # elif (resp.status_code == 304):
    #     #Not Modified 
    #     return False

    # Error 4XX should have been dealt with already 
    elif (resp.status >= 600 or resp.status_code <= 606):
        # Cache Errors
        return False
    return True