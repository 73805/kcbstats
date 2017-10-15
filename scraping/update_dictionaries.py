from utilities import place_suffix
from utilities import date_to_ord
from utilities import savePkl
from utilities import saveDf
from utilities import openPkl
from utilities import openDf

import pandas as pd
import math


# Updating the pickled dictionaries of contests, contests_basic, teams, and states
def update_dictionaries(new_contest_df, new_result_df):

    # read in the master dataframes
    contest_df = openDf("contest_df_master")
    result_df = openDf("result_df_master")
    # keep track of the new apendees
    new_contest_df["is_new"] = 1
    new_result_df["is_new"] = 1
    contest_df["is_new"] = 0
    result_df["is_new"] = 0
    # add new results to the master dataframes
    contest_df = pd.concat([contest_df, new_contest_df])
    result_df = pd.concat([result_df, new_result_df])
    # drop duplicates
    contest_df = contest_df.drop_duplicates(subset="id", keep="last")
    contest_df = contest_df.reset_index(drop=True)
    result_df = result_df.drop_duplicates(subset=["team_id", "contest_id", "score", "category"], keep="last")
    result_df = result_df.reset_index(drop=True)
    # get the new stuff after duplicates are dropped
    new_contest_df = contest_df[contest_df["is_new"] == 1]
    new_result_df = result_df[result_df["is_new"] == 1]
    # reset the is_new columns
    contest_df["is_new"] = 0
    result_df["is_new"] = 0
    # save out the master dataframes
    saveDf(contest_df, "contest_df_master")
    saveDf(result_df, "result_df_master")

    # read in the master dictionaries for mergers and appends (state is a full overwrite)
    master_contests = openPkl("contests")
    master_contests_basic = openPkl("contests_basic")
    master_teams = openPkl("teams")

    # update the master dictionaries:

    ###########################
    # Create Contest fresh append
    ##########################
    cdict = {}
    for i, contest in new_contest_df.iterrows():
        data = {}
        # subset the results for the contest
        result_sub = new_result_df[new_result_df["contest_id"] == contest.id]

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
        for team_id in result_sub["team_id"].unique():
            team_results = result_sub[result_sub["team_id"] == team_id]
            team_id = str(int(team_id))
            data["teams"][team_id] = {}
            data["teams"][team_id]["name"] = team_results["team_name"].unique()[0]
            for k, result in team_results.iterrows():
                if result.category == "overall":
                    data["teams"][team_id]["place"] = int(result.place)
                data["teams"][team_id][result.category] = result.score

        cdict[str(int(contest.id))] = data.copy()

    # Update Contest Profiles Dictionary
    for key in cdict.keys():
        master_contests[key] = cdict[key].copy()

    ##################################
    # Contest Basic Data: fresh append
    #################################
    cdict_basic = {}
    for key in cdict.keys():
        data = cdict[key].copy()
        data.pop("teams", None)
        cdict_basic[key] = data.copy()

    # Update Contest Profiles Dictionary
    for key in cdict_basic.keys():
        master_contests_basic[key] = cdict_basic[key].copy()

    print "Finished contests"

    ##################################
    # Team Profiles: full overwrite of aggregate fields
    #################################

    # create joined dataframes for master and new
    joined = pd.merge(result_df, contest_df, left_on='contest_id', right_on="id")

    # team updates need to take place directly on the master dictionary
    tdict = master_teams.copy()
    tdict_keys = tdict.keys()
    for team_id in list(result_df["team_id"].unique()):
        id_str = str(int(team_id))
        if not(id_str in tdict_keys):
            tdict[id_str] = {}

        # subset the results for this team
        joined_sub = joined[joined["team_id"] == team_id]
        overalls = joined_sub[joined_sub["category"] == "overall"]
        pure_overalls = overalls[overalls["skewed_overall"] == False]
        standards = joined_sub[joined_sub["category"] != "overall"]

        # simple features
        tdict[id_str]["appearances"] = int(overalls.shape[0])
        tdict[id_str]["top_finish"] = place_suffix(int(overalls["place"].min()))
        tdict[id_str]["top_5s"] = int(overalls[overalls["place"] < 6].shape[0])
        tdict[id_str]["name"] = joined_sub["team_name"].unique()[0]
        tdict[id_str]["state"] = overalls["state"].value_counts().index[0]
        # overall average
        if pure_overalls.shape[0] > 0:
            tdict[id_str]["overall_avg"] = float(pure_overalls["score"].mean())
        else:
            tdict[id_str]["overall_avg"] = 0
        # best category
        groups = standards.groupby(by="category")["score"].mean()
        if len(groups[groups == groups.max()].index) > 0:
            tdict[id_str]["strong_cat"] = groups[groups == groups.max()].index[0]
        else:
            tdict[id_str]["strong_cat"] = "NA"

    print "Finished teams meta data!"

    ##################################
    # Team Contest History: Scary merge with master dictionary
    #################################

    tdict_keys = tdict.keys()
    for c_id in list(new_contest_df["id"].unique()):
        c_id_str = str(int(c_id))
        # grab some contest context data straight from the master dictionary
        cdata = cdict[c_id_str]
        date_str = cdata["date_str"]
        date_order = cdata["date_order"]
        name = cdata["name"]
        state = cdata["state"]
        # subset the contest's results and iterate them
        sub = new_result_df[new_result_df["contest_id"] == c_id]
        for j, result in sub.iterrows():
            t_id_str = str(int(result["team_id"]))
            if t_id_str in tdict_keys:
                # initiate a "contests" dictionary if the team didn't have one yet
                if not("contests" in tdict[t_id_str]):
                    tdict[t_id_str]["contests"] = {}
                # initiate the specific contest entry if the team didn't have it yet
                if not(c_id_str in tdict[t_id_str]["contests"].keys()):
                    tdict[t_id_str]["contests"][c_id_str] = {}
                if result.category == "overall":
                    tdict[t_id_str]["contests"][c_id_str]["place"] = int(result["place"])
                    tdict[t_id_str]["contests"][c_id_str]["date_str"] = date_str
                    tdict[t_id_str]["contests"][c_id_str]["date_order"] = int(date_order)
                    tdict[t_id_str]["contests"][c_id_str]["name"] = name
                    tdict[t_id_str]["contests"][c_id_str]["state"] = state
                tdict[t_id_str]["contests"][c_id_str][result["category"]] = result["score"]
    print "finished teams contest data!"

    master_teams = tdict.copy()

    ##################################
    # State Profiles: full overwrite of aggregates
    #################################
    state_region = openPkl("state_region")
    state_name = openPkl("state_name")
    sdict = {}

    for state in state_name.keys():
        data = {}
        joined_sub = joined[joined["state"] == state]
        contest_sub = contest_df[contest_df["state"] == state]

        data["fullname"] = state_name[state]
        data["region"] = state_region[state]

        if contest_sub.shape[0] > 0:
            data["exists"] = True
            data["prize_avg"] = contest_sub["prize"].mean()
            data["teams_competed"] = joined_sub[joined_sub["category"] == "overall"]["team_id"].unique().shape[0]
            data["hot_month"] = contest_sub['date'].dt.strftime('%B').value_counts().index[0]
        else:
            data["exists"] = False
            data["prize_avg"] = "NA"
            data["teams_competed"] = 0
            data["hot_month"] = "NA"

        sdict[state] = data.copy()
    print "finished states"

    master_states = sdict.copy()

    ##################################
    # Save out the master dictionaries
    #######################hi##########

    savePkl(master_contests, "contests")
    savePkl(master_contests_basic, "contests_basic")
    savePkl(master_teams, "teams")
    savePkl(master_states, "states")



