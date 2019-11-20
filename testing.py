## use script for prototyping portions of code

## last updated 9/10/19

# script to collect video game scores for PS4 games

# first need to import packages required for ProcessLookupError



from requests import get
from bs4 import BeautifulSoup
from lxml import html 
import re
import pandas as pd
from time import sleep, time
from random import randint
from IPython import display
from warnings import warn

url = 'https://www.gamerankings.com/browse.html?site=ps4&page=13&sort=2&numrev=2'

# demonstrate extraction of webpage
response = get(url)
#print(response.text[:500])

# extract data using beautifulsoup
soup = BeautifulSoup(response.text, 'html.parser')
#print(type(html_soup))

vg_containers = soup.find_all('tr')
#print(len(vg_containers))

#print(vg_containers[0])

first_name = vg_containers[34].a.text
print(first_name)
first_dev = vg_containers[34].find_all('td', limit=3)[-1]
first_dev_txt = ''.join(first_dev.find('br').next_siblings)
first_dev_name = [x.strip() for x in first_dev_txt.split(',')][0]
try:
	first_year = [x.strip() for x in first_dev_txt.split(',')][1]
except IndexError:
	first_year = 'na'
print(first_year)

first_score_txt = vg_containers[34].find_all('td', limit=4)[-1]
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
#
## extract data from individual entries
for entry in vg_containers:
##	
##	# game name
	name = entry.a.text
	names.append(name)
##	
##	# developer
	first_dev = entry.find_all('td', limit=3)[-1]
	first_dev_txt = ''.join(first_dev.find('br').next_siblings)
	developer = [x.strip() for x in first_dev_txt.split(',')][0]
	developers.append(developer)
##	
##	# year published
	try:
		year = [x.strip() for x in first_dev_txt.split(',')][1]
	except IndexError:
		year = 'na'
	years.append(year)
##	
##	# avearge score
	first_score_txt = entry.find_all('td', limit=4)[-1]
	score = float(re.sub('%', '', ''.join(first_score_txt.find('b'))))
	scores.append(score)
##	
##	# number of reviews
	first_reviews = ''.join(first_score_txt.find('br').next_siblings)
	review = float(first_reviews.split(' ')[0])
	reviews.append(review)
##	
### look at ouput
test_df = pd.DataFrame({
	'Video Game': names,
	'Developer': developers,
	'Year': years,
	'Avg Score': scores,
	'# Reviews': reviews	
})
test_df = test_df[['Video Game','Developer','Year','Avg Score','# Reviews']]
#
#print(test_df)

test_df.to_csv(r'/Users/austindreyer/Documents/Python/Python_VideoGame_Project/videogame_scores.csv', index = None, header = True)

# create loop for full data scraping
#pages = [str(i) for i in range(0,55)]
#
#warn("Warning Simulation")
#
#start_time = time()
#requests = 0
#for _ in range(5):
#	requests += 1
#	sleep(randint(1, 3))
#	current_time = time()
#	elapsed_time = current_time - start_time
#	print('Request: {}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))
#display.clear_output(wait = True)

#root= tk.Tk()
#
#canvas1 = tk.Canvas(root, width = 300, height = 300, bg = 'lightsteelblue2', relief = 'raised')
#canvas1.pack()
#
#def exportCSV ():
#	global df
#	
#	export_file_path = filedialog.asksaveasfilename(defaultextension='.csv')
#	df.to_csv (export_file_path, index = None, header=True)
#
#saveAsButton_CSV = tk.Button(text='Export CSV', command=exportCSV, bg='green', fg='white', font=('helvetica', 12, 'bold'))
#canvas1.create_window(150, 150, window=saveAsButton_CSV)
#
#root.mainloop()