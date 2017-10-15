from get_links import get_links
from download_html import download_html
from parse_html import parse_html
from clean_data import clean_data
from filter_data import filter_data
from update_dictionaries import update_dictionaries
from jsonify import jsonify

countries = [1]
year_months = {2017: [8, 9, 10]}


# get the event URLs for the target date range and countries
links = get_links(countries, year_months)

# download the HTML and store the file names in a list
fnames = download_html(links)


# walk the files and build a dataframe
contest_df, result_df = parse_html(fnames)

# clean up the data frame and convert features
contest_df, result_df = clean_data(contest_df, result_df)

# clean up the data frame and convert features
new_contest_df, new_result_df = filter_data(contest_df, result_df)

# update the profile dictionaries
update_dictionaries(new_contest_df, new_result_df)

# convert to JSON
jsonify()