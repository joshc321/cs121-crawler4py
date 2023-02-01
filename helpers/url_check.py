'''
url_check.py

notes:
    need to make implimentation decision on whether the
    '.' at the beginning of url is manditory
'''
import re

def is_valid_domain(parsedurl):
    '''
        determines if given parsedurl object's domain is valid matching
        *.(ics|cs|informatics|stats).uci.edu/*

        @arg parsedurl urllib.parse.urlparse
        @return bool
    '''

    return bool(re.search(r'\.(ics|cs|informatics|stat)\.uci\.edu$', parsedurl.netloc))


