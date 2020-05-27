#Ryan Valencia

from pyeda.inter import *

#the following is a hand calculated dictionary of prime numbers with list values of the even nodes they reach in even steps
hardBDDPE = {
	3:  [8, 18, 28],
	5:  [0, 10, 20, 30],
	7:  [2, 12, 22],
	11: [6, 16, 26],
	13: [8, 18, 28],
	17: [2, 12, 22],
	19: [4, 14, 24],
	23: [8, 16, 28],
	29: [4, 14, 24],
	31: [6, 16, 26]
}

PE_Nodes = { 
    ('00011', '01000'), ('00011', '10010'), ('00011', '11010'), 
    ('00101', '00000'), ('00101', '10100'), ('00101', '01010'),
	('00101', '11110'), ('00111', '00010'), ('00111', '01100'), 
	('00111', '10100'), ('01011', '10000'), ('01011', '00110'),
	('01011', '11010'), ('01101', '01000'), ('01101', '10010'),
	('01101', '11100'), ('10001', '00010'), ('10001', '01100'),
	('10001', '10110'), ('10011', '00010'), ('10011', '01110'),
	('10011', '11000'), ('10111', '00100'), ('10111', '10010'),
	('10111', '11100'), ('11101', '00010'), ('11101', '01110'),
	('11101', '11000'), ('11111', '00110'), ('11111', '10000'),
	('11111', '11100')
}


nodes = {
	0  : "00000",
    1  : "00001",
    2  : "00010",
    3  : "00011",
    4  : "00100",
    5  : "00101",
    6  : "00110",
    7  : "00111",
    8  : "01000",
    9  : "01001",
    10 : "01010",
    11 : "01011",
    12 : "01100",
    13 : "01101",
    14 : "01110",
    15 : "01111",
    16 : "10000",
    17 : "10001",
    18 : "10010",
    19 : "10011",
    20 : "10100",
    21 : "10101",
    22 : "10110",
    23 : "10111",
    24 : "11000",
    25 : "11001",
    26 : "11010",
    27 : "11011",
    28 : "11100",
    29 : "11101",
    30 : "11110",
    31 : "11111"
}

#use R to denote the set of all edges in G
def createEdgeList():
	for i in range(0, 31):
		for j in range (0, 31):
			if ((i + 3)%32 == j%32) or ((i + 8)%32 == j%32):
				edgeList.append((f'{nodes[i]}', f'{nodes[j]}'))
	#for edge in edgeList:
	#	print(edge)

#create R as an expression, then make it a BDD
def createExp(edges):
	edgeExp = []
	for pair in edges:
		expression = ''
		count = 1
		for i in pair[0]:
			if(i == '1'):
				expression += 'x' + str(count) + ' & '
			else:
				expression += '~x' + str(count) + ' & '
			count += 1
		count = 1
		for i in pair[1]:
			if(i == '1'):
				expression += 'y' + str(count) + ' & '
			else:
				expression += '~y' + str(count) + ' & '
			count += 1
		expression = expression[:-3]
		edgeExp.append(expression)

	exp = edgeExp[0]
	for i in edgeExp:
		exp = exp or i
	return exp

#create [even] as an expression, then make it a BDD
def createEvenExp():
	evens = ["00000","00010","00100","00110","01000","01010",
            "01100","01110","10000","10010","10100","10110",
            "11000","11010","11100","11110"]
	for even in evens:
		expression = ''
		count = 1
		for i in even:
			if(i == '1'):
				expression += 'y' + str(count) + ' & '
			else:
				expression += '~y' + str(count) + ' & '
			count += 1
		expression = expression[:-3]
		evenExpList.append(expression)
	E = evens[0]
	for i in evens:
		E = E or i
	return E


#create [prime] as an expression, then make it a BDD
def createPrimeExp():
	primes = ["00011","00101","00111","01011","01101","10001","10011","10111","11101","11111"]
	primeExp = []
	for prime in primes:
		expression = ''
		num = 1
		for bit in prime:
			if (bit == '1'):
				expression += 'x' + str(num) + ' & '
			else:
				expression += '~x' + str(num) + ' & '
			num += 1    
		expression = expression[:-3]
		primeExp.append(expr(expression))

	P = primeExp[0]
	for i in primeExp:
		P = P | i 
	return P


def composeBDD(quant1, quant2):
	X = bddvars('x', 5)
	Y = bddvars('y', 5)
	Z = bddvars('z', 5)
	for i in range(0,5):
		quant1 = quant1.compose({Y[i]: Z[i]})
		quant2 = quant2.compose({Y[i]: Z[i]})


#3.5
def formulateStatement(input):
	A = bddvars('a', 5)
	B = bddvars('b', 5)

	for item in range(0,5):
		input = input.compose({A[item]: B[item]})

	if(input.smoothing() == 1):
		print("TRUE")
	else:
		print("FALSE")

#Part 4 the following functions look into the dictionary BDDPE
#BDDPE has keys of our set of primes and list values for even nodes that can be reached in even steps
#a - the following function, when given a prime number, u, returns a value from the respective list 
def giveEven(u):
	val = -1
	for key in hardBDDPE:
		if key == u:
			vList = hardBDDPE[key]
			val = vList[0]
	return val

#b - the following, when given a prime, u, and an even, v, if v is a value in the list of evens
def checkPrimeEven(u, v):
	val = False
	for key in hardBDDPE:
		if key == u:
			vlist = hardBDDPE[key]
			for even in vlist:
				if v == even:
					val = True
	return val

if __name__ == "__main__":
	edgeList = []
	evenExpList = []
	primeExpList = []

	#steps 3.1 - 3.3
	createEdgeList()
	R = createExp(edgeList)
	RR = expr2bdd(expr(R))

	EVE = createEvenExp()
	EVEN = expr2bdd(expr(EVE))

	PRIM = createPrimeExp()
	PRIME = expr2bdd(expr(PRIM))

	#step 3.4
	BDDPE = createExp(PE_Nodes)
	BDDPE = expr(BDDPE)
	BDDPE2 = expr2bdd(BDDPE)

	#3.5
	print("steps 3.1 thru 3.4 dont have any outputs")
	print("step 3.5:")
	formulateStatement(BDDPE2)

	Closure = RR
	while True:
		prop = Closure
		Closure = prop | composeBDD(prop, RR)

		if Closure.equivalent(prop):
			break
	RR = prop


	#part 4 calls
	print("part 4:")
	u = 23
	v = giveEven(u)
	print("The prime " + str(u) + " can reach the value " + str(v) + " in an even number of steps")

	incorrect = 14
	correct = 16

	test = checkPrimeEven(u, incorrect)
	print("checking if " + str(incorrect) + " is a v for the u " + str(u) + ":")
	print(test)

	test = checkPrimeEven(u, correct)
	print("checking if " + str(correct) + " is a v for the u " + str(u) + ":")
	print(test)

