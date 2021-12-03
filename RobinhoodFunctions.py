from datetime import date, datetime
import robin_stocks.robinhood as r
from pyrh import Robinhood
import pandas as pd
import csv
from collections import Counter
from robin_stocks.robinhood.export import export_completed_option_orders
import xlsxwriter as xl
from jproperties import Properties



def getCredentials():
    configs = Properties()

    with open(r'C:\Users\cthax\git\Stonk-Tracker\credentials.properties', 'rb') as read_prop:
     configs.load(read_prop)
	
    email = configs.get("email").data
    password = configs.get("password").data
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


def CallPutChart(chartCell, writer, workbook, worksheet, label1, label2):
    workbook = writer.book
    worksheet = writer.sheets["Options"]
    writer.sheets['Options'] = worksheet

    chart1 = workbook.add_chart({'type': 'pie'})

# Configure the series. Note the use of the list syntax to define ranges:

    chart1.add_series({
    'name':       'Pie sales data',
    'data_labels': {'percentage': True, 'category': True},
    'categories': ["Options", 0, 4, 0, 5],
    'values':     ["Options", 1, 4, 1, 5]
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
    'categories': ["Options", 1, 13, 10, 13],
    'values':     ["Options", 1, 14, 10, 14]
})

# Add a title.
    chart1.set_title({'name': 'Ticker Frequency'})

# Set an Excel chart style. Colors with white outline and shadow.
    chart1.set_style(10)

# Insert the chart into the worksheet (with an offset).
    worksheet.insert_chart(chartCell, chart1)

def writeOptionInfo(listOfTickers, optionNames, entryPrices, calls, puts):

# Configure the series. Note the use of the list syntax to define ranges:
    excelPath = r"C:\Users\cthax\Desktop\OptionTrades.xlsx"

    df1 = pd.DataFrame({"Ticker" : listOfTickers.keys(), "Frequency" : listOfTickers.values()})
    df2 = pd.DataFrame({"Option Name" : optionNames, "Entry Price" : entryPrices})
    df3 = pd.DataFrame({"Calls" : [calls], "Puts" : [puts]})
    df4 = pd.DataFrame({"Last updated:" : [datetime.now().strftime("%d/%m/%Y %H:%M")]})
    writer = pd.ExcelWriter(excelPath, engine = 'xlsxwriter',  datetime_format='mmm d yyyy hh:mm')
    workbook = writer.book
    worksheet = workbook.add_worksheet('Options')
    writer.sheets['Options'] = worksheet
    df1.to_excel(writer, sheet_name="Options", startcol=13, startrow=0, index= False)
    df2.to_excel(writer, sheet_name="Options", startcol=0, startrow=0, index= False)
    df3.to_excel(writer, sheet_name="Options", startcol=4, startrow=0, index= False)
    df4.to_excel(writer, sheet_name="Options", startcol=7, startrow=0, index= False)

    for i, col in enumerate(df2.columns):
        # find length of column i
        column_len = df2[col].astype(str).str.len().max()
        # Setting the length if the column header is larger
        # than the max column value length
        column_len = max(column_len, len(col)) + 2
        # set the column length
        worksheet.set_column(i, i, column_len)


    CallPutChart("E12", writer, workbook, worksheet, "Calls", "Puts")
    tickerFrequencyChart("N12", writer, workbook, worksheet, "Ticker", "Amount")
    writer.save
    return writer, excelPath


def closeAndSave(writer):
    writer.save()
    r.logout()