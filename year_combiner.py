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

#Function that combines all of the data in a year into one pandas dataframe joined on name and returns it
def combineYear(data_dir):

    # read rankings
    df_owgr = pd.read_csv(os.path.join(data_dir, "POINTSRANKINGS_Official_World_Golf_Ranking.csv"))

    for filename in os.listdir(data_dir):
        if not filename.endswith(".csv") or filename == "POINTSRANKINGS_Official_World_Golf_Ranking.csv":
            continue

        df1 = pd.read_csv(os.path.join(data_dir, filename))

        # delete unofficial rankings to avoid confusion
        for key, value in df1.iteritems():
            if "RANK" in key:
                del df1[key]

        # merge 1 and 2
        # TODO: Change to outer join if needed
        df_owgr = pd.merge(df1, df_owgr, on = "PLAYER NAME")
        df_owgr.set_index("PLAYER NAME", inplace = True)

    return df_owgr
