## last updated 12/5/19

# script to start exploring PS4 data

# load necessary packages
import sys
import pandas as pd 
import numpy as np
import matplotlib as mp
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

# set figure size for look-see plots
plt.rcParams["figure.figsize"] = (10, 5)

# read in data
ps4_data = pd.read_csv("/Users/austindreyer/Documents/Python/Python_VideoGame_Project/VG_data/PS4/ps4_videogame_data_ds.csv")

# check the dataframe structure
ps4_data.head()

# sort data by country for plotting
ps4_data_byc = ps4_data.sort_values("country")

# boxplots to look at avg game score by country
ax = sns.boxplot(x="country", y="avg_score", data=ps4_data_byc)
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right");

# boxplots to look at avg game score by genre
ax = sb.boxplot(x="genre", y="avg_score", data=ps4_data)
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right");


# inspect scores by developer est year, grouped by developer status
g = sns.catplot(x="est", y="avg_score",
                col="status",
                data=ps4_data, kind="box",
               height=4, aspect=1)
for ax in g.axes.flat:
   labels = ax.get_xticklabels() # get x labels
   for i,l in enumerate(labels):
       if i % 10 != 0:
           labels[i] = '' # show multiples of 5
   ax.set_xticklabels(labels, rotation=30)


# plot relationship between year released and score
plt.scatter(ps4_data.year_released, ps4_data.avg_score)

# plot relationship between year developer was established and score
plt.scatter(ps4_data.est, ps4_data.avg_score)

# boxplots to look at avg game sales by game genre
ax = sb.boxplot(x="genre", y="Tot_sales", data=ps4_data)
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right");

# boxplots to look at avg game sales by developer country 
ax = sb.boxplot(x="country", y="Tot_sales", data=ps4_data)
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right");

# countplot to look at number of games produced by different categorical factors, ordered by frequency
ax = sns.countplot(x="country", data=ps4_data, order = ps4_data['country'].value_counts().index)
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right");

# countplot to look at number of games produced by different categorical factors, ordered by frequency
ax = sns.countplot(x="developer", data=ps4_data, order = ps4_data['developer'].value_counts().index)
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right");

# countplot to look at number of games produced by different categorical factors, ordered by frequency
ax = sns.countplot(x="genre", data=ps4_data, order = ps4_data['genre'].value_counts().index)
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right");

# extract frequencies in actual quantitative numbers
genre_count = Counter(ps4_data.genre)
genre_count.most_common()





