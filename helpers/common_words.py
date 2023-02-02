'''

TO DO: Add shelf to store common words

'''

import shelve

from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist

def appendToShelf(freqDist):
    # Adds Frequency Distribution to Shelf
    try:
        shelf = shelve.open("commonWordsShelf.db")
        
        if "mainShelf" in shelf:
            fDist = shelf["mainShelf"]

            for token in freqDist:
                fDist[token] += freqDist[token]
            shelf["mainShelf"] = fDist

        else:
            shelf["mainShelf"] = freqDist

    finally:
        shelf.close()

def getCommonWords():
    # Returns a list of tuples (token, frequency) of size 50 
    try:
        shelf = shelve.open("commonWordsShelf.db")
        if "mainShelf" in shelf:
            fDist = shelf["mainShelf"]
            return fDist.most_common(50)

    finally:
        shelf.close()


if __name__ == "__main__":

    # Sample/Test 
    sample = "I Like Boo. Boo is my favorite dog"
    fdist = FreqDist()
    for word in word_tokenize(sample):
        fdist[word.lower()] += 1
    appendToShelf(fdist)
    getCommonWords()

