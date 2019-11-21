## last updated 11/19/19

## script to inspect developer dataframe for problem entries

## Working with developer data csv to identify and remove duplicates

# import necessary packages
import csv
import sys
import pandas as pd 
import numpy as np

# read in the csv of video game score data
dev_csv = pd.read_csv("/Users/austindreyer/Documents/Python/Python_VideoGame_Project/VG_data/PS4/videogame_devs.csv")

# and confirm it was read in as a dataframe
isinstance(dev_csv, pd.DataFrame)

# look at the top of the table to inspect
dev_csv.head(1)

# clean other columns as well, check for duplicates or clarity of categories, starting with Country

# create list of unique country IDs to check for issues
dist = set(dev_csv.country)
dist

# clear problems with several overlapping country IDs (e.g. US v USA) and strange entry of 'USIndiaEngland...'
# check the entries that match the oddities
pd.set_option('display.max_rows', 500)
dev_csv[dev_csv['country'].str.contains("United")]

# replace as go, visually confirming the correct assignment
dev_csv['country'].replace('United StatesCanada', 'USA', inplace = True)

# Developer name is compouned for Rockstar Games, inspect it separately
dev_csv[dev_csv['developer'].str.contains("Rockstar")]

# just replace entire entry for Rockstar Games, making it all a single entry for Rockstar Games, replace 
# using the index as shown in str.contains check
r_games = ['Rockstar Games', 'US', '1998', 'Subsidiary']
dev_csv.loc[461] = r_games

# confirm replacement
dev_csv.loc[461]

# check for other oddities in devs dataframe, like years that are more than 4 digits
dev_csv[(dev_csv.est.str.len() > 4)]

# replace few exceptions manually as well
#dev_csv['est'].replace('1989 (as Johnson Voorsanger Productions)', '1989', inplace = True)

# for extra long year entries, have to refer to index
dev_csv.iloc[481,2] = 1993

# check final data types for dataframe
dev_csv.dtypes

# make est column a float to match data type of video game dataframe
dev_csv['est'] = dev_csv['est'].astype(float)

# check final data types for dataframe
dev_csv.dtypes

# write the new corrected dataframe to a csv

dev_csv.to_csv("/Users/austindreyer/Documents/Python/Python_VideoGame_Project/VG_data/PS4/videogame_devs.csv", index = False, header = True)

