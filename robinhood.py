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
calls = 0
puts = 0

print(len(allPositions))
for i in range(1, len(allPositions), 2):
  
  option = r.get_option_instrument_data_by_id(allPositions[i]["option_id"])
  ticker = option["chain_symbol"]
  strike = option["strike_price"]
  callOrPut = option["type"]
  date = option["expiration_date"]

  optionNames.append("{} ${} {} {}".format(ticker, strike, callOrPut, date))

  entryPrice = allPositions[i]["average_price"]
  entryPrices.append("$" + entryPrice)

  if "call" in callOrPut:
    calls +=1
  else:
    puts +=1

print(len(optionNames))
df = pd.DataFrame({"Option Name" : optionNames, "Entry Price" : entryPrices})
writer = pd.ExcelWriter("OptionTrades.xlsx", engine = 'xlsxwriter')
df.to_excel(writer, sheet_name="Sheet1")

workbook = writer.book
worksheet = writer.sheets["Sheet1"]
chart1 = workbook.add_chart({'type': 'pie'})

# Configure the series. Note the use of the list syntax to define ranges:
worksheet.write_string("E2", "Calls")
worksheet.write_number("E3", calls)
worksheet.write_string("F2", "Puts")
worksheet.write_number("F3", puts)


chart1.add_series({
    'name':       'Pie sales data',
    'data_labels': {'value': True, 'category': True},
    'categories': ["Sheet1", 1, 4, 1, 5],
    'values':     ["Sheet1", 2, 4, 2, 5]
})

# Add a title.
chart1.set_title({'name': 'Call vs Put Frequency'})

# Set an Excel chart style. Colors with white outline and shadow.
chart1.set_style(10)

# Insert the chart into the worksheet (with an offset).
worksheet.insert_chart('E8', chart1, {'x_offset': 25, 'y_offset': 10})

writer.save()

closingPrices = []

r.logout()

