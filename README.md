# KCBS Competition Stats

This repository contains all the code driving my KCBS Competition Data web app at [kcbstats.red](https://kcbstats.red/states). The repository is broken up into two main sections. First, I have a handful of Python web scraping and data processing scripts which are responsible for building the team, contest and state profiles dispayed on the website. Second, I have the actual website HTML/CSS and Angular4 Typescript code.

You can read about the project below, or on the website's [about page](https://kcbstats.red/about)

## Web Scraping

The data for this website was pulled from the KCBS's [events pages](https://www.kcbs.us/events). The Python code in this project downloads competition HTML, cleans it up, extract any features used on the site, and then merges it with the existing JSON data. Currently the output of the script is five JSON files which I manually upload to Firebase.

### Data Quirks
 * Competitions from outside the US are currently excluded
 * Teams were identified by their unique names which probably caused some inaccuracies
 * A team needed at least one 'overall' finish to be included in the dataset
 * In total, this dataset contains over 10,000 teams and ~2,000 competitions

## Website

I built the website using Angular4 on the front-end, and Firebase for the database + hosting. All the typescript, html and css lives in the src folder. There are a number of auto-generated files in the project folder that I didn't include here.

## Check it out!

Starts on a big-time team like [Iowa's Smokey D's BBQ](https://kcbstats.red/team/6377). They have a long history of strong performances. You can also explore by state. [Kansas](https://kcbstats.red/state/ks) has a ton of competitions, including a few with over 600 teams! The last contest I judged at was a [Sam's Club Nation BBQ Tour in CT](https://kcbstats.red/contest/7123) where MA locals [Smokin Hoggz BBQ](https://kcbstats.red/team/11410) took third place.

[Start from home: Pick a state](https://kcbstats.red) If you're looking for a specific competition or team, you'll need to start by picking a state. Hosting is cheaper and pages load faster if I don't have to access all 15,000 team records for every user! If you're desperate to search a competition you can use the KCBS [events page](https://www.kcbs.us/events) and copy-paste the target competition's 'contest number' into the url slug kcbstats.red/contest/#### 

## Full Data Set

The full dataset is available on Kaggle. https://www.kaggle.com/jaysobel/kansas-city-barbeque-society-competition-results
