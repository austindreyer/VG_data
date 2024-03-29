## last updated 11/19/19

## Script to merge multiple datasets into single dataframe for analysis

# Load necessary packages
import sys
import pandas as pd 
import numpy as np
from fuzzywuzzy import fuzz

# Read in the csv of video game data
vg_csv = pd.read_csv("/Users/austindreyer/Documents/Python/Python_VideoGame_Project/videogame_scores_nodup.csv")
vg_devs = pd.read_csv("/Users/austindreyer/Documents/Python/Python_VideoGame_Project/videogame_devs.csv")

# And confirm they were read in as a dataframes
isinstance(vg_csv, pd.DataFrame)
isinstance(vg_devs, pd.DataFrame)

# Create new data frame that merges the two existing based on developer name
vg_data = vg_csv.merge(vg_devs, how = 'left')

# Inspect new data frame
vg_data.head()


# Remove rows without a matching developer
vg_nonan = vg_data.dropna()

# Inspect new data frame 
vg_nonan.head()

# Check the length of the merged data frame as compared to original
len(vg_data.index)-len(vg_nonan.index)


# Given the extreme loss of data based on matching of developer name, try to introduce fuzzy matching to 
# enable partial developer name matches to count for merging 
# to do so, need a function to match strings using fuzzywuzzy (added package install to start)

def match_name(name, list_names, min_score=0):
    '''Function to find names that are close matches to one another'''
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


# Need to generate dataframe of just the rows with missing values to fuzzy match
vg_nans = vg_data[pd.isnull(vg_data['status'])]

# Confirm the correct number of rows in NaNs table as it should match the difference
# in dataframe lengths found above
len(vg_nans.index)


# Check dataframe structure
vg_nans.head()

# Check dataframe structure
vg_devs.head()


# Then use the function to test matching names starting 
# with an empty list to store outputs
match_list = []

# Find name matches
for name in vg_nans.developer:
    # use function to find best match, set threshold for strength of match (0-100)
    match = match_name(name, vg_devs.developer, 50)
    
    # store iterated data in dict
    dict_ = {}
    dict_.update({"dev_name" : name})
    dict_.update({"dev_match" : match[0]})
    dict_.update({"score" : match[1]})
    match_list.append(dict_)
    
vg_match = pd.DataFrame(match_list)

# Show results that have a match >50
vg_match[vg_match['score'] >50]

# Check for increase match threshold to avoid non informative matches like only the word "Studios"
vg_98 = vg_match[vg_match['score'] >98]
vg_98.head()

# And check how many entries exist for fuzzy matched names
vg_index = list(vg_98.index.values)
len(vg_index)


# Confirm the only developers left with that include "Studios" have multiple word matches
studio_devs = vg_98[vg_98['dev_match'].str.contains("Studio")]
# Set viewer to allow inspection of all rows (Jupyter notebook)
#pd.set_option('display.max_rows', 500)
# View output
studio_devs


# Now, need to go back to original dataframe and replace the old developer names with the
# corrected names that have the additional data associated. To do this, will use the dataframe
# vg_98 as a dictionary to replace Developer column in original dataframe

# Create copy of original vg_csv data "Developer" column to replace values
df1 = pd.DataFrame(vg_csv.developer, columns = ['developer'])

# Replace the names of df1 using the dictionary of vg_98
df1['developer'] = df1['developer'].replace(vg_98.set_index('dev_name')['dev_match'].dropna())

# Compare the original Developer names with the updated ones
pd.concat([vg_csv.developer, df1], axis=1, keys=['old', 'new'])

# Replace the original Developer column of vg_csv with corrected matched column

vg_csv['developer'] = df1['developer']

vg_csv.head()

# Re-join the modified dataframe with the developer dataframe
vg_data_fin = vg_csv.merge(vg_devs, how = 'left')

# Remove the NaNs from the data set
vg_data_fin = vg_data_fin.dropna()

# Check the number of entries in final dataframe, should match the sum of lengths of originally 
# joined table (vg_nonan) and the vg_98 table
len(vg_data_fin.index) == sum([len(vg_nonan.index),len(vg_98.index)])

# Need to reindex dataframe having removed rows
vg_data_fin = vg_data_fin.reset_index(drop=True)

# Last check, look at year_released for correctness by viewing all unique entries
set(vg_data_fin.year_released)

# Inspect odd entries sequentially (e.g. 'Inc.', 'na')
vg_data_fin[vg_data_fin['year_released'].str.contains("na")]

# And replace as necessary using index
vg_data_fin.iat[823,2] = '2017'

# Note above, despite years for PS4 relaese prior to when the system was released (<2013) 
# leave them as it is the time the game first was released, reflecting it's development time
# more accurately

# Write the corrected csv with added developer details as a csv
vg_data_fin.to_csv("/Users/austindreyer/Documents/Python/Python_VideoGame_Project/ps4_videogame_data_dev.csv", index = False, header = True)

