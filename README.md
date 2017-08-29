# kcbstats

This repository contains the code behind my KCBS competition and teams website at [kcbstats.red](https://kcbstats.red/states).

You can read about the project below, or on the website's [about page](https://kcbstats.red/about)

## Web Scraping

The data for this website was pulled from the KCBS's [events pages](https://www.kcbs.us/events). I downloaded every event result page since the scoring changes in July 2013. I parsed each competition's context and result information into a dataframe with rows like "is_state_championship", "prize", and "date_string". Next, I cleaned up the data and extracted a few extra features like 'has_standard_categories.' I used iterated the cleaned competition data to build profiles for states and teams. 

### Data Quirks
 * Competitions from outside the US were excluded for V1 of this project
 * Teams were identified by their unique names which probably caused some inaccuracies
 * A team needed at least one 'overall' finish to be included in the dataset
 * In total, this dataset contains over 10,000 teams and ~1,500 competitions

## Website Tech

I built the website using Angular4 on the front-end, and Firebase for the database + hosting. All the typescript, html and css lives in the src folder. There are a number of auto-generated files in the project folder that I didn't include here.

## Check it out!

[Iowa's Smokey D's BBQ](https://kcbstats.red/team/6377) is a good team to check out. They have been competing since before the July start-point of this dataset and all the way through to a couple days before the first scrape.

[Pick a state](https://kcbstats.red) If you want to find a specific competition or team, you'll need to start by picking a state. Hosting is cheaper and pages load faster if I don't have to access all 15,000 team records for every user! You can search for a competition on the KCBS [events pages](https://www.kcbs.us/events) and copy-paste its 'contest number' into the url slug /contest/#### if you don't know where it was held.
