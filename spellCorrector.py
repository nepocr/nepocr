'''
spellCorrector.py
Unigram based spell correction utility for devnagari based language
Based off spell corrector by Peter Norvig

USAGE: this program imports big.txt file to load the frequency data into memory. Just call
correct('DEV_WORD')

RETURNS: A set of tuples with word and frequency

'''


import re
import collections

# THE MAIN DEVNAGARI CHARSET
alphabets = "क ख ग घ ङ च छ ज झ ञ ट ठ ड ढ ण त थ द ध न प फ ब भ म य र ल व श स ष ह क्ष त्र ज्ञ ा ि ी ु ू े ै ो ौ ं ः"


# Split on Space to get the list to carry out edits1
alphabetSet = alphabets.split()


# Generate regex string to split
reString = alphabets.replace(' ', '')


# Get Words for each case
def words(text): return re.findall('[' + reString + ']+', text)


# Generate word frequency
def train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model

# read and get frequency data
NWORDS = train(words(open('big.txt', 'r').read()))


# get the first edit by doing various tasks
def edits1(word):
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [a + b[1:] for a, b in splits if b]
    transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b) > 1]
    replaces = [a + c + b[1:] for a, b in splits for c in alphabetSet if b]
    inserts = [a + c + b for a, b in splits for c in alphabetSet]
    return set(deletes + transposes + replaces + inserts)


# do the second set of edit
def known_edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)


# get the known words set in NWORDS
def known(words): return set((w, NWORDS[w]) for w in words if w in NWORDS)


# get the correct word by getting the word if it exists or by using
# various transposes. Returns the dictionary with frequencies
def correct(word):
    candidates = known([word]) or known(
        edits1(word)) or known_edits2(word) or [word]
    return candidates
