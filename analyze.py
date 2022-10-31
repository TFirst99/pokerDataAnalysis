#card filter
import re
import pandas as pd
import openpyxl

#all the regex patterns
cardPattern = "card: \[[0-9A-Z]+[a-zA-Z]"
flopPattern = "FLOP"
raisePattern = "Player IlxxxlI raises \(\d{1,3}\.\d{2}\)|Player IlxxxlI raises \(\d{1,3}\)"
raiseNumberPattern = "\d{1,3}\.\d{2}|\d{1,3}"
actionPattern = 'Player IlxxxlI folds|Player IlxxxlI calls|Player IlxxxlI raises|Player IlxxxlI caps|Player IlxxxlI allin|Player IlxxxlI checks|Uncalled bet \(.{1,4}\) returned to IlxxxlI'
gameEndedPattern = 'Game ended'
winPattern = "\*Player IlxxxlI .* Wins: \d{1,3}\.\d{2}|\*Player IlxxxlI .* Collects: \d{1,3}\.\d{2}"
lossPattern = "^Player IlxxxlI .* Loses: \d{1,3}\.\d{2}"
winPattern2 = "\*Player IlxxxlI .* Wins: \d{1,3}\.$|\*Player IlxxxlI .* Collects: \d{1,3}\."
lossPattern2 = "^Player IlxxxlI .* Loses: \d{1,3}\.$"
winZeroPattern = "^Player IlxxxlI .* Wins: 0"
numberPattern = "\d{1,3}\.\d{2}\'\]$"
numberPattern2 = "\d{1,3}\.\'\]$"

#pathfiles
pathfile = "Export Holdem Manager 2.0 12302016144830.txt"

#lists we will find
handOutcomeProfit = []
combinedCardList = []
shortenedRaise = []
preRaiseAmount = []
actionList = []

def searchMatches(pattern):
	with open(pathfile, encoding='utf-8') as text:
		return [re.findall(pattern, line) for line in text]
	 
#Does all the searches and puts them into lists
initialCards = searchMatches(cardPattern)
print("1/10 searches done")
initialFlop = searchMatches(flopPattern)
print("2/10 searches done")
initialRaises = searchMatches(raisePattern)
print("3/10 searches done")
initialAction = searchMatches(actionPattern)
print("4/10 searches done")
gameEnded = searchMatches(gameEndedPattern)
print("5/10 searches done")
initialWin = searchMatches(winPattern)
print("6/10 searches done")
initialWin2 = searchMatches(winPattern2)
print("7/10 searches done")
initialLoss = searchMatches(lossPattern)
print("8/10 searches done")
initialLoss2 = searchMatches(lossPattern2)
print("9/10 searches done")
initialWinZero = searchMatches(winZeroPattern)
print("10/10 searches done")

#isolates the cards from the rest of the string
shortenedList = list(map(lambda x : str(x)[-4:-2],initialCards))

#removes empty elements and combines cards into hands
ind = 0
while ind < len(shortenedList):
	if shortenedList[ind] and shortenedList[ind + 1]:
		combinedCardList.append(shortenedList[ind] + shortenedList[ind + 1])
	ind += 1
print("Cards combined")

#creates a list with all the raises
ind = 0
while ind < len(initialRaises):
	if initialRaises[ind]:
		number = re.search(raiseNumberPattern, str(initialRaises[ind])).group(0)
		shortenedRaise.append(number)
	else:
		shortenedRaise.append("0")
	ind += 1

#find raises that occur between a hand being dealt and the flop
ind = 0
while ind < len(shortenedList):
	if shortenedList[ind] and not shortenedList[ind+1]:
		indCheck = ind + 1
		while indCheck < len(shortenedRaise):
			if shortenedRaise[indCheck] != "0":
				preRaiseAmount.append(shortenedRaise[indCheck])
				break
			elif initialFlop[indCheck]:
				preRaiseAmount.append("0")
				break
			else:
				indCheck += 1
	ind += 1
print("Pre-flop raises found")

