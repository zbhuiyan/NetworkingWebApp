import csv
import output




def make_default_dict():
'''Makes default dictionary, with given keys and empty values. These values are appended later from main file'''

	keys = ['Name', 'Email', 'Company', 'Phone Number']
	defaultdict = dict.fromkeys(keys, None)
	print defaultdict




def writecsvdict():
'''Creates a csv file taking the default dict from previous function'''

	# f = open('output2.csv', 'wb')
	# w = csv.DictWriter(f, defaultdict.keys())

	writer = csv.writer(open('output2.csv', 'wb'))
	for key, value in defaultdict.items():
		writer.writerow([key, value])
	return writer

	








make_default_dict()
writecsvdict()