#!/usr/bin/env python3

import pandas as pd
import os
import sys


table_filter = {
    "OFF_THE_TEE_SG_Tee-to-Green.csv": {
        "PLAYER NAME": "name",
        "SG:OTT": "sg_ott_avg",
        "SG:APR": "sg_apr_avg",
        "SG:ARG": "sg_arg_avg",
        "MEASURED ROUNDS": "rounds"
    },
    "PUTTING_SG_Putting.csv": {
        "PLAYER NAME": "name",
        "AVERAGE": "sg_p_avg"
    },
    "AROUND_THE_GREEN_Scrambling.csv": {
        "PLAYER NAME": "name",
        "%": "scrambling_pct"
    },
    "SCORING_Scoring_Average.csv": {
        "PLAYER NAME": "name",
        "AVG": "adj_scoring_avg"
    },
    "OFF_THE_TEE_Driving_Accuracy_Percentage.csv": {
        "PLAYER NAME": "name",
        "%": "driving_acc_pct"
    },
    "APPROACH_THE_GREEN_Greens_in_Regulation_Percentage.csv": {
        "PLAYER NAME": "name",
        "%": "gir_pct"
    },
    "OFF_THE_TEE_Driving_Distance.csv": {
        "PLAYER NAME": "name",
        "AVG.": "driving_dist_avg"
    },
    "MONEYFINISHES_Top_10_Finishes.csv": {
        "PLAYER NAME": "name",
        "TOP 10": "top_tens"
    },
    "POINTSRANKINGS_Official_World_Golf_Ranking_CURRENT.csv": {
        "PLAYER NAME": "name",
        "AVG POINTS": "owgr_points_current_avg"
    },
    "POINTSRANKINGS_Official_World_Golf_Ranking_NEXT.csv": {
        "PLAYER NAME": "name",
        "RANK THIS WEEK": "next_years_rank"
    }
}


def combine_year(data_dir):
    res_df = None

    for file in os.scandir(data_dir):
        if not file.name.endswith(".csv"):
            continue

        if file.name == "combined.csv":
            print("Noticed combined.csv file...  Skipping", file=sys.stderr)
            continue

        if file.name not in table_filter:
            print("Unrecognized CSV file:", file.path, file=sys.stderr)
            continue
        
        new_df = pd.read_csv(file.path)

        # seemingly there is a bug in pandas, so this is needed
        if "RANK THIS WEEK" in table_filter[file.name]:
            table_filter[file.name][new_df.columns[0]] = table_filter[file.name]["RANK THIS WEEK"]
            del table_filter[file.name]["RANK THIS WEEK"]
        
        # throw out un-needed columns
        columns_to_keep = list(table_filter[file.name].keys())
        new_df = new_df[columns_to_keep]

        # rename columns
        new_df.rename(columns=table_filter[file.name], inplace=True)

        # merge with running dataframe
        if res_df is None:
            res_df = new_df
        else:
            res_df = pd.merge(res_df, new_df, on="name")
    
    res_df['year'] = os.path.basename(data_dir)
    return res_df


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
            print(year_dir.name, "is not a directory, skipping...", file=sys.stderr)
            continue

        df = combine_year(year_dir.path)
        dataframes.append(df)
    
    res_df = pd.concat(dataframes, ignore_index=True)
    
    print("Saving combined file to:", outfile)
    res_df.to_csv(outfile)


if __name__ == '__main__':
    main()