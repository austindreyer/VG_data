## last updated 12/5/19

## Script to combine curated vg data with sales data into single dataframe


# Load necessary packages
import sys
import pandas as pd 
import numpy as np
from fuzzywuzzy import fuzz



# Read in the csv of video game data files
vg_data_dev = pd.read_csv("/Users/austindreyer/Documents/Python/Python_VideoGame_Project/VG_data/PS4/ps4_videogame_data_dev.csv")
vg_allsales = pd.read_csv("/Users/austindreyer/Documents/Python/Python_VideoGame_Project/VG_data/PS4/ps4_videogame_sales.csv")


# And confirm they were read in as a dataframes
isinstance(vg_data, pd.DataFrame)
isinstance(vg_sales, pd.DataFrame)

# Subset the sales dataframe by taking on games that have total sales >0.0
vg_sales = vg_allsales[vg_allsales['Tot_sales'] > 0]

# Likely worth looking into total sales by genre and not just the sales data that matches the ratings 
# data set so export it as a csv
vg_sales.to_csv("/Users/austindreyer/Documents/Python/Python_VideoGame_Project/VG_data/PS4/ps4_videogame_sales_pos.csv", index = False, header = True)

# Add column to original data frame to check for duplicate entries, video game title is the only concern for duplicates
# here. Note, must be done on original vg_allsales df to avoid taking a slice of a slice (no bueno)
vg_allsales['is_duplicated'] = vg_allsales['vg_name'].duplicated()


# Check for duplicates
vg_allsales['is_duplicated'].sum()

# Pull out the two duplicate names, they have tot_sales <0 so not included in truncated sales df
vg_allsales[vg_allsales['is_duplicated']]

# Check lengths of dataframes
print(len(vg_data_dev.index))
print(len(vg_sales.index))

# Check structure of dataframes, including for column names for joining, confirm can join on vg_name column
print(vg_data_dev.head())
print(vg_sales.head())

# Create new data frame that merges the two existing based on developer name
vg_data = vg_data_dev.merge(vg_sales, how = 'left')

# Inspect new data frame
vg_data.head()

# Remove rows without a matching entry for sales
vg_nonan = vg_data.dropna()

# Inspect new data frame 
pd.set_option('display.max_rows', 500)
vg_nonan

len(vg_nonan.index)

# Check the length of the merged data frame as compared to original
len(vg_data.index)-len(vg_nonan.index)

# Given the extreme loss of data based on matching of developer name, try to introduce fuzzy matching to 
# enable partial video game name matches to count for merging 
# to do so, need a function to match strings using fuzzywuzzy (added package install to start)

def match_name(name, list_names, min_score=0):
  '''Function to match names that are similar to one another'''
    # start with -1 score in case no matches
    max_score = -1
    # empty name for in case of no match as well
    max_name = ""
    # Iternating over all names in the dev data frame
    for orgname in list_names:
        #Finding fuzzy match score
        score = fuzz.token_set_ratio(name, orgname)
        # Checking if we are above our threshold and have a better score
        if (score > min_score) & (score > max_score):
            max_name = orgname
            max_score = score
    return (max_name, max_score)

# Need to generate dataframe of just the rows with missing values to fuzzy match
vg_nans = vg_data[pd.isnull(vg_data['Tot_sales'])]

# Confirm the correct number of rows in NaNs table as it should match the difference
# in dataframe lengths found above
len(vg_nans.index)

vg_nans.head()


vg_sales.head()

# Then use the function to test matching names starting 
# with an empty list to store outputs
match_list = []

# Find the matching names 
for name in vg_nans.vg_name:
    # Use function to find best match, set threshold for strength of match (0-100)
    match = match_name(name, vg_sales.vg_name, 50)
    
    # Store iterated data in dict
    dict_ = {}
    dict_.update({"vg_name" : name})
    dict_.update({"vg_match" : match[0]})
    dict_.update({"score" : match[1]})
    match_list.append(dict_)
    
vg_match = pd.DataFrame(match_list)

# Show results that have a match >50
vg_match[vg_match['score'] >50]

# check for increase match threshold to avoid non informative matches
vg_89 = vg_match[vg_match['score'] >89]
pd.set_option('display.max_rows', 500)

len(vg_89.index)



# Remove NaNs from sales df to inspect it manually for matches
vg_sales_nonan = vg_sales.dropna()

vg_sales_nonan[vg_sales_nonan['vg_name'].str.contains("Uncharted")]

vg_data_dev[vg_data_dev['vg_name'].str.contains("Resident")]

# Inspecting sales data has introduced the problem of what to do with sequals and 
# DLC for games. Probably best to average the data across DLC and add to original game it is an add-on to
# Start by removing rows from full dev data set that have a close but incorrect match in the sales
# data table

# Make copy of dev data table
vg_dev_copy = vg_nans

# And remove the rows based on name matching
vg_dev_copy = vg_dev_copy[vg_dev_copy.vg_name !='Battlefield V']

# Confirm removal by searching for string matching
vg_dev_copy[vg_dev_copy['vg_name'].str.contains('Resident')]

# Replace some names based on manually match
vg_dev_copy = vg_dev_copy.replace('Resident Evil 0: HD Remaster', 'Resident Evil Zero')

# Re-index entire copy dataframe and then redo fuzzy matching with modified copy set
vg_dev_copy = vg_dev_copy.sort_values('vg_name')

vg_dev_copy = vg_dev_copy.reset_index(drop=True)

# Now use copied dataframe to rematch
match_list2 = []


