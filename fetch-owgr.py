#!/usr/bin/env python3

import http.client
import bs4
import ssl
import pandas as pd


conn = http.client.HTTPSConnection("www.pgatour.com", context=ssl._create_unverified_context())

yearly_rankings = []

START_YEAR = 2003
END_YEAR = 2022

for year in range(START_YEAR, END_YEAR):
    print("Fetching data for year:", year)

    url = f"/stats/stat.186.y{year}.html"
    conn.request("GET", url)
    resp = conn.getresponse()
    data = resp.read()

    # locate table
    reader = bs4.BeautifulSoup(data, "lxml")
    table = reader.find("table", {"id": "statsTable"})

    # convert table to pandas dataframe
    df = pd.read_html(str(table))[0]
    
    # rename cols
    df.rename(columns={"PLAYER NAME": "name", df.columns[0]: "current_rank"}, inplace=True)

    # extract relevant cols and add to list
    name_ranking = df[['name', 'current_rank']]
    yearly_rankings.append(name_ranking)

dataframes = []

for i, yearly_ranking in enumerate(yearly_rankings[:-2]):
    next_year_rank = yearly_rankings[i+1].rename(columns={"current_rank": "rank_year_plus_one"})
    year_after_rank = yearly_rankings[i+2].rename(columns={"current_rank": "rank_year_plus_two"})
    
    new_df = pd.merge(yearly_ranking, next_year_rank, on="name")
    new_df = pd.merge(new_df, year_after_rank, on="name")
    new_df['year'] = START_YEAR + i

    dataframes.append(new_df)

res_df = pd.concat(dataframes, ignore_index=True)

if res_df is not None:
    print("Saving to CSV")
    res_df.to_csv(f"owgr_{START_YEAR}-{END_YEAR}.csv")
