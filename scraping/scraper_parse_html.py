import os
import bs4
import pandas as pd
import re
import string


# define template rows for the contest and result dataframes
contest_template = {"contest_number": "NA", "url": "NA", "title": "NA", "location": "NA", "date_str": "NA",
                    "prize": "NA", "cbj_percentage": "NA", "champ_bool": "NA", "has_results": "NA",
                    "has_core": "NA", "has_extra": "NA", "skewed_overall": "NA", "standard_scoring": "NA"}

result_sub_template =                  {"category": "NA", "team_name": "NA", "score": "NA", "place": "NA"}
result_template = {"contest_key": "NA", "category": "NA", "team_name": "NA", "score": "NA", "place": "NA"}

standard_cats = ["chicken", "ribs", "pork", "brisket", "overall"]


HOT_START = False
if HOT_START:
    result_df = pd.read_pickle("fresh_pkls/result_df.pkl")
    contest_df = pd.read_pickle("fresh_pkls/contest_df.pkl")
    target_years = [2014]
    start_key = 4664
    just_one = True
else:
    contest_df = pd.DataFrame(columns=contest_template.keys())
    result_df = pd.DataFrame(columns=result_template.keys())
    target_years = [2013, 2014, 2015, 2016, 2017]

# Iterate the downloaded html files
for year in target_years:
    directory = "contest_html/" + str(year)
    for i, clink in enumerate(os.listdir(directory)):

        if HOT_START and (year == target_years[0]):
            code = int(clink.split("-")[0])
            if just_one:
                if code != start_key:
                    continue
            else:
                if code < start_key:
                    continue

        fname = directory + "/" + clink
        with open(fname) as fp:
            contest = bs4.BeautifulSoup(fp, "html.parser")

        # initiate a new default row
        row_dict = contest_template.copy()

        # url
        url = "http://www.kcbs.us/event/" + clink[:4] + "/" + clink[5:-5]
        row_dict["url"] = url

        # title
        title_handle = contest.select(".event_head")
        if len(title_handle) > 0:
            title = title_handle[0].text.strip()
            row_dict["title"] = title

        # location / date as string
        sub_head = contest.select("#event_subhead")
        if len(sub_head) > 0:
            sub_head = sub_head[0]
            sub_head = sub_head.text.split('\n\t\t')
            if len(sub_head) == 3:
                location = sub_head[1].strip()
                date_str = sub_head[2].strip()
                row_dict["location"] = location
                row_dict["date_str"] = date_str

        # Meta Data - keys match website labels
        meta_dict = {"website": "NA", "kcbs reps": "NA", "contest number": "NA",
                     "prize money": "NA", "cbj percentage": "NA"}
        p_tags = contest.select("p")
        for tag in p_tags:
            text = tag.text
            # get a hold of the unlabelled meta-data <p> tag
            if "Contest Number:" in text:
                meta_data = text.split("\n")
                # meta-data in un-labelled HTML tags but have consistent plain text 'labels'
                for line in meta_data:
                    # split plain text label from its value
                    line = line.split(":")
                    if len(line) == 2:
                        key = line[0].strip().lower()
                        value = line[1].strip()
                        # minor adjustments to the prize money string
                        if key == "prize money":
                            # remove leading '$' and commas
                            value = float(value[1:].replace(",", ""))
                        meta_dict[key] = value

                row_dict["contest_number"] = int(meta_dict["contest number"])
                row_dict["prize"] = meta_dict["prize money"]
                row_dict["cbj_percentage"] = meta_dict["cbj percentage"]
            else:
                pass

        # State Championship Boolean
        champ_bool = False
        champ_text = contest.select('.float20 p strong em')
        if len(champ_text) > 0:
            if champ_text[0].text.strip() == "STATE CHAMPIONSHIP":
                champ_bool = True
        row_dict["champ_bool"] = champ_bool

        # Initiate some vars before diving into results
        temp_df = pd.DataFrame(columns=result_sub_template.keys())
        standard_cats = ["chicken", "ribs", "pork", "brisket", "overall"]
        extra_cats = 0
        has_results = False

        result_html = contest.select("div.grid07.float20 table.contestResults")
        if len(result_html) > 0:
            has_results = True
            # for each table of results
            for tbl in result_html:
                rows = tbl.select('tr')
                if len(rows) > 0:
                    # throw the kitchen sink at table heads
                    table_name = rows[0].text.strip().lower()
                    table_name = str(re.sub(r'\d+', '', table_name))
                    table_name = table_name.translate(None, string.punctuation)
                    table_name = table_name.strip()
                    if table_name == "pork ribs":
                        table_name = "ribs"
                    if table_name in standard_cats:
                        # cross this category off the list
                        standard_cats.remove(table_name)
                        # for each row in each table (unfortunately)
                        for q in range(1, len(rows)):
                            res_row = result_sub_template.copy()
                            res_row['category'] = table_name
                            trow = rows[q]
                            # unpack cells from row
                            cells = trow.select("td")
                            if len(cells) == 3:
                                res_row['place'] = float(cells[0].text)
                                res_row['team_name'] = cells[1].text
                                res_row['score'] = float(cells[2].text)
                                # add the row to the dataframe (in the dictionary)
                                temp_df.loc[-1] = res_row
                                temp_df.index = temp_df.index + 1
                    else:
                        extra_cats += 1

        # has any results
        row_dict["has_results"] = has_results

        # has all the standard categories
        row_dict["has_core"] = not(bool(len(standard_cats)))

        # has extra categories
        row_dict["has_extra"] = bool(extra_cats)

        # Maximum overall score over 720 (indicates non-standard category scoring)
        over_720 = False
        max_overall = temp_df[temp_df['category'] == "overall"]["score"].max()
        if max_overall > 720:
            over_720 = True

        row_dict["skewed_overall"] = over_720

        # has standard scoring
        row_dict["standard_scoring"] = (row_dict["has_core"] and not(row_dict["skewed_overall"]))


        # append the temporary results df to the master results df
        temp_df['contest_key'] = int(meta_dict["contest number"])
        result_df = pd.concat([result_df, temp_df])

        # insert the competition row into the competition data frame
        contest_df.loc[-1] = row_dict
        contest_df.index = contest_df.index + 1

        print "Completed:", i

# house keeping and write-out
contest_df["contest_number"] = contest_df["contest_number"].astype(int)
contest_df = contest_df.drop_duplicates(subset="contest_number", keep="last")
contest_df = contest_df.reset_index(drop=True)
contest_df.to_pickle("fresh_pkls/contest_df.pkl")

result_df["contest_key"] = result_df["contest_key"].astype(int)
result_df = result_df.drop_duplicates(keep="last")
result_df = result_df.reset_index(drop=True)
result_df.to_pickle("fresh_pkls/result_df.pkl")
