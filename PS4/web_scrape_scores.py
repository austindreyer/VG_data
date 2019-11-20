## last updated 11/10/19

## use following path to work through anaconda install of python:
	# /Users/austindreyer/anaconda3/bin/python $filename

# script to collect video game scores for PS4 games

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

url = "https://www.gamerankings.com/browse.html?site=ps4&cat=0&year=0&numrev=2&sort=2&letter=A&search="

# demonstrate extraction of webpage
response = get(url)
#print(response.text[:500])

# extract data using beautifulsoup
soup = BeautifulSoup(response.text, 'html.parser')
#print(type(html_soup))

vg_containers = soup.find_all('tr')
#print(len(vg_containers))

#print(vg_containers[0])

first_name = vg_containers[0].a.text
#print(first_name)
first_dev = vg_containers[0].find_all('td', limit=3)[-1]
first_dev_txt = ''.join(first_dev.find('br').next_siblings)
first_dev_name = [x.strip() for x in first_dev_txt.split(',')][0]
first_year = [x.strip() for x in first_dev_txt.split(',')][1]
#print(first_year)

first_score_txt = vg_containers[0].find_all('td', limit=4)[-1]
first_score = float(re.sub('%', '', ''.join(first_score_txt.find('b'))))
first_reviews = ''.join(first_score_txt.find('br').next_siblings)
first_rev_num = float(first_reviews.split(' ')[0])
#print(first_score)



### scrape the first page for PS4 video game reviews 

# create empty lists to fill with scraped data
names = []
developers = []
years = []
scores = []
reviews = []

# create loop for full data scraping
pages = [str(i) for i in range(0,55)]

# set up the loop monitoring
start_time = time()
requests = 0

# loop over all pages
for page in pages:
	
	# make a request for each page
	page_view = get('https://www.gamerankings.com/browse.html?site=ps4&page='
	+ page + '&sort=2&numrev=2')
	
	# add pauses in data pull requests to play nice with their server
	sleep(randint(10, 20))
	
	# keep an eye on the progress
	requests += 1
	elapsed_time = time() - start_time
	print('Request: {}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))
	display.clear_output(wait = True)
	
	# output a warning if trouble
	if response.status_code !=200:
		warn('Request: {}; Status code; {}'.format(requests, response.status_code))
		
	# interrupt loop if more loops than desired
	if requests > 56:
		warn('Request number exceeds expectations')
		break
		
	# extract contents of each page	
	soup = BeautifulSoup(page_view.text, 'html.parser')
	
	# get all of the rows corresponding to each game
	vg_containers = soup.find_all('tr')

	# extract data from individual entries
	for entry in vg_containers:
		
		# game name
		name = entry.a.text
		names.append(name)
		
		# developer
		first_dev = entry.find_all('td', limit=3)[-1]
		first_dev_txt = ''.join(first_dev.find('br').next_siblings)
		developer = [x.strip() for x in first_dev_txt.split(',')][0]
		developers.append(developer)
		
		# year published
		try:
			year = [x.strip() for x in first_dev_txt.split(',')][1]
		except IndexError:
			year = 'na'
		years.append(year)
		
		# avearge score
		first_score_txt = entry.find_all('td', limit=4)[-1]
		score = float(re.sub('%', '', ''.join(first_score_txt.find('b'))))
		scores.append(score)
		
		# number of reviews
		first_reviews = ''.join(first_score_txt.find('br').next_siblings)
		review = float(first_reviews.split(' ')[0])
		reviews.append(review)
	
# look at output
gamescores_df = pd.DataFrame({
	'Video Game': names,
	'Developer': developers,
	'Year': years,
	'Avg Score': scores,
	'# Reviews': reviews	
})
gamescores_df = gamescores_df[['Video Game','Developer','Year','Avg Score','# Reviews']]

print(gamescores_df.info())

# export shiny new data
gamescores_df.to_csv(r'/Users/austindreyer/Documents/Python/Python_VideoGame_Project/videogame_scores.csv', index = None, header = True)
