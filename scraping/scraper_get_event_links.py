import pickle

from selenium import webdriver

chrome_path = r'C:\Users\Jay\Desktop\Applied Data Science\project\chromedriver.exe'

driver = webdriver.Chrome()

# Start Scraping

contest_links = {}
years = range(2013, 2018)

for year in years:
    if year == 2013:
        pageUrl = "http://www.kcbs.us/events/" + str(year) + "/0/1"
    else:
        pageUrl = "http://www.kcbs.us/events/" + str(year) + "/0/1"
    contest_links[year] = []
    # go to a contest listing page
    driver.get(pageUrl)
    # select all the contest <a> tag elements
    a_tag_elements = driver.find_elements_by_css_selector("#mainContentInterior > table > tbody > tr > td > strong > a")
    # iterate through the selected elements
    for j, a_tag in enumerate(a_tag_elements):
        href = a_tag.get_attribute("href")
        contest_links[year].append(href)

# Save the URL list to a pkl file
with open('fresh_pkls/contest_links.pkl', 'wb') as f:
    pickle.dump(contest_links, f)
