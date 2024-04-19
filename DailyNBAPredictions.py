from ScheduleAndScoresPull import getTodaysSchedule
from TeamStatsPull import getTeamStats
import numpy as np
import pandas as pd
from datetime import timedelta
from keras.models import load_model

def makePredictions(date):
    schedule_df = getTodaysSchedule(date)

    yesterday_df = getTodaysSchedule(date-timedelta(days=1))
    yesterdays_teams = np.append(yesterday_df['Visitor/Neutral'].values, yesterday_df['Home/Neutral'].values)

    del yesterday_df

    schedule_df.rename(columns={'Visitor/Neutral' : 'Visiting Team', 'Home/Neutral' : 'Home Team'}, inplace=True)        
    schedule_df.insert(5, "Home Back to Back", False)
    schedule_df.insert(6, "Visiting Back to Back", False)
    schedule_df.drop(columns=['PTS', 'PTS.1'], inplace = True)

    schedule_df['Home Back to Back'] = np.where(schedule_df['Home Team'].isin(yesterdays_teams), True, False)
    schedule_df['Visiting Back to Back'] = np.where(schedule_df['Visiting Team'].isin(yesterdays_teams), True, False)


    if int(date.strftime("%m")) >= 9:
        year = int(date.strftime("%Y")) + 1
    else:
        year = int(date.strftime("%Y")) 

    stats_df = getTeamStats(year)

    statscolumns = stats_df.select_dtypes(include=[np.number]).drop(columns='Year').columns

    df = pd.merge(schedule_df, stats_df, left_on='Home Team', right_on='Team')
    df = pd.merge(df, stats_df, left_on='Visiting Team', right_on='Team', suffixes=('Home', 'Visitor'))

    del year, schedule_df, stats_df

    for col in statscolumns:
            df[col + 'Diff'] = df[col + 'Home'] - df[col + 'Visitor']

    df = df[df.columns.drop(list(df.filter(regex='Home$')))]
    df = df[df.columns.drop(list(df.filter(regex='Visitor$')))]
    df.set_index(['Date', 'Visiting Team', 'Home Team'], inplace=True)
    
    model = load_model('NBAPredictor.keras')
    
    try:
        predictions = pd.DataFrame(data=model.predict(df), columns=['Prediction'])
    except:
        raise Exception('No Games Today.')

    del model

    df.reset_index(inplace=True)
    df = df[['Home Team', 'Visiting Team']]

    df = pd.concat([df, predictions], axis=1)

    del predictions

    for index in range(len(df)):
        winProb = df.loc[index, 'Prediction']
        roadProb = 1 - winProb
        winProb = round((winProb * 100), 2)
        roadProb = round((roadProb * 100), 2)
        homeTeam = df.loc[index, 'Home Team']
        awayTeam = df.loc[index, 'Visiting Team']

        if winProb >= 50:
            moneyline = (int(np.round(-((100 * winProb) / (winProb - 100)), 0)))
            moneyline = "-" + str(moneyline)
        else:
            moneyline = (int(np.round(-((100 * (winProb - 100)) / (winProb)), 0)))
            moneyline = "+" + str(moneyline)

        if roadProb >= 50:
            roadmoneyline = (int(np.round(-((100 * roadProb) / (roadProb - 100)), 0)))
            roadmoneyline = "-" + str(roadmoneyline)
        else:
            roadmoneyline = (int(np.round(-((100 * (roadProb - 100)) / (roadProb)), 0)))
            roadmoneyline = "+" + str(roadmoneyline)

        winProb = str(winProb)
        roadProb = str(roadProb)

        print('Home Win for {}: {}% or {}, Away Win for {}: {}% or {}'.format(homeTeam, winProb, moneyline, awayTeam, roadProb, roadmoneyline))

    del df, winProb, roadProb, homeTeam, awayTeam, moneyline, roadmoneyline