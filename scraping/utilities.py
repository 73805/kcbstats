import pandas as pd
import json
import pickle
import unicodedata


'''
Internal Functions:
toFn
'''
def toFn(fn, suffix):
    if suffix == ".pkl":
        return "fresh_pkls/" + fn + suffix
    if suffix == ".json":
        return "fresh_json/" + fn + suffix

'''
External Functions:
getContestKeys
asciify
place_suffix
date_to_ord
saveJson
saveDict
saveDf
openDict
openDf
'''

# get list of contest keys currently in the database
def getContestKeys():
    contests = openPkl("contests")
    keys = contests.keys()
    return map(int, keys)

# convert string to ascii
def asciify(st):
    if type(st) == unicode:
        st = unicodedata.normalize('NFKD', st).encode('ascii', 'ignore').strip()
    else:
        st = unicode(st, 'ascii', 'ignore')
        st = unicodedata.normalize('NFKD', st).encode('ascii', 'ignore').strip()
    return st

# add suffix to finishing place ordinal 1 -> 1st, 11 -> 11th, 21 -> 21st
def place_suffix(place):
    if (place < 11) or (place > 19):
        s = str(place)
        suf = s[-1]
        if suf is '1':
            return s + 'st'
        elif suf is '2':
            return s + 'nd'
        elif suf is '3':
            return s + 'rd'
        else:
            return s + 'th'
    else:
        s = str(place)
        return s + 'th'

# convert a date string to a sortable integer YYYYMMDD
def date_to_ord(date_str):
    vals = date_str.split("-")
    yy = int(vals[2])
    mm = int(vals[0])
    dd = int(vals[1])
    return (10000*yy) + (100 * mm) + dd

def saveJson(obj, fn):
    fn = toFn(fn, ".json")
    with open(fn, 'w') as outfile:
        json.dump(obj, outfile, indent=4, allow_nan=False)

def savePkl(obj, fn):
    fn = toFn(fn, ".pkl")
    with open(fn, "wb") as handle:
        pickle.dump(obj, handle)

# Save a dataframe
def saveDf(obj, fn):
    fn = toFn(fn, ".pkl")
    obj.to_pickle(fn)

# open a pickle file
def openPkl(fn):
    fn = toFn(fn, ".pkl")
    with open(fn, "r") as handle:
        return pickle.load(handle)


# open a pickle file
def openDf(fn):
    fn = toFn(fn, ".pkl")
    return pd.read_pickle(fn)