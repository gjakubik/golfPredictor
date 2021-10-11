# with help of - https://stackoverflow.com/questions/54383305/merge-two-csv-files-based-on-a-data-from-the-first-column
# with help of - https://www.geeksforgeeks.org/update-column-value-of-csv-in-python/
# with help of - https://www.geeksforgeeks.org/adding-new-column-to-existing-dataframe-in-pandas/
# with help of - https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.insert.html
# with help of - https://stackoverflow.com/questions/13411544/delete-a-column-from-a-pandas-dataframe
# with help of - https://stackoverflow.com/questions/54655304/how-to-iterate-over-a-column-headers-and-row-values-in-pandas
# with help of - https://stackoverflow.com/questions/10377998/how-can-i-iterate-over-files-in-a-given-directory

# Explanation - PUT THIS FILE IN THE FOLDER OF A GIVEN YEAR OF STATS, IT WILL COMBINE THEM
# NOTE: do not change the excel file name for owgr file

import pandas as pd
import sys
import os

if len(sys.argv) != 2:
    print("Incorrect number of args")
    exit(1)

year = sys.argv[1]



df_owgr = pd.read_csv("POINTSRANKINGS_Official_World_Golf_Ranking.csv")

for filename in os.listdir("."):
    if filename.endswith(".csv") and filename != "POINTSRANKINGS_Official_World_Golf_Ranking.csv":
        df1 = pd.read_csv(filename)
        # delete unofficial rankings to avoid confusion
        for key, value in df1.iteritems():
            if "RANK" in key:
                del df1[key]
        # merge 1 and 2
        df_owgr = pd.merge(df1, df_owgr, on = "PLAYER NAME")
        df_owgr.set_index("PLAYER NAME", inplace = True)



df_owgr.insert(0, "YEAR", year)
df_owgr.to_csv("data_" + str(year) + ".csv")
