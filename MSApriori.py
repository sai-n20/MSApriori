import os

__location__ = os.path.realpath(os.path.join(
    os.getcwd(), os.path.dirname(__file__)))

mis_values = dict()
tempDict = dict()
itemCount = dict()
transactionList = list()
L = list()
candidateList = list([] for i in range(10))
sdcValue = 1

# supportCount is itemcount here
# n is transactionCount


def readFiles():
	global sdcValue, transactionCount
	with open(os.path.join(__location__, 'Data/As1_MIS3.txt')) as parameterFile:
		for mis in parameterFile:
			if(mis.find('SDC') > -1):
				sdcValue = float(mis.replace(' ', '').rstrip().split('=')[1])

			if(mis.find('rest') > -1):
				tempDict = mis.replace(' ', '').replace('MIS', '').replace(
				    '(', '').replace(')', '').rstrip().split('=')
				mis_values['rest'] = float(tempDict[1])

			elif(mis.find('MIS') > -1):
				tempDict = mis.replace(' ', '').replace('MIS', '').replace(
				    '(', '').replace(')', '').rstrip().split('=')
				mis_values[int(tempDict[0])] = float(tempDict[1])
	parameterFile.close()

	with open(os.path.join(__location__, 'Data/As1_Sample3.txt')) as dataFile:
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

# Sort MIS values
mis_values = {k: v for k, v in sorted(mis_values.items(), key=lambda item: item[1])}

# Loop through item counts to formulate L array
for key in itemCount:
	# Element only needs to pass lowest MIS value constraint
    if((itemCount.get(key) / transactionCount) >= next(iter(mis_values.values()))):
        L.append(key)

def MISvalue(item):
	if(mis_values.get(item)):
		return mis_values.get(item)
	else:
		return mis_values['rest']

# Form 1 item frequent itemset
for key in itemCount:
	# Element needs to pass MIS constraint
	if (itemCount[key] / transactionCount) >= MISvalue(key):
		candidateList[1].append(list())
		candidateList[1][len(candidateList[1])-1].append(key)

def level2candidategen():
	# Consider first element of a new itemset in L
	for lo in range(0, len(L)):
		# Element needs to pass MIS constraint
		if (itemCount[L[lo]] / transactionCount) >= MISvalue(L[lo]):
			# Find 2nd candidate element
			for hi in range(lo + 1, len(L)):
				# Element needs to pass MIS constraint and SDC constraint
				if (itemCount[L[hi]] / transactionCount) >= MISvalue(L[lo]) and abs((itemCount[L[hi]] / transactionCount) - (itemCount[L[lo]] / transactionCount)) <= sdcValue:
					# Append list and add 2 elements to this newly appended list
					candidateList[2].append(list())
					candidateList[2][len(candidateList[2])-1].append(L[lo])
					candidateList[2][len(candidateList[2])-1].append(L[hi])


def MSCandidate_gen(F):
    C_k = []
    for i in F:
        for j in F:
            if i!=j:
                sCount1 = itemCount[i[len(i)-1]]/transactionCount
                sCount2 = itemCount[j[len(j)-1]]/transactionCount
                if(i[len(i)-1]<j[len(j)-1]) and (i[:-1]==j[:-1]) and sdcValue >= abs(sCount1-sCount2):
                    C_k.append(i+j[-1:])
                    c = i+j[-1:]
                    
                    for k in range(1,len(c)+1):
                        s = c[:k-1]+c[k:]
                        if c[0] in s or MISvalue(c[1]) == MISvalue(c[0]):
                            if s not in F:
                                C_k.remove(c)
                                break
    return C_k


loopIterator = 2
while(len(candidateList[loopIterator - 1]) > 0):
	if(loopIterator == 2):
		level2candidategen()
	else:
		candidateList[loopIterator] = MSCandidate_gen(candidateList[loopIterator - 1])
	loopIterator += 1

def write_output():
	with open('result.txt', 'w') as output:
		for itemset in candidateList:
			if(len(itemset) > 0):
				output.write("(Length-{} {}\n".format(len(itemset[0]), len(itemset)))
				for item in itemset:
					output.write("\t(")
					for index, elem in enumerate(item):
						if(index < len(item) - 1):
							output.write("{} ".format(elem))
						else:
							output.write("{}".format(elem))
					output.write(")\n")
				output.write(")\n")
	output.close()
write_output()