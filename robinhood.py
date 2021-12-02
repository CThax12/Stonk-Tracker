import robin_stocks.robinhood as r
from pyrh import Robinhood
import pandas as pd
import csv

email = input("Email: ")
password = input("Password: ")

login = r.login(email, password)

# Query your positions
allPositions = r.get_all_option_positions()
print(allPositions[0])
for pos in allPositions:
  
  option = r.get_option_instrument_data_by_id(pos["option_id"])
  ticker = option["chain_symbol"]
  strike = option["strike_price"]
  callOrPut = option["type"]
  date = option["expiration_date"]

  print("{} ${:.2f} {} {}".format(ticker, strike, callOrPut, date))


tickers = []

# Get a list of the tickers for each trade.
for trade in allPositions:
  tickers.append(r.get_symbol_by_url(trade["instrument"]))

avgEntryPrices = []


r.logout()