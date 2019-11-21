## last updated 10/30/19

# script to collect video game sales for PS4 games

# first need to import packages required for ProcessLookupError
import re
import pandas as pd
import tkinter as tk
from tkinter import filedialog
from requests import get
from bs4 import BeautifulSoup
from lxml import html 
from time import sleep, time
from random import randint
from IPython import display
from warnings import warn

url = "http://www.vgchartz.com/platform/69/playstation-4/"

# demonstrate extraction of webpage
response = get(url)
print(response.text[:500])

# extract data using beautifulsoup
soup = BeautifulSoup(response.text, 'html.parser')

vg_containers = soup.find_all('tr')

# confirm the successful extraction of desired details
# video game name
first_name = vg_containers[1].find_all('td', limit=3)[-1]
first_name_txt = ''.join(first_dev.find('a').contents[0])

# genre
first_genre = vg_containers[1].find_all('td', limit=4)[-1].text

# north america sales
na_sales = vg_containers[1].find_all('td', limit=6)[-1].text

# europe sales
eu_sales = vg_containers[1].find_all('td', limit=7)[-1].text

# japan sales
j_sales = vg_containers[1].find_all('td', limit=8)[-1].text

# rest of world sales 
rest_sales = vg_containers[1].find_all('td', limit=9)[-1].text

# total sales
tot_sales = vg_containers[1].find_all('td', limit=10)[-1].text
#print(tot_sales)

### scrape the sales page for PS4 video games

# create empty lists to fill with scraped data
names = []
genres = []
northamers= []
europes = []
japans = []
rests = []
worlds = []

# extract data from individual entries
for entry in vg_containers[1:2]:
	try:
		# game name
		first_name = entry.find_all('td', limit=2)[-1]
		first_name_txt = ''.join(first_name.find('a').contents[0])
		names.append(first_name_txt)
		
		# genres
		genre = entry.find_all('td', limit=4)[-1].text
		genres.append(genre)
		
		# north america sales
		na_sale = entry.find_all('td', limit=6)[-1].text
		northamers.append(na_sale)
		
		# european sales
		eu_sale = entry.find_all('td', limit=7)[-1].text
		europes.append(eu_sale)
		
		# japan sales
		j_sale = entry.find_all('td', limit=8)[-1].text
		japans.append(j_sale)
		
		# rest of world sales
		rest_sale = entry.find_all('td', limit=9)[-1].text
		rests.append(rest_sale)
		
		# total sales
		tot_sale = entry.find_all('td', limit=10)[-1].text
		worlds.append(tot_sale)
	# need to include an expcetion if there is not a complete entry for a row
	except:
		continue 

# create dataframe of output
gamesales_df = pd.DataFrame({
	'vg_name': names,
	'genre': genress,
	'NA_sales': northamers,
	'EU_sales': europes,
	'Japan_sales': japans,
	'Nonspec_sales': rests,
	'Tot_sales': worlds
		
})

# assign column names
gamesales_df = gamesales_df[['vg_name','genre','NA_sales','EU_sales','Japan_sales', 'Nonspec_sales', 'Tot_sales']]

# check the details of dataframe
gamesales_df.info()

# export shiny new data
gamesales_df.to_csv(r'/Users/austindreyer/Documents/Python/Python_VideoGame_Project/VG_data/PS4/ps4_videogame_sales.csv', index = None, header = True)
