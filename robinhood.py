import robin_stocks.robinhood as r
from pyrh import Robinhood
import pandas as pd
import csv
from robin_stocks.robinhood.export import export_completed_option_orders
import xlsxwriter as xl



email = input("Email: ")
password = input("Password: ")

login = r.login(email, password)

# Query your positions
allPositions = r.get_all_option_positions()
optionNames = []
entryPrices = []
print(len(allPositions))
for i in range(1, len(allPositions), 2):
  
  option = r.get_option_instrument_data_by_id(allPositions[i]["option_id"])
  ticker = option["chain_symbol"]
  strike = option["strike_price"]
  callOrPut = option["type"]
  date = option["expiration_date"]

  optionNames.append("{} ${} {} {}".format(ticker, strike, callOrPut, date))

  entryPrice = allPositions[i]["average_price"]
  entryPrices.append(entryPrice)

print(len(optionNames))
df = pd.DataFrame({"Option Name" : optionNames, "Entry Price" : entryPrices})
writer = pd.ExcelWriter("OptionTrades.xlsx", engine = 'xlsxwriter')
df.to_excel(writer, sheet_name="Sheet1")
writer.save()

closingPrices = []

r.logout()

