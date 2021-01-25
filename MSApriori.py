import os

__location__ = os.path.realpath(os.path.join(
    os.getcwd(), os.path.dirname(__file__)))

sdcValue = 0.0
transactionCount = 0
mis_values = dict()
tempDict = dict()
itemList = list()
itemCount = dict()
transactionList = list()

with open(os.path.join(__location__, 'input.txt')) as f:
	for trans in f:
		transactionList.append(list())
		tempDict = trans.replace(' ', '').split(',')
		for item in tempDict:
			item = int(item)
			transactionList[len(transactionList) - 1].append(item)
			if(itemCount.get(item)):
				itemCount[item] = itemCount.get(item) + 1
	transactionCount = len(transactionList)

with open(os.path.join(__location__, 'parameters.txt')) as f:
	for mis in f:
		if(mis.find('SDC') > -1):
			sdcValue = float(mis.replace(' ', '').rstrip().split('=')[1])

		if(mis.find('rest') > -1):
			tempDict = mis.replace(' ', '').replace('MIS', '').replace('(', '').replace(')', '').rstrip().split('=')
			mis_values['rest'] = float(tempDict[1])

		elif(mis.find('MIS') > -1):
			tempDict = mis.replace(' ', '').replace('MIS', '').replace('(', '').replace(')', '').rstrip().split('=')
			mis_values[int(tempDict[0])] = float(tempDict[1])

	items = sorted(mis_values, key=mis_values.__getitem__)
	for item in items:
		itemList.append(item)
		itemCount[item] = 0

print(sdcValue)
print(mis_values)
print(itemList)
print(itemCount)
print(transactionCount)
print(transactionList)