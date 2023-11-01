import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
from sklearn.preprocessing import StandardScaler

def getTeamStats(year):
    base_url = 'https://www.basketball-reference.com/leagues/NBA_{}.html'
    req_url = base_url.format(year)
    data = requests.get(req_url)
    soup = BeautifulSoup(data.content, 'html.parser')
    table = soup.find('table', attrs={'id': 'per_poss-team'})
    poss_df = pd.read_html(str(table))[0]

    del base_url, req_url, data, soup, table

    time.sleep(3)

    base_url = 'https://www.basketball-reference.com/leagues/NBA_{}.html'
    req_url = base_url.format(year)
    data = requests.get(req_url)
    soup = BeautifulSoup(data.content, 'html.parser')
    table = soup.find('table', attrs={'id': 'advanced-team'})
    adv_df = pd.read_html(str(table))[0]

    del base_url, req_url, data, soup, table

    adv_df.columns = [x[1] for x in adv_df.columns]
    adv_df = adv_df[['Team', 'ORtg', 'DRtg', 'TS%']]

    df = poss_df.merge(adv_df, on='Team')

    del poss_df, adv_df

    df['Year'] = year
    df['Team'] = df['Team'].str.replace('*', '', regex=True)

    df.set_index(['Team', 'Year'], inplace=True)
    df.drop(columns=['Rk', 'G', 'MP'], inplace=True)

    scaler = StandardScaler()

    df = pd.DataFrame(scaler.fit_transform(df), columns=df.columns, index=df.index)
    df.reset_index(inplace=True)

    return df