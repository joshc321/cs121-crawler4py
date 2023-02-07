'''
url_check.py

notes:
    need to make implimentation decision on whether the
    '.' at the beginning of url is manditory
'''
import re
from urllib.parse import urlparse, urlunsplit
from urllib import parse
from urllib import robotparser

VALID_URL_PATTERN = re.compile(r'(?:(?P<subdomain>.*)\.)?(ics|cs|informatics|stat)\.uci\.edu$')

def is_valid_domain(parsedurl):
    '''
        determines if given parsedurl object's domain is valid matching
        *.(ics|cs|informatics|stats).uci.edu/*

        @arg parsedurl urllib.parse.urlparse
        @return bool
    '''

    regex_match = re.match(VALID_URL_PATTERN, parsedurl.netloc)
    return bool(regex_match)

def get_subdomain(parsedurl):
    '''
        Returns the subdomain from the ics.uci.edu domain, given
        the regex pattern and a urlparse object

        @arg parsedurl urllib.parse.urlparse
        @return str
    '''
    regex_match = re.match(VALID_URL_PATTERN, parsedurl.netloc)
    
    if regex_match:
        return regex_match.group('subdomain')
    
    return ''

def is_permitted(parsed_url):
    '''
        Detects whether the crawler is allowed to crawl the url or not

        @arg parsedurl
        @return bool
    '''
    try:
        parser = robotparser.RobotFileParser()
        user_agent = 'IR UW23 37183376,12247482,52163133,16453140'

        parser.set_url(parse.urljoin(f'{parsed_url.scheme}://{parsed_url.netloc}', 'robots.txt'))
        parser.read()

        return parser.can_fetch(user_agent, parsed_url.path)
    except Exception as e:
        # benefit of doubt, let other checks filter url out
        return True
        


if __name__ == '__main__':
    import urllib.parse

    assert is_permitted(urlparse('https://ics.uci.edu/bin/')) == False
    assert is_permitted(urlparse('https://ics.uci.edu/bin/random.txt')) == False
    assert is_permitted(urlparse('https://ics.uci.edu/~mpufal/')) == False
    assert is_permitted(urlparse('https://ics.uci.edu/~thornton/')) == True
    assert is_permitted(urlparse('https://ics.uci.edu/~fakeprof/')) == True

    parsed = urllib.parse.urlparse('https://ics.uci.edu')
    print(is_valid_domain(parsed))
    print(get_subdomain(parsed))

    parsed = urllib.parse.urlparse('https://one.two.stat.uci.edu')
    print(is_valid_domain(parsed))
    print(get_subdomain(parsed))

    parsed = urllib.parse.urlparse('https://onetwostat.uci.edu')
    print(is_valid_domain(parsed))
    print(get_subdomain(parsed))