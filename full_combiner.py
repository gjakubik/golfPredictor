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

    for df in year_dfs:
        print(df)

    # TODO: then concatenate all their dataframes
    concat_df = pd.concat(year_dfs, axis=0)

    print(concat_df)
    pass

if __name__ == '__main__':
    main()