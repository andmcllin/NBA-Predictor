import pandas as pd
import requests
from bs4 import BeautifulSoup
import time

def getTeamPossStats(year):

    base_url = 'https://www.basketball-reference.com/leagues/NBA_{}.html'

    req_url = base_url.format(year)
    data = requests.get(req_url)
    soup = BeautifulSoup(data.content, 'html.parser')
    table = soup.find('table', attrs={'id': 'per_poss-team'})
    df = pd.read_html(str(table))[0]

    time.sleep(3)

    base_url = 'https://www.basketball-reference.com/leagues/NBA_{}.html'

    req_url = base_url.format(year)
    data = requests.get(req_url)
    soup = BeautifulSoup(data.content, 'html.parser')
    table = soup.find('table', attrs={'id': 'advanced-team'})
    df2 = pd.read_html(str(table))[0]

    df2.columns = [x[1] for x in df2.columns]
    df2 = df2[['Team', 'DRtg', 'TS%']]

    merged_df = df.merge(df2, on='Team')
    merged_df['Year'] = year

    merged_df['Team'] = merged_df['Team'].str.replace('*', '', regex=True)

    return merged_df