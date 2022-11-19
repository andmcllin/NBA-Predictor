from getTeamStats import getTeamPossStats
from scipy.stats import zscore

def teamStatsZScore(year):

    df = getTeamPossStats(year)

    df = df.set_index(['Team', 'Year'])
    df2 = df.drop(columns=['Rk', 'G', 'MP'])
    df2 = df2.apply(zscore)
    df2 = df2.reset_index()
   
    return df2