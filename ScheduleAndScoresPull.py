import pandas as pd
import requests
import time
from bs4 import BeautifulSoup
from io import StringIO

def getPastScheduleAndScores(year):
    yearlydf = pd.DataFrame()
    months = ['october', 'november', 'december', 'january', 'february', 'march', 'april']

    for month in months:
        base_url = 'https://www.basketball-reference.com/leagues/NBA_{}_games-{}.html'
        req_url = base_url.format(year, month)
        data = requests.get(req_url)
        soup = BeautifulSoup(data.content, 'html.parser')
        table = soup.find('table', {'id': 'schedule'})

        del base_url, req_url, data, soup

        if table is not None:
            monthly_df = pd.read_html(StringIO(str(table)))[0]

            del table, monthly_df['Attend.'], monthly_df['Arena'], monthly_df['Notes']

            if 'Start (ET)' in monthly_df.columns:
                del monthly_df['Start (ET)']
            if 'Unnamed: 5' in monthly_df.columns:
                del monthly_df['Unnamed: 5']
            if 'Unnamed: 6' in monthly_df.columns:
                del monthly_df['Unnamed: 6']
            if 'Unnamed: 7' in monthly_df.columns:
                del monthly_df['Unnamed: 7']

            yearlydf = pd.concat([yearlydf, monthly_df])

        time.sleep(3)

    del months

    return yearlydf

def getTodaysSchedule(date):   
    yearstring = date.strftime("%Y")
    monthstring = str.lower(date.strftime("%B"))
    today = date.strftime("%a, %b %#d, %Y")

    if int(date.strftime("%m")) >= 9:
        year = int(yearstring) + 1
    else:
        year = int(yearstring)

    base_url = 'https://www.basketball-reference.com/leagues/NBA_{}_games-' + monthstring + '.html'
    req_url = base_url.format(year)
    data = requests.get(req_url)
    soup = BeautifulSoup(data.content, 'html.parser')
    table = soup.find('table', {'id': 'schedule'})

    del yearstring, monthstring, base_url, req_url, data, soup
        
    if table is not None:
        df = pd.read_html(StringIO(str(table)))[0]

        del table, df['Attend.'], df['Arena'], df['Notes']

        if 'Start (ET)' in df.columns:
            del df['Start (ET)']
        if 'Unnamed: 5' in df.columns:
            del df['Unnamed: 5']
        if 'Unnamed: 6' in df.columns:
            del df['Unnamed: 6']
        if 'Unnamed: 7' in df.columns:
            del df['Unnamed: 7']

        df = df.loc[df['Date'] == today]

        del today

        return df