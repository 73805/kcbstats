# kcbstats

This repository contains the code behind my KCBS competition and teams website at [kcbstats.red](https://kcbstats.red/states).

You can read about the project below, or on the website's [about page](https://kcbstats.red/about)

## Web Scraping

The data for this website was pulled from the KCBS's [events pages](https://www.kcbs.us/events). I downloaded every event result page since the scoring changes in July 2013. I parsed each competition's context and result information into a table, cleaned up the rows, and extracted a few extra features to build records for states, contests and teams. 

### Data Quirks

Teams were identified by their unique names which probably caused some inaccuracies. Competitions from outside the US were excluded for V1 of this project. A team needed at least one 'overall' finish to be included in this data set. There are roughly 15,000 teams and 1,500 competitions on this website! Competition ID's (the last URL segment) are straight from the KCBS, so you can use their events page search to find the route to a competition on this website.

## Website Tech

I built the website using Angular4 on the front-end, and Firebase for the database + hosting. All the typescript, html and css lives in the src folder. The app was initiated with the Angular4 CLI; there were a number of extra files in the project that I did not include here.

## Check it out!

[Iowa's Smokey D's BBQ](https://kcbstats.red/team/6377) is a good team to check out. They have been competing since before the July start-point of this dataset and all the way through to a couple days before the first scrape. There are plenty of perfect-180 gold bars in their scoring history, and Iowa has a great state flag!
