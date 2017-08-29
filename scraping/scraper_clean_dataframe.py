import pandas as pd
import datetime
import numpy as np
import pickle
import unicodedata

def asciify(st):
    if type(st) == unicode:
        st = unicodedata.normalize('NFKD', st).encode('ascii', 'ignore').strip()
    else:
        st = unicode(st, 'ascii', 'ignore')
        st = unicodedata.normalize('NFKD', st).encode('ascii', 'ignore').strip()
    return st

contest_df = pd.read_pickle('fresh_pkls/contest_df.pkl')
result_df = pd.read_pickle('fresh_pkls/result_df.pkl')

# Remove tournaments without results (cancelled)
contest_df = contest_df[contest_df['has_results'] == True].copy()

print "Removed Cancellations!"

# Split location column into city and state columns
states_dict = {'ak': 'Alaska', 'al': 'Alabama', 'ar': 'Arkansas', 'az': 'Arizona', 'ca': 'California',
         'co': 'Colorado', 'ct': 'Connecticut', 'de': 'Delaware', 'fl': 'Florida', 'ga': 'Georgia',
         'hi': 'Hawaii', 'ia': 'Iowa', 'id': 'Idaho', 'il': 'Illinois', 'in': 'Indiana',
         'ks': 'Kansas', 'ky': 'Kentucky', 'la': 'Louisiana', 'ma': 'Massachusetts',
         'md': 'Maryland', 'me': 'Maine', 'mi': 'Michigan', 'mn': 'Minnesota', 'mo': 'Missouri',
         'ms': 'Mississippi', 'mt': 'Montana', 'nc': 'North Carolina', 'nd': 'North Dakota',
         'ne': 'Nebraska', 'nh': 'New Hampshire', 'nj': 'New Jersey', 'nm': 'New Mexico',
         'nv': 'Nevada', 'ny': 'New York', 'oh': 'Ohio', 'ok': 'Oklahoma', 'or': 'Oregon',
         'pa': 'Pennsylvania', 'ri': 'Rhode Island', 'sc': 'South Carolina', 'sd': 'South Dakota',
         'tn': 'Tennessee', 'tx': 'Texas', 'ut': 'Utah', 'va': 'Virginia', 'vt': 'Vermont',
         'wa': 'Washington', 'wi': 'Wisconsin', 'wv': 'West Virginia', 'wy': 'Wyoming'}
states = states_dict.keys()

# Parsing city and state
for i, row in contest_df.iterrows():
    locat = row.location
    locat = locat.split(',')
    city = locat[0].strip()
    state = locat[-1].strip().lower()
    if state == 'dc':
        state = 'md'
    keep = (state in states)
    contest_df.set_value(i, 'keep', keep)
    contest_df.set_value(i, 'city', city)
    contest_df.set_value(i, 'state', state)

print "Split location column into city and state columns!"

contest_df = contest_df[contest_df.keep == True]

print "Removed contests from outside the 50 States."

# Convert CBJ% to Float 0:100, and normalize Prize values
for i, row in contest_df.iterrows():
    prize = row.prize
    if prize == 'NA':
        prize = 0
    contest_df.set_value(i, 'prize', prize)
    cbj = row.cbj_percentage
    if cbj == 'NA':
        cbj = 'nan'
    else:
        cbj = cbj[:-1] + '.0'
    contest_df.set_value(i, 'cbj_percentage', cbj)

contest_df['prize'] = contest_df['prize'].astype('float')
contest_df['cbj_percentage'] = contest_df['cbj_percentage'].astype('float')

print "Converted CBJ Percentage and Prize Values to Floats!"

# Parse Date String to datetime
m_dict = {"January": "1", "February": "2", "March": "3", "April": "4",
        "May": "5", "June": "6", "July": "7", "August": "8", "September": "9",
        "October": "10", "November": "11", "December": "12"}
for i, row in contest_df.iterrows():
    ds = row.date_str
    ds = ds.split(',')
    year = ds[-1].strip()
    year = year[2:]
    m_d = ds[0].split(' ')
    month = m_d[0].strip()
    month = m_dict[month]
    day = str(m_d[1].strip())
    date_concat = month + "-" + day + "-" + year
    contest_df.set_value(i, 'date_str', date_concat)

contest_df['date'] = pd.to_datetime(contest_df.date_str, infer_datetime_format=True)

print "Parsed date strings and datetimes!"

# Remove competitions before the scoring update (July 13, 2013)
early_cutoff = datetime.date(2013, 7, 13)
# early_cutoff = datetime.date(2016, 1, 1)
contest_df = contest_df[contest_df['date'] > early_cutoff]

print "Removed Competitions pre-dating scoring changes!"

result_df = result_df[result_df["contest_key"].isin(contest_df.contest_number.unique())]

# Save the cleaned data to a new pickle file
contest_df.to_pickle('fresh_pkls/contest_df_cleaned.pkl')
result_df.to_pickle('fresh_pkls/result_df_cleaned.pkl')

print "Saved out new dataframes to a pickle file"
