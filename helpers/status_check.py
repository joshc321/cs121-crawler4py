'''
Checks status of response code and determines if it is a valid response


Implement this function into extract_next_link function

'''

def is_valid_status(resp):
    # Server Should send 200 Status Codes
    # 1XX Error Codes information reqests
    # 204 Error Codes No Content
    # 3XX Redirects (Blank Pages)
    # 4XX Client Error
    # 5XX Server Error
    # 600-606 Cache Error
    if ((resp.status >= 200) and resp.status != 204 ):
        return True
    return False