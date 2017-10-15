from selenium import webdriver

# countries: a list of country codes (1 for USA)
# year_months a dictionary with year numbers as keys, and a list of month numbers as values
# a month-list of [0] gets all months (as per the website)
def get_links(countries, year_months):
    driver = webdriver.Chrome()
    chrome_path = r'C:\Users\Jay\Desktop\Applied Data Science\project\chromedriver.exe'
    links = []
    for country in countries:
        for year in year_months.keys():
            for month in year_months[year]:
                url = ("http://www.kcbs.us/events/" +
                          str(year) + "/" +
                          str(month) + "/" +
                          str(country))
                # go to a contest listing page
                driver.get(url)
                a_elements = driver.find_elements_by_css_selector(
                    "#mainContentInterior > table > tbody > tr > td > strong > a")
                for j, a_tag in enumerate(a_elements):
                    href = a_tag.get_attribute("href")
                    links.append(href)
    print "Retrieved contest URLs successfully"
    return links
