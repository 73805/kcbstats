from utilities import openPkl

import pandas as pd

def clean_data(contest_df, result_df):
    # load in state abbrev -> name dictionary
    states_dict = openPkl("state_name")
    states = states_dict.keys()

    m_dict = {"January": "1", "February": "2", "March": "3", "April": "4",
              "May": "5", "June": "6", "July": "7", "August": "8", "September": "9",
              "October": "10", "November": "11", "December": "12"}

    # Remove tournaments without results (cancelled)
    contest_df = contest_df[contest_df['has_results'] == True].copy()

    # for each contest row
    for i, row in contest_df.iterrows():
        # Parse city and state
        locat = row.location
        locat = locat.split(',')
        city = locat[0].strip()
        state = locat[-1].strip().lower()
        if state == 'dc':
            state = 'md'
        in_50_states = (state in states)
        contest_df.set_value(i, 'in_50_states', in_50_states)
        contest_df.set_value(i, 'city', city)
        contest_df.set_value(i, 'state', state)

        # convert CBJ% to Float 0:100, and normalize Prize values
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

        # Parse Date String to datetime
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

    # remove results associated with ignored competitions
    result_df = result_df[result_df["contest_id"].isin(contest_df["id"].unique())]

    # cast prize and cbj percentage to floats
    contest_df['prize'] = contest_df['prize'].astype('float')
    contest_df['cbj_percentage'] = contest_df['cbj_percentage'].astype('float')

    # cast date columns to date type
    contest_df['date'] = pd.to_datetime(contest_df.date_str, infer_datetime_format=True)

    print "Finished extracting features"

    return contest_df, result_df
