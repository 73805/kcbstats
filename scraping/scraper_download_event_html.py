import requests
import pickle

with open('pkls/contest_links.pkl', 'rb') as f:
    contest_links = pickle.load(f)

# run for 2013-2016 later
target_years = [2014, 2015, 2016]

for year in target_years:
    fpath = "contest_html/" + str(year) + "/"
    year_links = contest_links[year]
    for i, link in enumerate(year_links):
        # get the contest page
        res = requests.get(link)
        if res.status_code == requests.codes.ok:
            # construct the filename
            fname = link.split("/")
            fname = fname[-2] + "-" + fname[-1] + ".html"
            fname = fpath + fname
            # write out the HTML
            with open(fname, 'wb') as fd:
                for chunk in res.iter_content(chunk_size=100000):
                    fd.write(chunk)
            print "Done Writing:", i
        else:
            print "Request error!"
            print link
            break