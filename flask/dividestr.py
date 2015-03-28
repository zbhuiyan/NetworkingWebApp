import re

def divideparts(str):

	

	divided = []
	
	for n in str.split('\n'):
		divided.append(n)

	print divided


divideparts('and\nthere is\nmany')