from ScheduleAndScoresPull import getPastScheduleAndScores
from TeamStatsPull import getTeamStats
import pandas as pd
import numpy as np

def createGameResultsCSV(startyear, endyear):
    years = np.arange(startyear, endyear, 1)

    df = pd.DataFrame()

    for year in years:
        scores_df = getPastScheduleAndScores(year)

        scores_df.rename(columns={'Visitor/Neutral' : 'Visiting Team', 'Home/Neutral' : 'Home Team'}, inplace=True)        
        scores_df['Home Win'] = np.where((scores_df['PTS.1'] >scores_df['PTS']), 1, 0)
        scores_df.drop(columns=['PTS', 'PTS.1'], inplace=True)

        teamstats_df = getTeamStats(year)

        statscolumns = teamstats_df.select_dtypes(include=[np.number]).drop(columns='Year').columns

        merged_df = pd.merge(scores_df, teamstats_df, left_on='Home Team', right_on='Team')
        merged_df = pd.merge(merged_df, teamstats_df, left_on='Visiting Team', right_on='Team', suffixes=('Home', 'Visitor'))

        del scores_df, teamstats_df

        for col in statscolumns:
            merged_df[col + 'Diff'] = merged_df[col + 'Home'] - merged_df[col + 'Visitor']

        merged_df = merged_df[merged_df.columns.drop(list(merged_df.filter(regex='Home$')))]
        merged_df = merged_df[merged_df.columns.drop(list(merged_df.filter(regex='Visitor$')))]

        df = pd.concat([df, merged_df])
        
    del merged_df

    df.to_csv('nbaGameResults.csv.gz', compression={'method':'gzip'}, index=False)