# Golf Predictor
![GitHub commit activity](https://img.shields.io/github/commit-activity/w/gjakubik/golfPredictor) ![GitHub last commit](https://img.shields.io/github/last-commit/gjakubik/golfPredictor)

Golf tournament outcome prediction models based on data scraped from the [PGA Tour](https://www.pgatour.com/)


### Data Collection
1. Install Requirements
    ```
    $ pip3 install -r scraper/requirements.txt
    ```
2. Fetch and Aggregate Data
    - Use Shell script to do following:
        - Crawl the PGA Tour website for data in several categories for each year in specified range (using custom [scrapy module](scraper/pga_scrapy/spiders/pga_stats.py))
        - Next, concat data from each year and rename columns to create a single file with all aggregated data (using [`combiner.py`](combiner.py)) at [`data/combined.csv`](data/combined.csv)
        ```
        $ ./fetch_all_data.sh 2004 2019
        Fetching Data for year: 2004
        Fetching Data for year: 2005
        ...
        Fetching Data for year: 2019
        Combining Data
        ...
        ```
    - Collect world golf ranking data (from 2004 to 2019), and save to [`owgr_2004-2019.csv`](owgr_2004-2019.csv)
        ```
        $ ./fetch-owgr.py
        ```
### Run Models
1. Start jupyter notebook server
    - VSCode extensions makes this easy, but another option is running
        ```
        $ jupyter notebook
        ```
        then using a browser to navigate to the specified URL, which will be something like http://localhost:8888/?token=YOUR_TOKEN
2. Run each cell in the main jupyter notebook file at [`model/golf_predictor_v1.ipynb`](model/golf_predictor_v1.ipynb)

