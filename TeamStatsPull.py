import pandas as pd
import requests
from bs4 import BeautifulSoup
from io import StringIO
import time
from sklearn.preprocessing import RobustScaler

def getTeamStats(year):
    base_url = 'https://www.basketball-reference.com/leagues/NBA_{}.html'
    req_url = base_url.format(year)
    data = requests.get(req_url)
    soup = BeautifulSoup(data.content, 'html.parser')
    table = soup.find('table', attrs={'id': 'per_poss-team'})
    poss_df = pd.read_html(StringIO(str(table)))[0]
    poss_df.drop(columns=['Rk', 'G', 'MP'], inplace=True)
    poss_df = poss_df.rename(columns={c: c+'_For' for c in poss_df.columns if c not in ['Team']})

    del table

    time.sleep(3)

    table = soup.find('table', attrs={'id': 'advanced-team'})
    adv_df = pd.read_html(StringIO(str(table)))[0]

    del table

    adv_df.columns = [x[1] for x in adv_df.columns]
    adv_df = adv_df[['Team', 'ORtg', 'DRtg', 'TS%']]
    adv_df = adv_df.rename(columns={c: c+'_For' for c in adv_df.columns if c not in ['Team']})

    for_df = poss_df.merge(adv_df, on='Team')

    del poss_df, adv_df

    for_df['Year'] = year
    for_df['Team'] = for_df['Team'].str.replace('\*', '', regex=True)

    for_df.set_index(['Team', 'Year'], inplace=True)

    time.sleep(3)
    
    table = soup.find('table', attrs={'id': 'per_poss-opponent'})
    against_df = pd.read_html(StringIO(str(table)))[0]
    against_df.drop(columns=['Rk', 'G', 'MP'], inplace=True)
    against_df = against_df.rename(columns={c: c+'_Against' for c in against_df.columns if c not in ['Team']})

    del base_url, req_url, data, soup, table

    against_df['Year'] = year
    against_df['Team'] = against_df['Team'].str.replace('\*', '', regex=True)

    against_df.set_index(['Team', 'Year'], inplace=True)

    df = pd.merge(for_df, against_df, on=['Team', 'Year'])

    del for_df, against_df

    scaler = RobustScaler()

    df = pd.DataFrame(scaler.fit_transform(df), columns=df.columns, index=df.index)
    df.reset_index(inplace=True)

    return df