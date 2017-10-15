from utilities import openDf

import requests


def remove_suffix(url):
    return url.replace(".html", "").strip()


# links: list of contest urls to download
def download_html(links):
    # read in the master dataframe
    contest_df = openDf("contest_df_master")
    # filter out URL's which are already recorded in the contest_df
    old_links = list(contest_df["url"])
    old_links = [remove_suffix(url) for url in old_links]
    links = [remove_suffix(url) for url in links]
    new_links = list(set(links) - set(old_links))

    fnames = []
    fpath = "contest_html/"
    for i, url in enumerate(new_links):
        # construct the filename by concatenating key with url-name
        fname = url.split("/")
        fname = fname[-2] + "-" + fname[-1] + ".html"
        fname = fpath + fname
        # get the contest page
        res = requests.get(url + ".html")
        if res.status_code == requests.codes.ok:
            # save out the html file
            with open(fname, 'wb') as outfile:
                for chunk in res.iter_content(chunk_size=100000):
                    outfile.write(chunk)
            fnames.append(fname)
        else:
            print "Request code not ok!"
            print url
            return False
    print "Downloaded HTML successfully"
    return fnames
