'''
Parses text for tokenization as well as urls from given response content
'''

from lxml import html

import requests

def scrape_urls(content, base_url):
    'takes in html string returns list of found urls'

    # parse content and make links absolute for crawling
    document = html.document_fromstring(content)
    document.make_links_absolute(base_url)

    found_urls = []

    for (element, attribute, link, pos) in document.iterlinks():
        found_urls.append(link)


    return found_urls

if __name__ == '__main__':
    a = requests.get(r'https://github.com/joshc321/cs121-crawler4py')
    r = a.content
    print(scrape_urls(r, 'https://github.com/joshc321/cs121-crawler4py'))