#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 17:23:55 2019

@author: Jake
"""

#############################################################################
# H_0: Rushing has no impact on length of QB careers                        #
# H_a: QBs with higher than average rushing stats have shorter than average #
#      careers                                                              #
#############################################################################

import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load data from CSV
print()
df = pd.read_csv('qb_rushing.csv')

# Organize by player rank
df = df.set_index('player_rank').sort_index()
print(df.head(10).to_string())

# Total QBs
print('Total QBs: {}'.format(df.shape[0]))

# Look at players with >1 year, started >= 10 games, since first Super Bowl
df = df[(df['first_year'] < df['last_year']) &
        (df['games_started'] >= 10) &
        (df['first_year'] > 1966)]
print('QBs who played >1 year, started 10+ games, since 1966-67 season: {}'\
      .format(df.shape[0]))

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
plt.figure(figsize = (8, 8))
plt.hist(df['games_played'], [i for i in range(0, games_max, 10)])
plt.axvline(games_median,
            color = 'red',
            label = 'Median [{}]'.format(games_median))
plt.axvline(games_mean,
            color = 'black',
            label = 'Mean [{}]'.format(games_mean))
plt.title('Games Played per QB (1 bin = 10 games)')
plt.xlabel('Games Played')
plt.ylabel('Count')
plt.xlim(0, 10 * math.floor(games_max/10))
plt.grid(which = 'major')
plt.legend(loc = 'best')
plt.show()

####################
# RUSHING ATTEMPTS #
####################
attempts_max = int(max(df['rushing_attempts']))
attempts_mean = round(df['rushing_attempts'].mean(), 1)
attempts_median = round(df['rushing_attempts'].median(), 1)

# Histogram of rushing attempts
plt.figure(figsize = (8, 8))
plt.hist(df['rushing_attempts'], [i for i in range(0, attempts_max, 25)])
plt.axvline(attempts_median,
            color = 'red',
            label = 'Median [{}]'.format(attempts_median))
plt.axvline(attempts_mean,
            color = 'black',
            label = 'Mean [{}]'.format(attempts_mean))
plt.xlim(0, 1200)
plt.title('Rushing Attempts (1 bin = 25 attempts)')
plt.xlabel('Attempts')
plt.ylabel('Count')
plt.grid(which = 'major')
plt.legend(loc = 'best')
plt.show()

###############################
# YARDS PER ATTEMPT - ALL QBS #
###############################
yards_max = int(max(df['yards_per_attempt']))
yards_mean = round(df['yards_per_attempt'].mean(), 1)
yards_median = round(df['yards_per_attempt'].median(), 1)

# Histogram of yards per attempt
plt.figure(figsize = (8, 8))
plt.hist(df['yards_per_attempt'], bins = [i for i in range(-2, 11)])
plt.axvline(yards_median,
            color = 'red',
            label = 'Median [{}]'.format(yards_median))
plt.axvline(yards_mean,
            color = 'black',
            label = 'Mean [{}]'.format(yards_mean))
plt.xlim(-2, 10)
plt.title('Rushing Yards per Attempt (1 bin = 1 yard)')
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
print('Mean games played of top 25% of QBs [count: {}] based on rushing '
      'attempts: {}'.format(att_top25.shape[0], att_top25_mean_games))
print('Mean games played of bottom 25% of QBs [count: {}] based on rushing '
      'attempts: {}'.format(att_bot25.shape[0], att_bot25_mean_games))

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
print('Mean games played, top 25% of QBs [count: {}] based on yards per '
      'attempt: \n---> {} <---'.format(ypa_top25.shape[0],
                                       ypa_top25_mean_games))
print('Mean games played, bottom 25% of QBs [count: {}] based on yards per '
      'attempt: \n---> {} <---'.format(ypa_bot25.shape[0],
                                       ypa_bot25_mean_games))

########################################################################
# HISTOGRAM OF GAMES PLAYED FOR TOP AND BOTTOM 25% - YARDS PER ATTEMPT #
########################################################################
print()
gp_top25_max = int(ypa_top25['games_played'].max())
gp_bot25_max = int(ypa_bot25['games_played'].max())
plt.hist(ypa_top25['games_played'], [i for i in range(0, gp_top25_max, 25)],
         alpha = 0.75, label = 'Top 25%')
plt.hist(ypa_bot25['games_played'], [i for i in range(0, gp_bot25_max, 25)],
         alpha = 0.5, label = 'Bot 25%')
plt.legend()

##############################################################
# STANDARD DEVIATIONS OF GAMES PLAYED FOR TOP AND BOTTOM 25% #
##############################################################
print('Standard deviation of games played for top 25%: {}'.
      format(round(np.std(ypa_top25['games_played']), 2)))
print('Standard deviation of games played for bottom 25%: {}'.
      format(round(np.std(ypa_bot25['games_played']), 2)))