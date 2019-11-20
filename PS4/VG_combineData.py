## last updated 11/19/19

## script to merge multiple datasets into single dataframe for analysis

# load necessary packages
import csv
import sys
import pandas as pd 
import numpy as np
import fuzzywuzzy as fw

# read in the csv of video game data
vg_csv = pd.read_csv("/Users/austindreyer/Documents/Python/Python_VideoGame_Project/videogame_scores_nodup.csv")
vg_devs = pd.read_csv("/Users/austindreyer/Documents/Python/Python_VideoGame_Project/videogame_devs.csv")

# and confirm they were read in as a dataframes
isinstance(vg_csv, pd.DataFrame)
isinstance(vg_devs, pd.DataFrame)

# create new data frame that merges the two existing based on developer name
vg_data = vg_csv.merge(vg_devs, how = 'left')

# inspect new data frame
vg_data.head()


# remove rows without a matching developer
vg_nonan = vg_data.dropna()

# inspect new data frame 
vg_nonan.head()

# check the length of the merged data frame as compared to original
len(vg_data.index)-len(vg_nonan.index)


# given the extreme loss of data based on matching of developer name, try to introduce fuzzy matching to 
# enable partial developer name matches to count for merging 
# to do so, need a function to match strings using fuzzywuzzy (added package install to start)

def match_name(name, list_names, min_score=0):
    # start with -1 score in case no matches
    max_score = -1
    # empty name for in case of no match as well
    max_name = ""
    # Iternating over all names in the dev data frame
    for orgname in list_names:
        #Finding fuzzy match score
        score = fuzz.partial_ratio(name, orgname)
        # Checking if we are above our threshold and have a better score
        if (score > min_score) & (score > max_score):
            max_name = orgname
            max_score = score
    return (max_name, max_score)


# need to generate dataframe of just the rows with missing values to fuzzy match
vg_nans = vg_data[pd.isnull(vg_data['status'])]

# confirm the correct number of rows in NaNs table as it should match the difference
# in dataframe lengths found above
len(vg_nans.index)


# Check dataframe structure
vg_nans.head()

# Check dataframe structure
vg_devs.head()


# then use the function to test matching names starting 
# with an empty list to store outputs
match_list = []

# use 
for name in vg_nans.Developer:
    # use function to find best match, set threshold for strength of match (0-100)
    match = match_name(name, vg_devs.Developer, 50)
    
    # store iterated data in dict
    dict_ = {}
    dict_.update({"dev_name" : name})
    dict_.update({"dev_match" : match[0]})
    dict_.update({"score" : match[1]})
    match_list.append(dict_)
    
vg_match = pd.DataFrame(match_list)

# show results that have a match >50
vg_match[vg_match['score'] >50]

# check for increase match threshold to avoid non informative matches like only the word "Studios"
vg_98 = vg_match[vg_match['score'] >98]
vg_98.head()

# and check how many entries exist for fuzzy matched names
vg_index = list(vg_98.index.values)
len(vg_index)


# confirm the only developers left with that include "Studios" have multiple word matches
studio_devs = vg_98[vg_98['dev_match'].str.contains("Studio")]
# set viewer to allow inspection of all rows (Jupyter notebook)
#pd.set_option('display.max_rows', 500)
# view output
studio_devs


# now, need to go back to original dataframe and replace the old developer names with the
# corrected names that have the additional data associated. To do this, will use the dataframe
# vg_98 as a dictionary to replace Developer column in original dataframe

# create copy of original vg_csv data "Developer" column to replace values
df1 = pd.DataFrame(vg_csv.Developer, columns = ['developer'])

# replace the names of df1 using the dictionary of vg_98
df1['developer'] = df1['developer'].replace(vg_98.set_index('dev_name')['dev_match'].dropna())

# compare the original Developer names with the updated ones
pd.concat([vg_csv.Developer, df1], axis=1, keys=['old', 'new'])

# replace the original Developer column of vg_csv with corrected matched column

vg_csv['developer'] = df1['developer']

vg_csv.head()

# re-join the modified dataframe with the developer dataframe
vg_data_fin = vg_csv.merge(vg_devs, how = 'left')

# remove the NaNs from the data set
vg_data_fin = vg_data_fin.dropna()

# check the number of entries in final dataframe, should match the sum of lengths of originally 
# joined table (vg_nonan) and the vg_98 table
len(vg_data_fin.index) == sum([len(vg_nonan.index),len(vg_98.index)])

# write the corrected csv with added developer details as a csv
vg_data_fin.to_csv("/Users/austindreyer/Documents/Python/Python_VideoGame_Project/PS4videogame_data_dev.csv", index = False, header = True)

