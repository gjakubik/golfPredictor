#!/usr/bin/env python3

import pandas as pd
import os
import sys

from year_combiner import combine_year


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} DATA_DIR", file=sys.stderr)
        sys.exit(1)

    data_dir = sys.argv[1]
    outfile = os.path.join(data_dir, "combined.csv")

    # Run year combiner on each year
    dataframes = []
    for year_dir in os.scandir(data_dir):
        if year_dir.name == "combined.csv":
            print("Noticed combined.csv file... Skipping", file=sys.stderr)
            continue

        if not os.path.isdir(year_dir):
            print(year_dir, "is not a directory, skipping...", file=sys.stderr)
            continue

        df = combine_year(year_dir.path)
        dataframes.append(df)
    
    res_df = pd.concat(dataframes, ignore_index=True)
    
    print("Saving combined file to:", outfile)
    res_df.to_csv(outfile)

    # return for fun
    return res_df


if __name__ == '__main__':
    main()