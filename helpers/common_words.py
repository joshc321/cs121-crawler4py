'''

Handles sotring and analysis of process data by crawler

'''

import shelve
import urllib.parse
from threading import Lock

from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist

from collections import defaultdict
from url_check import get_subdomain


data_shelf_lock = Lock()

def update_data_shelf(freqDist, url):
    # Adds Frequency Distribution to Shelf
    with data_shelf_lock:
        try:
            # Open Shelf File
            shelf = shelve.open("dataShelf.db")
            
            # Updates commonData key which stores token frequency
            if "commonData" in shelf:
                fDist = shelf["commonData"]

                for token in freqDist:
                    fDist[token] += freqDist[token]
                shelf["commonData"] = fDist

            else:
                shelf["commonData"] = freqDist
            
            # Updates longestPage key which stores a tuple of url and token count
            if "longestPage" in shelf:
                longPage = shelf["longestPage"]

                currentPageSize = sum(freqDist.values())

                if (currentPageSize > longPage[1]):
                    shelf["longestPage"] = (url, currentPageSize)
            
            else:
                shelf["longestPage"] = (url, sum(freqDist.values()))
                
            
            # Updates subdomainData which stores amount of links in each subdomain
            if "subdomainData" not in shelf:
                shelf["subdomainData"] = defaultdict(int)
            
            sDict = shelf["subdomainData"]
            parsedUrl = urllib.parse.urlparse(url)
            subDomain = get_subdomain(parsedUrl)
            if (subDomain and "ics.uci.edu" in url):
                sDict[subDomain] += 1
            
            shelf["subdomainData"] = sDict


        finally:
            shelf.close()

def get_common_words():
    # Returns a list of tuples (token, frequency) of size 50 
    try:
        shelf = shelve.open("dataShelf.db")
        if "commonData" in shelf:
            fDist = shelf["commonData"]
            return fDist.most_common(50)
        else:
            print("Common Data does not exist on Shelf")

    finally:
        shelf.close()

def get_longest_page():
    try:
        shelf = shelve.open("dataShelf.db")
        if "longestPage" not in shelf:
            raise KeyError
        
        return shelf["longestPage"]
    
    except KeyError:
        print("Longest Page data does not exist on Shelf")

    finally:
        shelf.close()

def print_subdomains():
    # Formats and Prints subdomain and count into console

    try:
        shelf = shelve.open("dataShelf.db")
        if "subdomainData" not in shelf:
            raise KeyError
        
        sDict = shelf["subdomainData"]

        for key, value in sorted(sDict.items(), key=lambda x: (x[0], -x[1])):
            print(f'{key}, {value}')
    
    except KeyError:
        print("Subdomain Data does not exist on Shelf")

    finally:
        shelf.close()


if __name__ == "__main__":
    # Sample Test
    sample = "I Like Boo. Boo is my favorite dog"
    fdist = FreqDist()
    for word in word_tokenize(sample):
        fdist[word.lower()] += 1
    url = 'https://123.two.stat.uci.edu'
    update_data_shelf(fdist, url)
    print_subdomains()
    print("List of Common Words:", get_common_words())
    print("Longest Page:", get_longest_page())

