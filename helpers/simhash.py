HASH_LENGTH = 256
_DEBUG = False

if _DEBUG:
    HASH_LENGTH = 8
    from nltk import FreqDist

import hashlib

def simhash(tokens):
    '''
    Input: FreqDist of tokens
    returns fingerprint as int
    '''

    fingerprint = 0

    V = [0] * HASH_LENGTH

    if _DEBUG:
        fake_hash = {
            'tropical': 0b01100001,
            'fish': 0b10101011,
            'include': 0b11100110,
            'found': 0b00011110,
            'environments': 0b00101101,
            'around': 0b10001011,
            'world': 0b00101010,
            'including': 0b11000000,
            'both': 0b10101110,
            'freshwater': 0b00111111,
            'salt': 0b10110101,
            'water': 0b00100101,
            'species': 0b11101110
        }
        tokens = FreqDist(['tropical', 'tropical', 'fish', 'fish', 'include', 'found', 'environments', 'around', 'world', 'including', 'both', 'freshwater', 'salt', 'water', 'species'])

    # build vector V
    for word, freq in tokens.items():
        word_hash = int(hashlib.sha256(word.encode('utf-8')).hexdigest(),16)

        if _DEBUG:
            word_hash = fake_hash[word]

        for i in range(HASH_LENGTH):
            wordbit = (word_hash >> i) & 1

            if wordbit == 1: # add weight
                V[i] += freq
            elif wordbit == 0: # subtract weight
                V[i] -= freq

    # build fingerprint
    for i, vbit in enumerate(V):
        if vbit > 0: # positive so 1 in fingerprint, add
            fingerprint += (1 << i)

    if _DEBUG:
        print(V[::-1])
        print(bin(fingerprint))

    return fingerprint

def similarity(fingerprint1, fingerprint2):
    '''
    Takes two fingerprints
    Returns a percentage as a float indicating how many bits they have in common
    '''
    simbit = ~ (fingerprint1 ^ fingerprint2) # XNOR, 1s where bits are the same, 0s where they are different

    num_same = 0

    for i in range(HASH_LENGTH):
        num_same += simbit >> i & 1
    
    return float(num_same) / HASH_LENGTH

if __name__ == '__main__':
    import requests
    from parse_content import scrape_info, token_freq
    from nltk.tokenize import word_tokenize

    resp1 = requests.get('https://www.timeanddate.com/calendar/monthly.html?year=2021&month=2&country=1')
    resp2 = requests.get('https://www.timeanddate.com/calendar/monthly.html?year=2023&month=1&country=1')

    links1, text1 = scrape_info(resp1.content, resp1.url)
    links2, text2 = scrape_info(resp2.content, resp2.url)

    tokens1 = word_tokenize(text1.lower())
    tokens2 = word_tokenize(text2.lower())

    token_freq1 = token_freq(tokens1)
    token_freq2 = token_freq(tokens2)

    h1 = simhash(token_freq1)
    h2 = simhash(token_freq2)
    print(h1)
    print(h2)

    print(similarity(h1,h2))