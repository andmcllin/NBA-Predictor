import pandas as pd
import requests
import time
from bs4 import BeautifulSoup


def getScheduleandResultsPast(year):

    yearlydf = pd.DataFrame()

    time.sleep(3)

    base_url = 'https://www.basketball-reference.com/leagues/NBA_{}_games-october.html'

    req_url = base_url.format(year)
    req = requests.get(req_url)
    soup = BeautifulSoup(req.content, 'html.parser')
    table = soup.find('table', {'id': 'schedule'})

    if table is not None:

        df = pd.read_html(str(table))[0]

        del df['Attend.']
        del df['Arena']
        del df['Notes']

        if 'Start (ET)' in df.columns :
            del df['Start (ET)']
        if 'Unnamed: 5' in df.columns :
            del df['Unnamed: 5']
        if 'Unnamed: 6' in df.columns :
            del df['Unnamed: 6']
        if 'Unnamed: 7' in df.columns :
            del df['Unnamed: 7']

        yearlydf = df

    time.sleep(3)

    base_url = 'https://www.basketball-reference.com/leagues/NBA_{}_games-november.html'
    req_url = base_url.format(year)
    req = requests.get(req_url)
    soup = BeautifulSoup(req.content, 'html.parser')
    table = soup.find('table', {'id': 'schedule'})

    if table is not None:

        df = pd.read_html(str(table))[0]

        del df['Attend.']
        del df['Arena']
        del df['Notes']

        if 'Start (ET)' in df.columns:
            del df['Start (ET)']
        if 'Unnamed: 5' in df.columns:
            del df['Unnamed: 5']
        if 'Unnamed: 6' in df.columns:
            del df['Unnamed: 6']
        if 'Unnamed: 7' in df.columns:
            del df['Unnamed: 7']

        yearlydf = pd.concat([yearlydf, df])

    time.sleep(3)

    base_url = 'https://www.basketball-reference.com/leagues/NBA_{}_games-december.html'
    req_url = base_url.format(year)
    req = requests.get(req_url)
    soup = BeautifulSoup(req.content, 'html.parser')
    table = soup.find('table', {'id': 'schedule'})

    if table is not None:

        df = pd.read_html(str(table))[0]

        del df['Attend.']
        del df['Arena']
        del df['Notes']

        if 'Start (ET)' in df.columns:
            del df['Start (ET)']
        if 'Unnamed: 5' in df.columns:
            del df['Unnamed: 5']
        if 'Unnamed: 6' in df.columns:
            del df['Unnamed: 6']
        if 'Unnamed: 7' in df.columns:
            del df['Unnamed: 7']

        yearlydf = pd.concat([yearlydf, df])
    
    time.sleep(3)

    base_url = 'https://www.basketball-reference.com/leagues/NBA_{}_games-january.html'
    req_url = base_url.format(year)
    req = requests.get(req_url)
    soup = BeautifulSoup(req.content, 'html.parser')
    table = soup.find('table', {'id': 'schedule'})

    if table is not None:

        df = pd.read_html(str(table))[0]

        del df['Attend.']
        del df['Arena']
        del df['Notes']

        if 'Start (ET)' in df.columns:
            del df['Start (ET)']
        if 'Unnamed: 5' in df.columns:
            del df['Unnamed: 5']
        if 'Unnamed: 6' in df.columns:
            del df['Unnamed: 6']
        if 'Unnamed: 7' in df.columns:
            del df['Unnamed: 7']
            
        yearlydf = pd.concat([yearlydf, df])

    time.sleep(3)

    base_url = 'https://www.basketball-reference.com/leagues/NBA_{}_games-february.html'
    req_url = base_url.format(year)
    req = requests.get(req_url)
    soup = BeautifulSoup(req.content, 'html.parser')
    table = soup.find('table', {'id': 'schedule'})

    if table is not None:

        df = pd.read_html(str(table))[0]

        del df['Attend.']
        del df['Arena']
        del df['Notes']

        if 'Start (ET)' in df.columns:
            del df['Start (ET)']
        if 'Unnamed: 5' in df.columns:
            del df['Unnamed: 5']
        if 'Unnamed: 6' in df.columns:
            del df['Unnamed: 6']
        if 'Unnamed: 7' in df.columns:
            del df['Unnamed: 7']
            
        yearlydf = pd.concat([yearlydf, df])

    time.sleep(3)

    base_url = 'https://www.basketball-reference.com/leagues/NBA_{}_games-march.html'
    req_url = base_url.format(year)
    req = requests.get(req_url)
    soup = BeautifulSoup(req.content, 'html.parser')
    table = soup.find('table', {'id': 'schedule'})

    if table is not None:

        df = pd.read_html(str(table))[0]

        del df['Attend.']
        del df['Arena']
        del df['Notes']

        if 'Start (ET)' in df.columns:
            del df['Start (ET)']
        if 'Unnamed: 5' in df.columns:
            del df['Unnamed: 5']
        if 'Unnamed: 6' in df.columns:
            del df['Unnamed: 6']
        if 'Unnamed: 7' in df.columns:
            del df['Unnamed: 7']

        yearlydf = pd.concat([yearlydf, df])

        time.sleep(3)

        base_url = 'https://www.basketball-reference.com/leagues/NBA_{}_games-april.html'
        req_url = base_url.format(year)
        req = requests.get(req_url)
        soup = BeautifulSoup(req.content, 'html.parser')
        table = soup.find('table', {'id': 'schedule'})

        if table is not None:

            df = pd.read_html(str(table))[0]

            del df['Attend.']
            del df['Arena']
            del df['Notes']

        if 'Start (ET)' in df.columns:
            del df['Start (ET)']
        if 'Unnamed: 5' in df.columns:
            del df['Unnamed: 5']
        if 'Unnamed: 6' in df.columns:
            del df['Unnamed: 6']
        if 'Unnamed: 7' in df.columns:
            del df['Unnamed: 7']
   
        yearlydf = pd.concat([yearlydf, df])
        
    return yearlydf

def getScheduleToday(date):
    
    time.sleep(3)

    yearstring = date.strftime("%Y")
    monthstring = str.lower(date.strftime("%B"))
    today = date.strftime("%a, %b %#d, %Y")
    year = int(yearstring)

    base_url = 'https://www.basketball-reference.com/leagues/NBA_{}_games-' + monthstring + '.html'

    req_url = base_url.format(year)
    req = requests.get(req_url)
    soup = BeautifulSoup(req.content, 'html.parser')
    table = soup.find('table', {'id': 'schedule'})

    if table is not None:

        df = pd.read_html(str(table))[0]

        del df['Attend.']
        del df['Arena']
        del df['Notes']

        if 'Start (ET)' in df.columns:
            del df['Start (ET)']
        if 'Unnamed: 5' in df.columns:
            del df['Unnamed: 5']
        if 'Unnamed: 6' in df.columns:
            del df['Unnamed: 6']
        if 'Unnamed: 7' in df.columns:
            del df['Unnamed: 7']

        df = df.loc[df['Date'] == today]

        return df