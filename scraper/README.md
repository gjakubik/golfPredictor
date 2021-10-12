# PGA Tour Website Scraper

Created a small web scraper to collect the stats from the pgatour.com website

## Setup

Setup Virtual Environment
```
$ python3 virtualenv venv
```
Activate Virtual Environment 
```
$ source venv/bin/activate
```
Install the requirements
```
$ pip3 install -r "requirements.txt"
```

Run crawler 
```
$ scrapy crawl pga_stats -a year=YEAR
```

## Process

1) The web crawler extracts the links for each of the 'stats' landing pages.  
2) The spider parses the "stats" landing page to gather all the links for the individual stats
3) The spider crawls through each of those links and yields the name of the stat and the html table
4) The item is passed to a pipeline where the `pandas` `read_html` function is used to parse out the table. 
5) The item is written to a csv file with `to_csv` and named the name of the stat. 

