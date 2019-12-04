#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 17:23:55 2019

@author: Jake
"""

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('qb_rushing.csv')

# csv file is out of order, so reorganize by player rank
df = df.set_index('player_rank').sort_index()

# how many players are there
print('Total QBs: {}'.format(df.shape[0]))

# only look at players who played more than one year
df = df[(df['first_year'] != df['last_year']) & (df['games_started'] >= 10)]
print('QBs who played >1 year and started 10+ games: {}'.format(df.shape[0]))

################
# GAMES PLAYED #
################
games_max = int(max(df['games_played']))
games_mean = round(df['games_played'].mean(), 1)
games_median = df['games_played'].median()
print('Max games played: {}\nMean games played: {}\nMedian games played: {}'.\
      format(games_max, games_mean, games_median))

# Histogram of games played
plt.hist(df['games_played'], bins = 34)
plt.axvline(games_median,
            color = 'red',
            label = 'Median [{}]'.format(games_median))
plt.axvline(games_mean,
            color = 'black',
            label = 'Mean [{}]'.format(games_mean))
plt.title('Games Played per QB (1 bin = 10 games)')
plt.xlabel('Games Played')
plt.ylabel('Count')
plt.xlim(0, 350)
plt.grid(which = 'major')
plt.legend(loc = 'best')
plt.show()

###########
# RUSHING #
###########
rush_mean = round(df['yards_per_attempt'].mean(), 1)
rush_median = round(df['yards_per_attempt'].median())

# Histogram of yards rushed per attempt
plt.hist(df['yards_per_attempt'], bins = [i for i in range(-2, 11)])
plt.axvline(rush_median,
            color = 'red',
            label = 'Median [{}]'.format(rush_median))
plt.axvline(rush_mean,
            color = 'black',
            label = 'Mean [{}]'.format(rush_mean))
plt.xlim(-2, 8)
plt.title('Rushing Yards per Attempt')
plt.xlabel('Yards per Attempt')
plt.ylabel('Count')
plt.grid(which = 'major')
plt.show()