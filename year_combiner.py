#!/usr/bin/env python3

# with help of - https://stackoverflow.com/questions/54383305/merge-two-csv-files-based-on-a-data-from-the-first-column
# with help of - https://www.geeksforgeeks.org/update-column-value-of-csv-in-python/
# with help of - https://www.geeksforgeeks.org/adding-new-column-to-existing-dataframe-in-pandas/
# with help of - https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.insert.html
# with help of - https://stackoverflow.com/questions/13411544/delete-a-column-from-a-pandas-dataframe
# with help of - https://stackoverflow.com/questions/54655304/how-to-iterate-over-a-column-headers-and-row-values-in-pandas
# with help of - https://stackoverflow.com/questions/10377998/how-can-i-iterate-over-files-in-a-given-directory

import pandas as pd
import sys
import os


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
        "AVG POINTS": "owgr_points_next_avg"
    }
}


#Function that combines all of the data in a year into one pandas dataframe joined on name and returns it
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

    return res_df


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} DATA_YEAR_DIR", file=sys.stderr)
        sys.exit(1)
    
    data_dir = sys.argv[1]
    out_file = os.path.join(data_dir, "combined.csv")

    # combine
    print("Combining Files")
    res = combine_year(data_dir)

    # export
    print("Exporting Result to:", out_file)
    res.to_csv(out_file)


if __name__ == "__main__":
    main()
