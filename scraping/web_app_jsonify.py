import pandas as pd
import json
from sklearn import preprocessing
import pickle
import math


do_contests = True
do_teams = True
do_states = True

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

def date_to_ord(date_str):
    vals = date_str.split("-")
    yy = int(vals[2])
    mm = int(vals[0])
    dd = int(vals[1])
    return (10000*yy) + (100 * mm) + dd

def saveJson(obj, fn):
    fn = "fresh_json/" + fn + ".json"
    with open(fn, 'w') as outfile:
        json.dump(obj, outfile, indent=4, allow_nan=False)

def saveDict(obj, fn):
    fn = "fresh_pkls/" + fn + ".pkl"
    with open(fn, "wb") as handle:
        pickle.dump(obj, handle)


all_result_df = pd.read_pickle("fresh_pkls/result_df.pkl")
contest_df = pd.read_pickle("fresh_pkls/contest_df_cleaned.pkl")
five_cats = ["overall", "chicken", "ribs", "pork", "brisket"]

# subset the results to those associated with the current competitions
result_df = all_result_df[all_result_df["contest_key"].isin(contest_df["contest_number"].unique())]

# subset result table to the standard categories and overall
result_df = result_df[result_df["category"].isin(five_cats)]

# subset the competitions to those that have at least one overall result
overall_result_keys = result_df[result_df["category"] == "overall"]["contest_key"].unique()
contest_df = contest_df[contest_df["contest_number"].isin(overall_result_keys)]

# Remove results associated with teams that have no overall finishes
finishers = result_df[result_df["category"] == "overall"]["team_name"].unique()
result_df = result_df[result_df["team_name"].isin(finishers)].copy()

# encode team names to keys
team_encoder = preprocessing.LabelEncoder()
team_encoder.fit(result_df['team_name'])
result_df['team_key'] = team_encoder.transform(result_df['team_name'])

# get a list of all the teams still in the result data frame
finisher_keys = result_df['team_key'].unique()

# create a joined data frame of all the result records + contest data (inner join)
joined = pd.merge(result_df, contest_df, left_on='contest_key', right_on="contest_number")

# build the contest dictionary
cdict = {}
cdict_sub = {}
if do_contests:
    for i, contest in contest_df.iterrows():
        data = {}
        result_sub = result_df[result_df.contest_key == contest.contest_number]

        # simple features
        data["attendance"] = int(result_sub["team_name"].unique().shape[0])
        data["date_str"] = contest.date_str.replace("-", "/")
        data["date_order"] = date_to_ord(contest.date_str)
        data["is_state_champ"] = contest.champ_bool
        data["location"] = contest.location
        data["name"] = contest.title
        data["prize"] = int(contest.prize)
        data["state"] = contest.state
        cbj = contest.cbj_percentage
        if math.isnan(cbj):
            data["cbj_percentage"] = "NA"
        else:
            data["cbj_percentage"] = str(int(contest.cbj_percentage)) + "%"

        # teams and score data
        data["teams"] = {}
        for team_key in result_sub["team_key"].unique():
            team_results = result_sub[result_sub["team_key"] == team_key]
            team_key = str(int(team_key))
            data["teams"][team_key] = {}
            data["teams"][team_key]["name"] = team_results["team_name"].unique()[0]
            for k, result in team_results.iterrows():
                if result.category == "overall":
                    data["teams"][team_key]["place"] = int(result.place)
                data["teams"][team_key][result.category] = result.score

        cdict[str(int(contest.contest_number))] = data.copy()

    saveDict(cdict, "contests")
    saveJson(cdict, "contests")

    # create mini contest dict without scoring data for state pages
    for key in cdict.keys():
        data = cdict[key].copy()
        data.pop("teams", None)
        cdict_sub[key] = data.copy()

    saveDict(cdict_sub, "contests_basic")
    saveJson(cdict_sub, "contests_basic")

    print "Finished contests"

