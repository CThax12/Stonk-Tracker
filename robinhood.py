import robin_stocks.robinhood as r
from pyrh import Robinhood
import pandas as pd
import csv

email = input("Email: ")
password = input("Password: ")

login = r.login(email, password)

# Query your positions
allPositions = r.get_all_option_positions()
optionNames = []
print(allPositions[0])
for pos in allPositions:
  
  option = r.get_option_instrument_data_by_id(pos["option_id"])
  ticker = option["chain_symbol"]
  strike = option["strike_price"]
  callOrPut = option["type"]
  date = option["expiration_date"]

  optionNames.append("{} ${} {} {}".format(ticker, strike, callOrPut, date))

entryPrices = []

closingPrices = []

r.logout()