'''
url_check.py

notes:
    need to make implimentation decision on whether the
    '.' at the beginning of url is manditory
'''
import re

VALID_URL_PATTERN = re.compile(r'(?P<subdomain>.*)?\.(ics|cs|informatics|stat)\.uci\.edu')

def is_valid_domain(parsedurl):
    '''
        determines if given parsedurl object's domain is valid matching
        *.(ics|cs|informatics|stats).uci.edu/*

        @arg parsedurl urllib.parse.urlparse
        @return bool
    '''

    regex_match = re.search(VALID_URL_PATTERN, parsedurl.netloc)
    return bool(regex_match)

def get_subdomain(parsedurl):
    '''
        Returns the subdomain from the ics.uci.edu domain, given
        the regex pattern and a urlparse object

        @arg parsedurl urllib.parse.urlparse
        @return str
    '''
    regex_match = re.search(VALID_URL_PATTERN, parsedurl.netloc)
    
    if regex_match:
        return regex_match.group('subdomain')
    
    return ''

if __name__ == '__main__':
    import urllib.parse

    parsed = urllib.parse.urlparse('https://one.two.ics.uci.edu')
    print(is_valid_domain(parsed))
    print(get_subdomain(parsed))
