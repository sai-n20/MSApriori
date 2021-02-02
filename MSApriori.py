import os

__location__ = os.path.realpath(os.path.join(
    os.getcwd(), os.path.dirname(__file__)))

mis_values = dict()
tempDict = dict()
itemCount = dict()
transactionList = list()
L = list()
candidateList = list([] for _ in range(10))

def readFiles():
	global sdcValue, transactionCount
	with open(os.path.join(__location__, 'parameters.txt')) as parameterFile:
		for mis in parameterFile:
			if(mis.find('SDC') > -1):
				sdcValue = float(mis.replace(' ', '').rstrip().split('=')[1])

			if(mis.find('rest') > -1):
				tempDict = mis.replace(' ', '').replace('MIS', '').replace('(', '').replace(')', '').rstrip().split('=')
				mis_values['rest'] = float(tempDict[1])

			elif(mis.find('MIS') > -1):
				tempDict = mis.replace(' ', '').replace('MIS', '').replace('(', '').replace(')', '').rstrip().split('=')
				mis_values[int(tempDict[0])] = float(tempDict[1])
	parameterFile.close()

	with open(os.path.join(__location__, 'input.txt')) as dataFile:
		for trans in dataFile:
			transactionList.append(list())
			tempDict = trans.replace(' ', '').split(',')
			for item in tempDict:
				item = int(item)
				transactionList[len(transactionList) - 1].append(item)
				if(itemCount.get(item)):
					itemCount[item] = itemCount.get(item) + 1
				else:
					itemCount[item] = 1
		transactionCount = len(transactionList)
	dataFile.close()

readFiles()
mis_values = {k: v for k, v in sorted(mis_values.items(), key=lambda item: item[1])}

for key in itemCount:
    if((itemCount.get(key) / transactionCount) >= next(iter(mis_values.values()))):
        L.append(key)

for lo in range (0, len(L)):
	if(mis_values.get(L[lo])):
		supportValue = mis_values.get(L[lo])
	else:
		supportValue = mis_values['rest']
	if (itemCount[L[lo]] / transactionCount) >= supportValue:
		for hi in range( lo + 1, len(L)):
			if (itemCount[L[hi]] / transactionCount) >= supportValue and abs((itemCount[L[hi]] / transactionCount) - (itemCount[L[lo]] / transactionCount)) <= sdcValue:
				candidateList[2].append(list())
				candidateList[2][len(candidateList[2])-1].append(L[lo])
				candidateList[2][len(candidateList[2])-1].append(L[hi])

print(sdcValue)
print(mis_values)
print(itemCount)
print(transactionCount)
print(transactionList)
print(L)
print(candidateList)