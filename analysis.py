# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 22:22:44 2017

@author: PaulPelayo
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm


#player_info = {
#    'Tm': 0,
#    'turnovers': 0, 
#    '3P': 0, 
#    'AST': 0,
#    'FG': 0,
#    'FT': 0, 
#    'DRB': 0,
#    'ORB': 0,
#    'BLK': 0,
##    'PF': 0
#
##}
#teams 

nba_stuff_weight = {
    'FG': 0.4,
    'PTS': 1,
    'ORB': 0.7,	
    'DRB': 0.3,
    'STL': 1,
    'ORB': 0.726,
    'AST': 0.7,	
    'DRB':	 0.272,	
    'PF': -0.318,	
    'FTM':	-0.372,	
    'FGM':	-0.726,
    'TOV':	-0.998,
	
}


br_weight = {
    'FG': 1.591,
    'STL': 0.998,
    '3P': 0.958,	
    'FT': 0.868,
    'BLK': 0.726,
    'ORB': 0.726,
    'AST': 0.642,	
    'DRB':	 0.272,	
    'PF': -0.318,	
    'FTM':	-0.372,	
    'FGM':	-0.726,
    'TOV':	-0.998	
}
def first2(s):
    return s[:2]

player_df = pd.read_csv('./data/Players.csv')
stats_df = pd.read_csv('./data/Seasons_Stats.csv')
team_df = pd.read_csv('./data/team_totals.csv').rename(index = str, columns={'3P': 'Threes'})
record_df = pd.read_csv('./data/records.csv', header=1)


record_df['Overall'] = record_df['Overall'].apply(first2)
record_dict = dict(zip(record_df.Team, record_df.Overall))

team_df['Wins'] = team_df['Team'].map(record_dict)
player_df = player_df.drop(['Unnamed: 0'], axis = 1)
stats_df = stats_df.drop(['Unnamed: 0'], axis = 1)


team_df['FTM'] = team_df['FTA'] - team_df['FT']
team_df['FGM'] = team_df['FGA'] - team_df['FG']
stats_df['FTM'] = stats_df['FTA'] - stats_df['FT']
stats_df['FGM'] = stats_df['FGA'] - stats_df['FG']



stats_df['br-per'] = (stats_df['FG'] * br_weight['FG'] + stats_df['STL'] * br_weight['STL'] + 
    stats_df['3P'] * br_weight['3P'] + stats_df['FT'] * br_weight['FT'] +
    stats_df['BLK'] * br_weight['BLK'] + stats_df['ORB'] * br_weight['ORB'] +
    stats_df['AST'] * br_weight['AST'] + stats_df['DRB'] * br_weight['DRB'] +
    stats_df['PF'] * br_weight['PF'] +  stats_df['TOV'] * br_weight['TOV'])
    
stats_df['game-score'] = (stats_df['PTS'] + 0.4 * stats_df['FG'] - 0.7 * 
    stats_df['FGA'] - 0.4 * (stats_df['FTA'] - stats_df['FT']) + 0.7 * stats_df['ORB'] + 
    0.3 * stats_df['DRB'] + stats_df['STL'] + 0.7 * stats_df['AST'] + 0.7 * stats_df['BLK'] - 
    0.4 * stats_df['PF'] - stats_df['TOV'])








stats_df = stats_df[stats_df['Year'] > 2016]
stats_df['MPG'] = stats_df['MP']/82
qualified_per = stats_df[stats_df['MPG'] > 6.9].drop_duplicates('Player', 'last').rename(index = str, columns={'3P': 'Threes'})

game_score = qualified_per.sort(['game-score'], ascending=False).head(150)['Player'].tolist()
true_per = qualified_per.sort(['PER'], ascending=False).head(150)['Player'].tolist()
br_per = qualified_per.sort(['br-per'], ascending=False).head(150)['Player'].tolist()





#X = team_df[['FG', 'Threes', 'FT', 'BLK', 'ORB', 'AST', 'DRB', 'PF', 'TOV']]
#y = team_df['Wins']
#model = sm.OLS(y, X).fit()
#print(model.summary())

version_rankings = pd.DataFrame(
    {'true_per': true_per,
     'br_per': br_per,
     'game-score': game_score
     })

#X = qualified_per[['TOV', 'Threes', 'AST', 'FG', 'FT', 'DRB', 'ORB', 'BLK', 'PF']]
#y = qualified_per['PER']
#model = sm.OLS(y, X).fit()
#print(model.summary())
#model = ols('~ PER', qualified_per).fit()
#model.summary()
#players = dict.fromkeys(stats_df['Player'].unique().tolist(), player_stats)
#team_player = dict.fromkeys
#lg_drb = team_df['DRB'].sum()
#
#
#lg_ft = team_df['FT'].sum()
#lg_pf = team_df['PF'].sum()
#lg_pts = team_df['PTS'].sum()
#lg_fga = team_df['FGA'].sum()
#lg_orb = team_df['ORB'].sum()
#lg_tov = team_df['TOV'].sum()
#lg_fta = team_df['FTA'].sum()
#lg_trb = lg_orb + lg_drb
#lg_ast = team_df['AST'].sum()
#lg_fg = team_df['FG'].sum()







