import os

import calendar
import datetime
from dotenv import load_dotenv
import holidays
import json
import requests
from time import sleep

import db
from filtered import tickers
from logs.logs import info, error, warn, critic

load_dotenv()

today = datetime.date.today()

def is_business_day(date):
    # Check if the day is a weekday (Monday=0, Sunday=6)
    if date.weekday() < 5:
        # Check if the day is not a public holiday
        if date not in holidays.CountryHoliday('USA'):
            return True
    return False

def last_business_day(date):
    prev_day = date - datetime.timedelta(days=1)
    while not is_business_day(prev_day):
        prev_day -= datetime.timedelta(days=1)
    return prev_day

last_bd = last_business_day(today)
day = last_bd.strftime('%Y-%m-%d')

today = datetime.date.today()

if is_business_day(today):
    #if today.weekday() == calendar.MONDAY:
    if today.weekday():    
        print(f"\nINFORMATIVO: Hoje ({day}) é dia útil\n\n")
    else:
        print(f"INFORMATIVO: Hoje ({day}) não é dia útil!")
else:
    print(f"INFORMATIVO: O ultimo dia útil foi: {day}")

def getQuote(ticker):
    polygonKey=os.getenv('OBFUSCATE')
    response = requests.get(f"https://api.polygon.io/v1/open-close/{ticker}/{day}?apiKey={polygonKey}")
    if response.status_code == 200:
        # data = response.json()
        # data = json.dumps(data)
        data = response.json()
        return data
    else:
        print(response.status_code)
        print(response.text)
        return None

def getTickers():
    polygonKey=os.getenv('OBFUSCATE')

    response = requests.get(f"https://api.polygon.io/v2/aggs/grouped/locale/us/market/stocks/{day}?adjusted=true&apiKey={polygonKey}")
    if response.status_code == 200:
        # data = response.json()
        # data = json.dumps(data)
        data = response.json()
        return data
    else:
        print(response.status_code)
        print(response.text)
        return response.text