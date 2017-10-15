from utilities import savePkl
from utilities import openPkl

import pandas as pd
import datetime

# removing competitions and results that don't fit the criteria!
def filter_data(contest_df, result_df):
    # remove contests which are already in the records
    old_contests = openPkl("contests_basic")
    old_keys = map(int, old_contests.keys())
    # note the ~ index-not operator
    contest_df = contest_df[~contest_df["id"].isin(old_keys)]

    # remove contests which don't yet have results
    overall_result_keys = list(result_df[result_df["category"] == "overall"]["contest_id"].unique())
    contest_df = contest_df[contest_df["id"].isin(overall_result_keys)]

    # remove contests from outside the 50 states
    contest_df = contest_df[contest_df["in_50_states"] == True]

    # Remove contests before the scoring update (July 13, 2013)
    early_cutoff = datetime.date(2013, 7, 13)
    contest_df = contest_df[contest_df['date'] > early_cutoff]

    print "Found " + str(contest_df.shape[0]) + " new contest(s)"

    # remove results associated with removed contests
    result_df = result_df[result_df["contest_id"].isin(contest_df["id"].unique())]

    # remove results associated with non-standard categories
    five_cats = ["overall", "chicken", "ribs", "pork", "brisket"]
    result_df = result_df[result_df["category"].isin(five_cats)]

    # remove results for teams that did not have an overall finish in the contest
    filtered_results = pd.DataFrame(columns=list(result_df.columns))
    for i, contest_id in enumerate(list(result_df["contest_id"].unique())):
        result_sub = result_df[result_df["contest_id"] == contest_id]
        # only include results from teams who placed overall
        contest_finishers = result_sub[result_sub["category"] == "overall"]["team_name"].unique()
        result_sub = result_sub[result_sub["team_name"].isin(contest_finishers)].copy()
        filtered_results = pd.concat([filtered_results, result_sub])

    contest_df = contest_df.copy()
    result_df = filtered_results.copy()

    # encode teams names to unique team ID numbers
    team_key_map = openPkl("team_name_map")
    # create new IDs for unseen teams
    new_teams = list(set(list(result_df["team_name"].unique())) - set(team_key_map.keys()))
    max_id = max(team_key_map.values())
    for i, name in enumerate(new_teams):
        team_key_map[name] = int(max_id + i + 1)

    # write out the updated encoding
    savePkl(team_key_map, "team_name_map")

    # apply the encoding to the result dataframe
    result_df["team_id"] = -1
    result_df["team_id"].update(result_df["team_name"].map(team_key_map))

    print "Finished filtering rows"
    return contest_df, result_df
