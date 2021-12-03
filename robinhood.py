import RobinhoodFunctions as rf

email, password = rf.getCredentials()
rf.loginToRH(email, password)
allPositions = []
allPositions = rf.getAllOptions(allPositions)
frequentTickers = rf.getFrequentTickers(allPositions)
rf.r.options.write_spinner()
rf.r.options.spinning_cursor()
optionNames, entryPrices, calls, puts = rf.getOptionTrades(allPositions)
writer, excelPath= rf.writeOptionInfo(frequentTickers, optionNames, entryPrices, calls, puts)


rf.closeAndSave(writer)

print("Options successfully exported to:", excelPath)
