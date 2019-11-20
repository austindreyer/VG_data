## last updated 11/13/19

# script to collect video game scores for PS4 games

# first need to import packages required 
import re
import pandas as pd
import tkinter as tk
import numpy as np
from tkinter import filedialog
from requests import get
from bs4 import BeautifulSoup
from lxml import html 
from time import sleep, time
from random import randint
from IPython import display
from warnings import warn

url = "https://en.wikipedia.org/wiki/List_of_video_game_developers"

df = pd.read_html(url, header=0)[2]

devs_df = df[['developer','country','est']]

#print(devs_df)

#df.head()

# demonstrate extraction of webpage
response = get(url)
#print(response.text[:500])

# extract data using beautifulsoup
soup = BeautifulSoup(response.text, 'html.parser')
#print(type(html_soup))

#table_body = soup.find('tbody')
#print(table_body)
#rows = table_body.find_all('tr')
#for row in rows:
#	cols = row.find_all('td')
#	cols = 
#
#vg_containers = soup.find_all('table', attrs={'class': 'wikitable sortable'})
#print(len(vg_containers))

# create empty lists to store developer status info
status = []

# extract all of the trs from the table, including those without style stipulated
trs = soup.find("table", class_="wikitable sortable").find_all("tr")

# populate the status list with the actual style guide for each row, recognizing the 
# different possibilities represent the developer status
for tr in trs[1:]:
	try:
		stat = tr["style"]
	except:
		stat = 'none'

	status.append(stat)

# repopulate status list using list comprehension to make the colors of each row explicit 
# for the status of the developer
status = ['Subsidiary' if x=='background:#c9daff;' else 'Defunct' if x=='background:#ffe8a9;' else 'Independent' for x in status]

# add Status column to the original developer data frame
devs_df= devs_df.assign(Status=status)

print(devs_df.head())

# export shiny new data
#devs_df.to_csv(r'/Users/austindreyer/Documents/Python/Python_VideoGame_Project/videogame_devs.csv', index = None, header = True)
