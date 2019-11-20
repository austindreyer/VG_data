## last updated 11/19/19

## script to inspect dataframe for duplicate entries

# import the CSV module, knows how to handle csv files, and sys to catch error
import csv
import sys
import pandas as pd 
import numpy as np


# check python version
sys.version

# read in the csv of video game score data
vg_csv = pd.read_csv("/Users/austindreyer/Documents/Python/Python_VideoGame_Project/VG_data/PS4/ps4_videogame_scores.csv")

# and confirm it was read in as a dataframe
isinstance(vg_csv, pd.DataFrame)

# inspecting data for data type, need function to test for float based to prevent issues of data manipulation
def is_float(value):
  try:
    float(value)
    return True
  except:
    return False

is_float(vg_csv.iloc[:,3])

# look at the top of the table to inspect
vg_csv.head(1)

# and inspect table to confirm the column names are not part of the structure
print(vg_csv.iloc[0,0])

# can sort the data frame and create new table
vg_csv_sorted = vg_csv.sort_values("developer")

vg_csv_sorted.head(3)

# add column to original data frame to check for duplicate entries, video game title is the only concern for duplicates here
vg_csv['is_duplicated'] = vg_csv['vg_name'].duplicated()

# sum the duplicated column to see how many duplicates there are
vg_csv['is_duplicated'].sum()

# find the duplicate
vg_csv[vg_csv['is_duplicated']]

# view the dupliate rows together 
vg_csv[vg_csv['vg_name'] == 'Asterix & Obelix XXL 2']


# investigate discrepencies to determine the same game had the developer 
# listed for one entry (Etranges Libellules) and the publisher for 
# the second dupliate entry (Anuman Interactive). Therefore, modify the
# correct developer row using the row indices to incorporate all scores, 
# then delete duplicate entry

# first correct avg score
vg_csv.iloc[194,3] = np.mean([float(vg_csv.iloc[194,3]), float(vg_csv.iloc[195,3])])

# then number of reviews
vg_csv.iloc[194,4] = sum([float(vg_csv.iloc[194,4]), float(vg_csv.iloc[195,4])])

# and delete dupliate row (axis = 0 for row, 1 for column)
vg_nodup = vg_csv.drop(vg_csv.index[195], axis = 0)

# confirm no duplicate exsits and appropriate columns have been changed
print(vg_nodup['is_duplicated'].sum())

vg_nodup[vg_nodup['vg_name'] == 'Asterix & Obelix XXL 2']

# remove duplicated identifier column
vg_nodup.drop('is_duplicated', axis = 1, inplace = True)

# confirm column has been deleted
vg_nodup.head()

# write the new corrected dataframe to a csv

vg_nodup.to_csv("/Users/austindreyer/Documents/Python/Python_VideoGame_Project/VG_data/PS4/videogame_scores_nodup.csv", index = False, header = True)

