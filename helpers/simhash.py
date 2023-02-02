HASH_LENGTH = 64 # length of hash's produced by builtin hash
_DEBUG = False

if _DEBUG:
    HASH_LENGTH = 8
    from nltk import FreqDist

def simhash(tokens):
    '''
    Input: FreqDist of tokens
    returns fingerprint as int
    '''

    fingerprint = 0

    V = [0 for i in range(HASH_LENGTH)]

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

    for word, freq in tokens.items():
        word_hash = hash(word)

        if _DEBUG:
            word_hash = fake_hash[word]

        for i in range(HASH_LENGTH):
            wordbit = (word_hash >> i) & 1

            if wordbit == 1: # add weight
                V[i] += freq
            elif wordbit == 0: # subtract weight
                V[i] -= freq

    for i, vbit in enumerate(V):
        if vbit > 0: # positive so 1 in fingerprint, add
            fingerprint += (1 << i)

    if _DEBUG:
        print(V[::-1])
        print(bin(fingerprint))

    return fingerprint

def similarity(fingerprint1, fingerprint2):
    simbit = ~ (fingerprint1 ^ fingerprint2) # XNOR, 1s where bits are the same, 0s where they are different

    num_same = 0

    for i in range(HASH_LENGTH):
        if simbit >> i & 1 == 1:
            num_same += 1
    
    return float(num_same) / HASH_LENGTH