# Import from the parent directory (app)
import os
polygonKey = os.environ.get("POLYGON_API_KEY")
#Import from the parent directory (app)
import calendar
import datetime
from dotenv import load_dotenv
import holidays
import json
import platform
import requests
from time import sleep

import db
from logs.logs import info, error, warn, critic
from tickers import getQuote, getTickers
from filtered import tickers

load_dotenv()

today = datetime.date.today()
now = datetime.datetime.now()
now = now.strftime("%Y-%m-%d %H:%M:%S")

db.create()

def clear():
    if platform.system() == "Linux":
        os.system('clear')
    elif platform.system() == "Windows":
        os.system('cls')

def start():
    clear()
    print("Bem vindo ao seu simple home broker!\n")

    print("Principais ativos do dia:\n")

    stocks = db.check_stocks()
    
    if stocks == False:
        tickers_used = getTickers()
        tickers_used = json.dumps(tickers_used)
        tickers(tickers_used)
    else:
        stocks = json.loads(stocks)
        tickers(json.dumps(stocks))

    condition = input("\n\n-------------------------------------------------------------------------\nQuer consultar seus ativos? [S/N]\n")
    while True:
        clear()
        if condition.upper() == "S":
            clear()
            extract()
            conditionII = input("Quer efetuar uma operação financeira agora? [S/N]\n")
            if conditionII.upper() == "S":
                clear()
                op = operation()
                if op == 4:
                    break
            if conditionII.upper() == "N":
                clear()
                print("Obrigado pela preferencia, volte sempre!")
                break
        elif condition.upper()=="N":
            clear()
            print("Entendi, obrigado pela preferencia, volte sempre")
            break
        else:
            clear()
            print("Não compreendi, tente novamente.")
    
def operation():
    clear()
    while True:
        clear()
        try:
            financ = int(input("""Qual operação gostaria de fazer?
    0- EXTRATO
    1- COMPRAR
    2- VENDER
    3- FECHAR POSIÇÃO
    4- SAIR\n"""))
            if financ == 0:
                extract()
                continue
            if financ == 1:
                clear()
                print("Principais ativos do dia:\n")

                stocks = db.check_stocks()
                
                if stocks == False:
                    tickers_used = getTickers()
                    tickers_used = json.dumps(tickers_used)
                    tickers(tickers_used)
                else:
                    stocks = json.loads(stocks)
                    tickers(json.dumps(stocks))

                ticker = input("Insira o ticker do ativo que deseja comprar agora (exemplo: AAPL):\n")
                try:
                    amount = int(input("Insira a quantidade de ativos que deseja comprar:\n"))
                except:
                    print("Entrada inválida")
                ticker = ticker.upper()
                
                if isinstance(ticker, str) and isinstance(amount, int):
                    tickers_db = db.tickers()
                    if ticker in tickers_db: 
                        db.insert(ticker, amount, now)
                        print("\n\nFeito!\n\n")
                        sleep(1)
                    else:
                        print(f"{ticker} ativo não existe, tente novamente")
                        continue
                else:
                    print("Algo deu errado, por favor, tente novamente.")
                    continue
                continue
            elif financ == 2:
                clear()
                extract()
                ticker = input("Insira o ticker do ativo que deseja vender agora (exemplo: AAPL):\n")
                try:
                    amount = int(input("Insira a quantidade de ativos que deseja vender:\n"))
                except:
                    print("Entrada inválida")
                if isinstance(ticker, str) and isinstance(amount, int):
                    ticker = ticker.upper()
                    
                    total_amount = db.total(ticker)
                    
                    if amount <= total_amount:
                        db.sell(ticker, total_amount, amount, now)
                        print("\n\nFeito!\n\n")
                        sleep(2)
                    elif amount > total_amount:
                        print(f"Você não pode vender {amount} cotas de {ticker}\nQuantidade disponível:\n\n{ticker}: {total_amount}\n")
                        critic(f"ticker={ticker}, amount={amount} | {now} | SELLING REFUSED")
                        sleep(1)
                        print(3)
                        sleep(1)
                        sleep(1)
                        print(2)
                        sleep(1)
                        print(1)
                        print("\n\nAlgo deu errado\n\n")
                        sleep(3)
                    else:
                        print("Algo deu errado")
                else:
                    print("Algo deu errado, por favor, entre o valor novamente.")
                continue
            elif financ == 3:
                clear()
                extract()
                ticker = input("Insira o ticker do ativo que deseja diluir posição \n\n(Exemplo: AAPL):\n")
                
                ticker = ticker.upper()
                total_amount = db.total(ticker)
                response = input(f"Tem certeza que deseja vender {total_amount} cotas do ativo {ticker}?\n\n[S/N]")
                
                if response.upper() == "S":
                    if isinstance(ticker, str):
                        
                        if total_amount:
                            actual_amount = 0
                            db.sell(ticker, actual_amount, total_amount, now)
                            db.delete(ticker)
                            print("\n\nFeito!\n\n")
                            sleep(1)
                            clear()
                        else:
                            critic(f"ticker={ticker} | {now} | POSITION CLOSING REFUSED")
                            sleep(1)
                            print(3)
                            sleep(1)
                            sleep(1)
                            print(2)
                            sleep(1)
                            print(1)
                            print("\n\nAlgo deu errado\n\n")
                            sleep(3)
                    else:
                        print("Algo deu errado, por favor, entre o valor novamente.")
                    continue
                elif response.upper() == "N":
                    print("Operação cancelada!")
                else:
                    print("Não te entendi, repita")
            elif financ == 4:
                clear()
                print("Obrigado pela preferência!")
                return 4
            else:
                clear()
                print("Não entendi, por favor, digite novamente")
        except:
            print("Entrada inválida")

def extract():
    clear()
    results = db.read()
    
    print("""
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+                  
|           Ativo           |       Quantidade        |       Ultima Atualização        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+""")
    if results:
        for result in results:
            
            ticker=result[0]
            total=result[1]
            date=result[2]
            
            print(f"""|           {ticker}            |           {total}             |       {date}       |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+""")
    else:
            print("""|                                         EMPTY                                         |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
""")

if __name__ == "__main__":
    start()