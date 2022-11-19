import pandas as pd
import requests
from bs4 import BeautifulSoup

def getTeamPossStats(year):

    base_url = 'https://www.basketball-reference.com/leagues/NBA_{}.html'

    req_url = base_url.format(year)
    data = requests.get(req_url)
    soup = BeautifulSoup(data.content, 'html.parser')
    table = soup.find('table', attrs={'id': 'per_poss-team'})
    df = pd.read_html(str(table))[0]
    df['Year'] = year

    return df