# build the teams dictionary
tdict = {}
if do_teams:
    for team_key in finisher_keys:
        data = {}
        joined_sub = joined[joined["team_key"] == team_key]
        overalls = joined_sub[joined_sub["category"] == "overall"]
        pure_overalls = overalls[overalls["skewed_overall"] == False]
        standards = joined_sub[joined_sub["category"] != "overall"]

        data["appearances"] = int(overalls.shape[0])
        data["top_finish"] = place_suffix(int(overalls["place"].min()))
        data["top_5s"] = int(overalls[overalls["place"] < 6].shape[0])
        data["name"] = joined_sub["team_name"].unique()[0]
        data["state"] = overalls["state"].value_counts().index[0]
        # overall average
        if pure_overalls.shape[0] > 0:
            data["overall_avg"] = float(pure_overalls["score"].mean())
        else:
            data["overall_avg"] = 0
        # best category
        groups = standards.groupby(by="category")["score"].mean()
        if len(groups[groups == groups.max()].index) > 0:
            data["strong_cat"] = groups[groups == groups.max()].index[0]
        else:
            data["strong_cat"] = "NA"
        tdict[str(int(team_key))] = data.copy()

    print "finished teams meta data!"

    # contests and scores
    # for each contest
    for key in contest_df["contest_number"]:
        ckey = str(int(key))
        # get the contest meta data
        sub = contest_df[contest_df["contest_number"] == key]
        date_str = sub["date_str"].values[0].replace("-", "/")
        date_order = date_to_ord(sub["date_str"].values[0])
        name = sub["title"].values[0]
        state = sub["state"].values[0]
        # subset the results and iterate them
        sub = result_df[result_df.contest_key == key]
        for j, result in sub.iterrows():
            tkey = str(int(result.team_key))
            if tkey in tdict:
                # initiate the contests dict if it didn't exist
                if not("contests" in tdict[tkey]):
                    tdict[tkey]["contests"] = {}
                # initiate the contest entry if it didn't exist
                if not(ckey in tdict[tkey]["contests"]):
                    tdict[tkey]["contests"][ckey] = {}
                if result.category == "overall":
                    tdict[tkey]["contests"][ckey]["place"] = int(result.place)
                    tdict[tkey]["contests"][ckey]["date_str"] = date_str
                    tdict[tkey]["contests"][ckey]["date_order"] = int(date_order)
                    tdict[tkey]["contests"][ckey]["name"] = name
                    tdict[tkey]["contests"][ckey]["state"] = state
                tdict[tkey]["contests"][ckey][result.category] = result.score
    print "finished teams contest data!"

    saveDict(tdict, "teams")
    saveJson(tdict, "teams")

if do_states:
    # state dictionary
    with open("fresh_pkls/state_region.pkl", "rb") as fn:
        state_region = pickle.load(fn)

    with open("fresh_pkls/state_name.pkl", "rb") as fn:
        state_name = pickle.load(fn)

    sdict = {}
    for state in state_name.keys():
        data = {}
        joined_sub = joined[joined["state"] == state]
        overalls = joined_sub[joined_sub["category"] == "overall"]
        contest_sub = contest_df[contest_df["state"] == state]

        data["fullname"] = state_name[state]
        data["region"] = state_region[state]

        if contest_sub.shape[0] > 0:
            data["exists"] = True
            data["prize_avg"] = contest_sub["prize"].mean()
            data["teams_competed"] = joined_sub[joined_sub["category"] == "overall"]["team_key"].unique().shape[0]
            data["hot_month"] = contest_sub['date'].dt.strftime('%B').value_counts().index[0]
        else:
            data["exists"] = False
            data["prize_avg"] = "NA"
            data["teams_competed"] = 0
            data["hot_month"] = "NA"

        sdict[state] = data.copy()
        print "finished state " + state

    saveJson(sdict, "states")
