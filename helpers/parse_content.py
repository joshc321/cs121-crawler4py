'''
Parses text for tokenization as well as urls from given response content
'''

from lxml import html
from lxml.html.clean import Cleaner

import nltk
nltk.download('popular')
from nltk.tokenize import word_tokenize
from nltk import FreqDist

from filter import EN_STOPWORDS

import requests

def scrape_info(content, base_url):
    '''
    scrapes urls and text from context
    
    @arg content : html string
    @arg base_url : string
    @return (set,string)
    '''
    try:
        # define cleaner with settings
        cleaner = Cleaner(style=True, javascript=True)
        # clean html
        cleaned_content = cleaner.clean_html(content)
    except Exception as e:
        print('Failed cleaning: ', base_url, e)
        cleaned_content = content
    
    try:
        # create document
        document = html.document_fromstring(cleaned_content)
        document.make_links_absolute(base_url)
    except Exception as e:
        print('Failed parsing document: ', base_url, e)
        return (set(),[])
    
    links = {link for element, attribute, link, pos in document.iterlinks()}
    text = document.text_content()
    return (links, text)

def scrape_text(content, base_url):
    'takes in html string and base url returns text found in html'
    try:
        # define Cleaner and cleaner settings
        cleaner = Cleaner(style=True, links=True, javascript=True, page_structure=True)
        # clean html
        cleaned_content = cleaner.clean_html(content)
    
    except Exception as e:
        print('Failed cleaning: ', base_url, e)
        cleaned_content = content
    
    try:
        return html.fromstring(cleaned_content).text_content()
    except Exception as e:
        print('Failed parsing text from: ', base_url, e)
        return ''

def token_freq(text: str):
    #Return a FreqDist object(similar to map)
    # Iterate through element to display results
    # Can also delete elements

    return FreqDist(word_tokenize(text.lower()))

def scrape_urls(content, base_url):
    'takes in html string and base url returns list of found urls'

    try:
        # parse content and make links absolute for crawling
        document = html.document_fromstring(content)
        document.make_links_absolute(base_url)

    except Exception as e:
        print('Failed parsing links from: ', base_url, e)
        return []

    return [link for element, attribute, link, pos in document.iterlinks()]

if __name__ == '__main__':
    a = requests.get(r'https://github.com/joshc321/cs121-crawler4py')
    r = a.content
    print(token_freq(r, 'https://github.com/joshc321/cs121-crawler4py').items())