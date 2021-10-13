# This file uses the year_combiner.py program to 

import pandas as pd
import os
import re

from year_combiner import combineYear

def main():

    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

    # Run year combiner on each year
    year_dfs = []
    for year_dir in os.scandir(data_dir):
        print(year_dir.name)
        year_dfs.append(combineYear(os.path.join(data_dir, year_dir.name), year_dir.name))

    start = 0

    for i, df in enumerate(year_dfs):
        end = start + len(df)
        indicies = [i for i in range(start, end)]
        df[f"INDEX_{i}"] = indicies
        df.reset_index(inplace=True)
        df.set_index(f"INDEX_{i}", inplace=True)
        start = end

    for df in year_dfs:
        df = df.loc[~df.index.duplicated(keep='first')]
        print(df.columns)
        print(df)

    print(year_dfs)
    # TODO: then concatenate all their dataframes
    concat_df = pd.concat(year_dfs, ignore_index=True)

    print(concat_df)
    pass

if __name__ == '__main__':
    main()