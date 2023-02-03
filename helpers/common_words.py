'''

TO DO: Add shelf to store common words

'''

import shelve

from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist

def update_common_word_shelf(freqDist):
    # Adds Frequency Distribution to Shelf
    try:
        shelf = shelve.open("dataShelf.db")
        
        if "commonData" in shelf:
            fDist = shelf["commonData"]

            for token in freqDist:
                fDist[token] += freqDist[token]
            shelf["commonData"] = fDist

        else:
            shelf["commonData"] = freqDist

    finally:
        shelf.close()

def get_common_words():
    # Returns a list of tuples (token, frequency) of size 50 
    try:
        shelf = shelve.open("dataShelf.db")
        if "commonData" in shelf:
            fDist = shelf["commonData"]
            return fDist.most_common(50)

    finally:
        shelf.close()


if __name__ == "__main__":
    # Sample/Test 
    sample = "I Like Boo. Boo is my favorite dog"
    fdist = FreqDist()
    for word in word_tokenize(sample):
        fdist[word.lower()] += 1

    update_common_word_shelf(fdist)
    get_common_words()

