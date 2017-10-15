import bs4
import pandas as pd
import re
import string
import os

def parse_html(fnames):
    # define template rows for the contest and result dataframes
    contest_template = {"id": "NA", "url": "NA", "title": "NA", "location": "NA", "date_str": "NA",
                        "prize": "NA", "cbj_percentage": "NA", "champ_bool": "NA", "has_results": "NA",
                        "has_core": "NA", "has_extra": "NA", "skewed_overall": "NA", "standard_scoring": "NA"}

    result_template = {"category": "NA", "team_name": "NA", "score": "NA", "place": "NA"}

    standard_cats = ["chicken", "ribs", "pork", "brisket", "overall"]

    contest_df = pd.DataFrame(columns=contest_template.keys())
    result_df = pd.DataFrame(columns=result_template.keys())

    do_all = False
    if do_all:
        directory = "contest_html/"
        for i, clink in enumerate(os.listdir(directory)):
            fnames.append(directory + clink)

    for i, fname in enumerate(fnames):
        with open(fname) as fp:
            contest = bs4.BeautifulSoup(fp, "html.parser")

        # initiate a new default row
        new_row = contest_template.copy()

        # reconstructing the url
        fsplit = fname.split("-")
        fsplit[0] = fsplit[0].replace('contest_html/', '')
        url = fsplit[0] + "/" + "-".join(fsplit[1:])
        url = "http://www.kcbs.us/event/" + url[:-5]
        new_row["url"] = url

        # title
        title_handle = contest.select(".event_head")
        if len(title_handle) > 0:
            title = title_handle[0].text.strip()
            new_row["title"] = title

        # location / date as string
        sub_head = contest.select("#event_subhead")
        if len(sub_head) > 0:
            sub_head = sub_head[0]
            sub_head = sub_head.text.split('\n\t\t')
            if len(sub_head) == 3:
                location = sub_head[1].strip()
                date_str = sub_head[2].strip()
                new_row["location"] = location
                new_row["date_str"] = date_str

        # contextual data - keys match website labels
        meta_dict = {"website": "NA", "kcbs reps": "NA", "contest number": "NA",
                     "prize money": "NA", "cbj percentage": "NA"}
        p_tags = contest.select("p")
        for tag in p_tags:
            text = tag.text
            # get a hold of the unlabelled meta-data <p> tag
            if "Contest Number:" in text:
                meta_data = text.split("\n")
                # html tags are unlabelled by there are consistent plain text 'labels'
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

                new_row["id"] = int(meta_dict["contest number"])
                new_row["prize"] = meta_dict["prize money"]
                new_row["cbj_percentage"] = meta_dict["cbj percentage"]

        # State Championship Boolean
        champ_bool = False
        champ_text = contest.select('.float20 p strong em')
        if len(champ_text) > 0:
            if champ_text[0].text.strip() == "STATE CHAMPIONSHIP":
                champ_bool = True
        new_row["champ_bool"] = champ_bool

        # Contest Results - initiating some variables first
        temp_df = pd.DataFrame(columns=result_template.keys())
        extra_cats = 0
        has_results = False
        standard_cats = ["chicken", "ribs", "pork", "brisket", "overall"]

        result_tables = contest.select("div.grid07.float20 table.contestResults")
        if len(result_tables) > 0:
            has_results = True
            # for each table of results
            for table in result_tables:
                rows = table.select('tr')
                if len(rows) > 0:
                    # normalize table headers a bit before using them as category keys
                    table_name = rows[0].text.strip().lower()
                    table_name = str(re.sub(r'\d+', '', table_name))
                    table_name = table_name.translate(None, string.punctuation)
                    table_name = table_name.strip()
                    if table_name == "pork ribs":
                        table_name = "ribs"
                    if table_name in standard_cats:
                        # cross this category off the list
                        standard_cats.remove(table_name)
                        # for each (non-header) row in each table (unfortunately)
                        for q in range(1, len(rows)):
                            res_row = result_template.copy()
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
        new_row["has_results"] = has_results

        # has all the standard categories
        new_row["has_core"] = not(bool(len(standard_cats)))

        # has extra categories
        new_row["has_extra"] = bool(extra_cats)

        # Maximum overall score over 720 (indicates non-standard category scoring)
        over_720 = False
        max_overall = temp_df[temp_df['category'] == "overall"]["score"].max()
        if max_overall > 720:
            over_720 = True

        new_row["skewed_overall"] = over_720

        # has standard scoring
        new_row["standard_scoring"] = (new_row["has_core"] and not(new_row["skewed_overall"]))

        # append the temporary results df to the master results df
        temp_df['contest_id'] = int(meta_dict["contest number"])
        result_df = pd.concat([result_df, temp_df])

        # insert the competition row into the competition data frame
        contest_df.loc[-1] = new_row
        contest_df.index = contest_df.index + 1

        print "Parsed html file:", i

    # house keeping
    contest_df["id"] = contest_df["id"].astype(int)
    contest_df = contest_df.drop_duplicates(subset="id", keep="last")
    contest_df = contest_df.reset_index(drop=True)

    result_df["contest_id"] = result_df["contest_id"].astype(int)
    result_df = result_df.drop_duplicates(keep="last")
    result_df = result_df.reset_index(drop=True)

    print "Finished parsing html"

    return contest_df, result_df
