from getScheduleandResults import getScheduleToday
from getTeamStatsZScore import teamStatsZScore
from datetime import date
import pandas as pd
from keras.models import load_model

def dailyGamesDataFrame(date):
    df = getScheduleToday(date)

    df = df.rename(columns={'Visitor/Neutral' : 'Visiting Team', 'Home/Neutral' : 'Home Team'})        
    df = df.drop(columns=['PTS', 'PTS.1'])

    year = int(date.strftime("%Y"))

    df2 = teamStatsZScore(year)

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

    return merged_df

def predictDailyGames():
    df = dailyGamesDataFrame(date.today())
    df = df.set_index(['Date', 'Visiting Team', 'Home Team'])

    model = load_model('NBAPredictor.h5')

    predictions = model.predict(df)

    df = df.reset_index()
    df = df[['Home Team', 'Visiting Team']]

    gamesWithPredictions = [df, predictions]

    return gamesWithPredictions

def interpretPredictions():

    df = predictDailyGames()

    for gameNum in range(len(df[0])):
        winProb = df[1][gameNum][1]
        winProb = str(round((winProb * 100), 2))
        homeTeam = df[0]['Home Team'][gameNum]
        awayTeam = df[0]['Visiting Team'][gameNum]

        print('There is a ' + winProb + '%' + ' chance that the ' + homeTeam + ' will defeat the ' + awayTeam)