#assembles a list of first actions
ind = 0
while ind < len(initialCards):
	if initialCards[ind] and not initialCards[ind+1]:
		indCheck = ind + 1
		while indCheck < len(initialAction):
			if initialAction[indCheck]:
				actionList.append(initialAction[indCheck])
				break
			elif gameEnded[indCheck]:
				break
			else:
				indCheck += 1
	ind += 1
print("First actions found")

#finds the profit/loss of each hand
ind = 0
while ind < len(initialWin):
	if initialWin[ind]:
		profit = re.search(numberPattern, str(initialWin[ind])).group(0)
		profit = profit[:-2]
		handOutcomeProfit.append(profit)
		ind += 1
	elif initialWin2[ind]:
		profit = re.search(numberPattern2, str(initialWin2[ind])).group(0)
		profit = profit[:-3]
		handOutcomeProfit.append(profit)
		ind += 1
	elif initialLoss[ind]:
		profit = re.search(numberPattern, str(initialLoss[ind])).group(0)
		profit = "-" + profit[:-2]
		handOutcomeProfit.append(profit)
		ind += 1
	elif initialLoss2[ind]:
		profit = re.search(numberPattern2, str(initialLoss2[ind])).group(0)
		profit = "-" + profit[:-3]
		handOutcomeProfit.append(profit)
		ind += 1
	elif initialWinZero[ind]:
		profit = 0
		handOutcomeProfit.append(profit)
		ind += 1
	else:
		ind +=1
print("Profits found")

#uses pandas to create a dataframe that contains the cards, actions, and outcome of every hand.
dataframe1 = pd.DataFrame(list(zip(combinedCardList,actionList, handOutcomeProfit, preRaiseAmount)), columns = ['Cards', 'Action', 'Profit', 'Pre-Raise Amount'])

#prompts the user to either print a list, dataframe, or output an excel file
while True:
	try:
		print("Lists: initialCards, initialFlop, initialRaises, initialAction, gameEnded, initialWin, initialWin2, initialLoss, initialLoss2, initialWinZero, dataframe1")
		print("Actions: output, stop")
		printSelection = input("print List/Action:  ")
		if printSelection == "initialCards":
			print(initialCards)
			print("Elements:" ,len(initialCards))
		elif printSelection == "initialWin":
			print(initialWin)
			print("Elements:" ,len(initialWin))
		elif printSelection == "initialFlop":
			print(initialFlop)
			print("Elements:" ,len(initialFlop))
		elif printSelection == "initialRaises":
			print(initialRaises)
			print("Elements:" ,len(initialRaises))
		elif printSelection == "shortenedRaise":
			print(shortenedRaise)
			print("Elements:" ,len(shortenedRaise))
		elif printSelection == "shortenedList":
			print(shortenedList)
			print("Elements:" ,len(shortenedList))
		elif printSelection == "combinedCardList":
			print(combinedCardList)
			print("Elements:" ,len(combinedCardList))
		elif printSelection == "preRaiseAmount":
			print(preRaiseAmount)
			print("Elements:" ,len(preRaiseAmount))
		elif printSelection == "initialAction":
			print(initialAction)
			print("Elements:" ,len(initialAction))
		elif printSelection == "actionList":
			print(actionList)
			print("Elements:" ,len(actionList))
		elif printSelection == "gameEnded":
			print(gameEnded)
			print("Elements: " ,len(gameEnded))
		elif printSelection == "handOutcomeProfit":
			print(handOutcomeProfit)
			print("Elements: " ,len(handOutcomeProfit))
		elif printSelection == "initialLoss":
			print(initialLoss)
			print("Elements: ", len(initialLoss))
		elif printSelection == "initialWinZero":
			print(initialWinZero)
			print("Elements: ", len(initialWinZero))
		elif printSelection == "dataframe1":
			print(dataframe1)
		elif printSelection == "output":
			dataframe1.to_excel('pokerData.xlsx')
		elif printSelection == "stop":
			print("STOPPING")
			exit()
		else:
			print("Not Found")
	except NameError:
		print ("idk error")
		break