for name in vg_dev_copy.vg_name:
    # Use function to find best match, set threshold for strength of match (0-100)
    match = match_name(name, vg_sales.vg_name, 50)
    
    # Store iterated data in dict
    dict_ = {}
    dict_.update({"vg_name" : name})
    dict_.update({"vg_match" : match[0]})
    dict_.update({"score" : match[1]})
    match_list2.append(dict_)
    
vg_match2 = pd.DataFrame(match_list2)

# Show results that have a match >50
vg_match2[vg_match2['score'] >50]


vg2_89 = vg_match2[vg_match2['score'] >89]
pd.set_option('display.max_rows', 1000)
vg2_89


# Now, need to go back to original dataframe and replace the old developer names with the
# corrected names that have the additional data associated. To do this, will use the dataframe
# vg2_89 as a dictionary to replace Developer column in original dataframe

# Create copy of original vg_csv data "Developer" column to replace values
df2 = pd.DataFrame(vg_data_dev.vg_name, columns = ['vg_name'])

# Replace the names of df2 using the dictionary of vg2_89
df2['vg_name'] = df2['vg_name'].replace(vg2_89.set_index('vg_name')['vg_match'].dropna())

# Compare the original Developer names with the updated ones
pd.concat([vg_data_dev.vg_name, df2], axis=1, keys=['old', 'new'])

# Replace the original Developer column of vg_csv with corrected matched column

vg_data_dev['vg_name'] = df2['vg_name']

vg_data_dev.head()

# Re-join the modified dataframe with the developer dataframe
vg_data_fin = vg_data_dev.merge(vg_sales, how = 'left')

# Remove the NaNs from the data set
vg_data_fin = vg_data_fin.dropna()

# Need to reindex dataframe having removed rows
vg_data_fin = vg_data_fin.reset_index(drop=True)


# Now need to deal with duplicates as the game names for multiple DLC content was replaced by single game name
# during matching. As stated, for all duplicates will create a new single entry that is the sum of 
# the component sales data and average of the review data

# Start by reidentifying duplicates
#vg_data_fin['is_duplicated'] = vg_data_fin['vg_name'].duplicated()

vg_data_fin['is_duplicated'].sum()

# Look at the duplicates
pd.set_option('display.max_rows', 500)
 vg_data_fin[vg_data_fin['is_duplicated']]

# Process duplicates as stated using a function to do so

def dup_process(input_df, dup_col):
  '''Function to combine duplicate entries by averaging stats'''
    # Create empty list to store all new rows
    nodup = []
    # Get just the duplicated offending entries
    dups = input_df[input_df['is_duplicated']]
    # Get unique items of dup_col
    u_names = set(dups[dup_col])
    for name in u_names:
        # Need to extract row showing all duplicates
        temp_rows = input_df[input_df[dup_col]==name]
        # Make new single entry by copying entire top row as only the avg_score and num_reviews will change
        new_row = temp_rows.iloc[1].copy()
        
        # Calculate and replace combined values for duplicated game entries
        new_row['avg_score'] = temp_rows['avg_score'].mean()
        new_row['num_reviews'] = temp_rows['num_reviews'].sum()
        
        # Append each new single entry to form a complete data frame summarzing duplicates
        nodup.append(new_row)
    # Make new list a data frame for export
    nodup_df = pd.DataFrame(nodup)
    nodup_df = nodup_df.sort_values('vg_name')
    # Export unduplicated dataframe
    return(nodup_df)

# Create new datafrae of just the duplicated data that have been corrected with a single entry per vg_name
just_dups = dup_process(vg_data_fin, 'vg_name')

# Check the dataframe
just_dups

len(just_dups.index)

# Need to remerge the corrected duplicated data with original data set. To do so, first remove all 
# duplicated rows as indicated by "True" in is_duplicated column as they will be replaced by the
# values from the corrected row. Then perform a left merge of the original data and the corrected
# Duplicated data as vg_data_ds for 'developer and sales'
vg_data_ds = vg_data_fin[vg_data_fin['is_duplicated']==False]

vg_data_ds = vg_data_ds.merge(just_dups, how = 'left')

# Remove duplicated identifier column
vg_data_ds.drop('is_duplicated', axis = 1, inplace = True)

# Function to check on memory usage by data types for columns
def memory_change(input_df, column, dtype):
  '''Function to calculate potential memory savings'''
    df = input_df.copy()
    old = round(df[column].memory_usage(deep=True) / 1024, 2) # In KB
    new = round(df[column].astype(dtype).memory_usage(deep=True) / 1024, 2)# In KB
    change = round(100 * (old - new) / (old), 2)
    report = ("The inital memory footprint for {column} is: {old}KB.\n" 
              "The casted {column} would take: {new}KB.\n"
              "A change of {change} %.").format(**locals())
    return report


print(memory_change(vg_data_ds, 'vg_name', 'category'))


# Check the file size and data type for different columns, modify data types as necessary for memory 
# optomization. Include memory_usage argument 'deep' to access size of "object" datatype
vg_data_ds.info(memory_usage = 'deep')

# Can change data types of specific columns if desire and then compare total size
#vg_data_ds.vg_name = vg_nodup.vg_name.astype('category')
#vg_data_ds.developer = vg_nodup.developer.astype('category')

#vg_nodup.info(memory_usage = 'deep')


# Write the corrected csv with added developer details as a csv
vg_data_ds.to_csv("/Users/austindreyer/Documents/Python/Python_VideoGame_Project/VG_data/PS4/ps4_videogame_data_ds.csv", index = False, header = True)

