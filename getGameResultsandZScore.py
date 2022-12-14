from getScheduleandResults import getScheduleandResultsPast
from getTeamStatsZScore import teamStatsZScore
import pandas as pd
import numpy as np
import time

def getGameResultsandZScoreDiff(startyear, endyear):
    years = np.arange(startyear, endyear, 1)

    final_df = pd.DataFrame()

    for year in years:

        df = getScheduleandResultsPast(year)

        time.sleep(3)

        df = df.rename(columns={'Visitor/Neutral' : 'Visiting Team', 'Home/Neutral' : 'Home Team'})
        
        df['Home Win'] = np.where((df['PTS.1'] > df['PTS']), 1, 0)
        df = df.drop(columns=['PTS', 'PTS.1'])

        df2 = teamStatsZScore(year)

        time.sleep(3)

        merged_df = pd.merge(df, df2, left_on='Home Team', right_on='Team')
        merged_df = pd.merge(merged_df, df2, left_on='Visiting Team', right_on='Team', suffixes=('Home', 'Visitor'))

        merged_df['TS%Diff'] = merged_df['TS%Home'] - merged_df['TS%Visitor']
        merged_df['FTDiff'] = merged_df['FTHome'] - merged_df['FTVisitor']
        merged_df['FTADiff'] = merged_df['FTAHome'] - merged_df['FTAVisitor']
        merged_df['FT%Diff'] = merged_df['FT%Home'] - merged_df['FT%Visitor']
        merged_df['ORBDiff'] = merged_df['ORBHome'] - merged_df['ORBVisitor']
        merged_df['DRBDiff'] = merged_df['DRBHome'] - merged_df['DRBVisitor']
        merged_df['ASTDiff'] = merged_df['ASTHome'] - merged_df['ASTVisitor']
        merged_df['STLDiff'] = merged_df['STLHome'] - merged_df['STLVisitor']
        merged_df['BLKDiff'] = merged_df['BLKHome'] - merged_df['BLKVisitor']
        merged_df['TOVDiff'] = merged_df['TOVHome'] - merged_df['TOVVisitor']
        merged_df['PFDiff'] = merged_df['PFHome'] - merged_df['PFVisitor']
        merged_df['PTSDiff'] = merged_df['PTSHome'] - merged_df['PTSVisitor']
        merged_df['PADiff'] = merged_df['DRtgHome'] - merged_df['DRtgVisitor']

        merged_df = merged_df[merged_df.columns.drop(list(merged_df.filter(regex='Home$')))]
        merged_df = merged_df[merged_df.columns.drop(list(merged_df.filter(regex='Visitor$')))]

        final_df = pd.concat([final_df, merged_df])


    final_df.to_csv('gameResultsandZScoreDiff.csv', index=False)
    return final_df

getGameResultsandZScoreDiff(2021, 2023)