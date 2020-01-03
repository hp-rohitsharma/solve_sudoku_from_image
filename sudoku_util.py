
def getAllEmptyCells(input):
	List = []
	for i in range(9):
		for j in range(9):
			if input[i][j] == 0:		
				List.append([ i, j ]) 	
	return List

def getPossibleValues(i, j, input):
	usedValues = set()	
	for x in range(len(input)):			
		usedValues.add(input[i][x])
	for y in range(len(input)):	
		usedValues.add(input[y][j])
	cs = j - j%3
	ce = j + (2 -j%3)

	rs = i - i%3
	re = i + (2 -i%3)

	for r in range(rs, re + 1):	
		for c in range(cs, ce + 1):	
			usedValues.add(input[r][c])

	possiblevalues = []
	
	for z in range(1, 10):	
		if z not in usedValues:
			possiblevalues.append(z)
	
	return possiblevalues

def solved(input):
	flags = [False for i in range(9)]
	on = False
	for j in range(9):
		for i in range(9):	
			index = input[j][i]
			if flags[index - 1] == on:
				flags[index - 1] = not on
			else:
				return False
		on = not on
	
	for j in range(9):
		for i in range(9):	
			index = input[i][j]
			if flags[index - 1] == on:
				flags[index -1 ] = not on
			else:
				return False
		on = not on

	squareStarts = [
		[0,0], [0,3],[0,6],
		[3,0], [3,3],[3,6],
		[6,0], [6,3],[6,6]
	]
			
	for k in range(len(squareStarts)):
		rs = squareStarts[k][0]
		cs = squareStarts[k][1]
		for j in range(rs, 3 + rs):
			for i in range(cs, 3 + cs):	
				index = input[i][j]
				if flags[index - 1] == on:
					flags[index -1 ] = not on
				else:
					return False
		on = not on

	return True

def dp(i, j, k, input, emptyCells):
	#if k > 40:
		#print(k,'  ' , len(emptyCells),'  ' ,k == len(emptyCells))
	possibleValues = getPossibleValues(i, j, input)
	#print(possibleValues)
	for possibleValue in possibleValues:
		input[i][j] = possibleValue		
		if k == len(emptyCells):
			if solved(input) == True:				
				return True
		else:
			next = emptyCells[k]
			status = dp(next[0], next[1], k + 1, input, emptyCells)			
			if status == True:
				return True

	input[i][j] = 0			
	return False

def solve(array):
	emptyCells = getAllEmptyCells(array)
	if(len(emptyCells) == 0):
		print('Already Solved')
		return array
	next = emptyCells[0]
	status = dp(next[0], next[1], 1, array, emptyCells)
	if status == True:
		print('Solved')						
		return array
	else:
		print('Cant be solved')
	return array