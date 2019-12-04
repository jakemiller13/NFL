#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 17:23:55 2019

@author: Jake
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load data from CSV
print()
df = pd.read_csv('qb_rushing.csv')

# Organize by player rank
df = df.set_index('player_rank').sort_index()

# Total QBs
print('Total QBs: {}'.format(df.shape[0]))

# Look at players who played >1 year and started >= 10 games
df = df[(df['first_year'] < df['last_year']) & (df['games_started'] >= 10)]
print('QBs who played >1 year and started 10+ games: {}'.format(df.shape[0]))

# Use these 4 categories for analysis - note the NaN values in YPA
categories = ['games_played', 'games_started', 'rushing_attempts',
              'yards_per_attempt']
print()
print(df[categories].describe())
quantiles = [0.25, 0.5, 0.75]
gp_quant = np.quantile(df['games_played'], quantiles)
ra_quant = np.quantile(df['rushing_attempts'], quantiles)
ypa_quant = np.nanquantile(df['yards_per_attempt'], quantiles)

################
# GAMES PLAYED #
################
games_max = int(max(df['games_played']))
games_mean = round(df['games_played'].mean(), 1)
games_median = df['games_played'].median()

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

####################
# RUSHING ATTEMPTS #
####################
attempts_mean = round(df['rushing_attempts'].mean(), 1)
attempts_median = round(df['rushing_attempts'].median(), 1)

# Histogram of rushing attempts
plt.hist(df['rushing_attempts'], bins = 48)
plt.axvline(attempts_median,
            color = 'red',
            label = 'Median [{}]'.format(attempts_median))
plt.axvline(attempts_mean,
            color = 'black',
            label = 'Mean [{}]'.format(attempts_mean))
plt.xlim(0, 1200)
plt.title('Rushing Attempts (1 bin = 25 attempts')
plt.xlabel('Attempts')
plt.ylabel('Count')
plt.grid(which = 'major')
plt.legend(loc = 'best')
plt.show()

#####################
# YARDS PER ATTEMPT #
#####################
yards_mean = round(df['yards_per_attempt'].mean(), 1)
yards_median = round(df['yards_per_attempt'].median(), 1)

# Histogram of yards per attempt
plt.hist(df['yards_per_attempt'], bins = [i for i in range(-2, 11)])
plt.axvline(yards_median,
            color = 'red',
            label = 'Median [{}]'.format(yards_median))
plt.axvline(yards_mean,
            color = 'black',
            label = 'Mean [{}]'.format(yards_mean))
plt.xlim(-2, 8)
plt.title('Rushing Yards per Attempt (1 bin = 1 yard')
plt.xlabel('Yards per Attempt')
plt.ylabel('Count')
plt.grid(which = 'major')
plt.legend(loc = 'best')
plt.show()

################################################################
# COMPARE LENGTH OF CAREER OF TOP 25% TO BOTTOM 25% - ATTEMPTS #
################################################################
# This doesn't control for bad QBs, so look at yards per attempt
print()
att_top25 = df[df['rushing_attempts'] > ra_quant[2]]
att_bot25 = df[df['rushing_attempts'] < ra_quant[0]]
att_top25_mean_games = round(att_top25['games_played'].mean(), 1)
att_top25_median_games = round(att_top25['games_played'].median(), 1)
att_bot25_mean_games = round(att_bot25['games_played'].mean(), 1)
att_bot25_median_games = round(att_bot25['games_played'].median(), 1)
print('Mean games played of top 25% of QBs based on rushing attempts: {}'\
      .format(att_top25_mean_games))
print('Mean games played of bottom 25% of QBs based on rushing attempts: {}'\
      .format(att_bot25_mean_games))
'''
print('Median games played of top 25% of QBs based on rushing attempts: {}'\
      .format(att_top25_median_games))
print('Median games played of bottom 25% of QBs based on rushing attempts: {}'\
      .format(att_bot25_median_games))
'''

#########################################################################
# COMPARE LENGTH OF CAREER OF TOP 25% TO BOTTOM 25% - YARDS PER ATTEMPT #
#########################################################################
print()
ypa_top25 = df[df['yards_per_attempt'] > ypa_quant[2]]
ypa_bot25 = df[df['yards_per_attempt'] < ypa_quant[0]]
ypa_top25_mean_games = round(ypa_top25['games_played'].mean(), 1)
ypa_top25_median_games = round(ypa_top25['games_played'].median(), 1)
ypa_bot25_mean_games = round(ypa_bot25['games_played'].mean(), 1)
ypa_bot25_median_games = round(ypa_bot25['games_played'].median(), 1)
print('Mean games played of top 25% of QBs based on yards per attempt: {}'\
      .format(ypa_top25_mean_games))
print('Mean games played of bottom 25% of QBs based on yards per attempt: {}'\
      .format(ypa_bot25_mean_games))
'''
print('Median games played of top 25% of QBs based on rushing attempts: {}'\
      .format(ypa_top25_median_games))
print('Median games played of bottom 25% of QBs based on rushing attempts: {}'\
      .format(ypa_bot25_median_games))
'''