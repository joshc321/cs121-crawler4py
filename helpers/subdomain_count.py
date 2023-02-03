'''

Record subdomains and count amount of unique pages in each

Perhaps call this function in url_check sub domain
Perhaps call this function for x amount of rul parsed to save time
Perhaps write into text file

'''

import shelve
from collections import defaultdict
from url_check import get_subdomain

def update_subdomain_shelf(parsedurl):
    try:
        shelf = shelve.open("dataShelf.db")
        
        if "subdomainData" not in shelf:
            shelf["subdomainData"] = defaultdict(int)
        
        sDict = shelf["subdomainData"]
        
        subDomain = get_subdomain(parsedurl)
        if (subDomain):
            sDict[subDomain] += 1
        
        shelf["subdomainData"] = sDict
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
    import urllib.parse

    parsedurl = urllib.parse.urlparse('https://123.two.stat.uci.edu')
    update_subdomain_shelf(parsedurl)
    print_subdomains()

