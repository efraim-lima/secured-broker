import sys
import os

import json
from tabulate import tabulate
import platform

import db

def tickers(json_data):
    data = json.loads(json_data)
    results = data['results']

    results.sort(key=lambda x: x['h'], reverse=True)

    all_tickers = [result['T'] for result in results]
    top_ = results[:10]
    results = results[:500]
    tickers = [result['T'] for result in top_]
    table_data = [[result['T'], result['h'], result['l'], result['c'], result['o'], result['v'], result.get('vw', 0.0)] for result in top_]
    all_table_data = [[result['T'], result['h'], result['l'], result['c'], result['o'], result['v'], result.get('vw', 0.0)] for result in results]

    stocks = db.check_stocks()
    if stocks == False:
        for i in all_table_data:
            db.create()
            ticker = i[0]
            high = i[1]
            low = i[2]
            close = i[3]
            oppen = i[4]
            volume  = i[5]
            vwap = i[6]

            print("Loading, isso pode levar um tempo...")
            db.insert_stocks(ticker,high,low,close,oppen,volume,vwap)
            if platform.system() == "Linux":
                os.system('clear')
            elif platform.system() == "Windows":
                # Option 1: Using cls command (more compatible)
                os.system('cls')

    table = tabulate(table_data, headers=['Ticker', 'High', 'Low', 'Close', 'Open', 'Volume', 'VWAP'], tablefmt='orgtbl')

    print(table + "\n")

    print("Princpais ativos:\n", ' | '.join(tickers))

    return all_tickers