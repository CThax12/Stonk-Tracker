import robin_stocks.robinhood as r
from pyrh import Robinhood
import pandas as pd
import csv
from collections import Counter
from robin_stocks.robinhood.export import export_completed_option_orders
import xlsxwriter as xl



def getCredentials():
    email = input("Email: ")
    password = input("Password: ")
    return email,password


def loginToRH(email, password):
    login = r.login(email, password)


def getAllOptions(allPositions):
  allPositions = r.get_all_option_positions()
  return allPositions


def getOptionTrades(allPositions):
    optionNames = []
    entryPrices = []
    calls = 0
    puts = 0

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
    return optionNames,entryPrices,calls,puts

def getFrequentTickers(allPositions):
  tickerList = []
  for i in range(1, len(allPositions), 2):
    ticker = allPositions[i]['chain_symbol']
    tickerList.append(ticker)
  
  c = Counter(tickerList)
  return dict(c.most_common(10))


  

def writeOptionsToExcel():
    df = pd.DataFrame({"Option Name" : optionNames, "Entry Price" : entryPrices})
    writer = pd.ExcelWriter("OptionTrades.xlsx", engine = 'xlsxwriter')
    df.to_excel(writer, sheet_name="Sheet1")
    return writer


def CallPutChart(chartCell, writer, workbook, worksheet, label1, label2):
    workbook = writer.book
    worksheet = writer.sheets["Options"]
    writer.sheets['Options'] = worksheet

    chart1 = workbook.add_chart({'type': 'pie'})

# Configure the series. Note the use of the list syntax to define ranges:

    chart1.add_series({
    'name':       'Pie sales data',
    'data_labels': {'percentage': True, 'category': True},
    'categories': ["Options", 1, 5, 1, 6],
    'values':     ["Options", 2, 5, 2, 6]
})

# Add a title.
    chart1.set_title({'name': 'Call vs Put Frequency'})

# Set an Excel chart style. Colors with white outline and shadow.
    chart1.set_style(10)

# Insert the chart into the worksheet (with an offset).
    worksheet.insert_chart(chartCell, chart1)

def tickerFrequencyChart(chartCell, writer, workbook, worksheet, label1, label2):
    workbook = writer.book
    worksheet = writer.sheets["Options"]
    writer.sheets['Options'] = worksheet

    chart1 = workbook.add_chart({'type': 'pie'})

# Configure the series. Note the use of the list syntax to define ranges:

    chart1.add_series({
    'name':       'Ticker Frequency',
    'data_labels': {'value': True, 'category': True},
    'categories': ["Options", 3, 13, 3, 14],
    'values':     ["Options", 4, 13, 13, 14]
})

# Add a title.
    chart1.set_title({'name': 'Ticker Frequency'})

# Set an Excel chart style. Colors with white outline and shadow.
    chart1.set_style(10)

# Insert the chart into the worksheet (with an offset).
    worksheet.insert_chart(chartCell, chart1)

def writeOptionInfo(listOfTickers, optionNames, entryPrices, calls, puts):

# Configure the series. Note the use of the list syntax to define ranges:

    df1 = pd.DataFrame({"Ticker" : listOfTickers.keys(), "Frequency" : listOfTickers.values()})
    df2 = pd.DataFrame({"Option Name" : optionNames, "Entry Price" : entryPrices})
    df3 = pd.DataFrame({"Calls" : [calls], "Puts" : [puts]})
    writer = pd.ExcelWriter("OptionTrades.xlsx", engine = 'xlsxwriter')
    workbook = writer.book
    worksheet = workbook.add_worksheet('Options')
    writer.sheets['Options'] = worksheet
    df1.to_excel(writer, sheet_name="Options", startcol=13, startrow=3)
    df2.to_excel(writer, sheet_name="Options", startcol=0, startrow=0)
    df3.to_excel(writer, sheet_name="Options", startcol=4, startrow=1)
    CallPutChart("E8", writer, workbook, worksheet, "Calls", "Puts")
    tickerFrequencyChart("N20", writer, workbook, worksheet, "Ticker", "Amount")
    writer.save
    return writer




email, password = getCredentials()
loginToRH(email, password)
allPositions = []
allPositions = getAllOptions(allPositions)
frequentTickers = getFrequentTickers(allPositions)
optionNames, entryPrices, calls, puts = getOptionTrades(allPositions)
writer = writeOptionInfo(frequentTickers, optionNames, entryPrices, calls, puts)


writer.save()

r.logout()

