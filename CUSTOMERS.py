import csv
import time
import pandas as pd

class customers(object):

	def __init__(self,filename):
		self.filename = filename

	def csvGetCustInfo(self,custID):
		""" 
			Converts the data from '.csv' file to list 
			where row is presented as a list
		"""
		data = []
		newdata = []
		with open(self.filename, "rt", encoding='ascii') as csvfile:
			csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
			data = list(csvreader)
			newdata = [data[0]]
			for i in range(0,len(data)):
				if data[i][0] == str(custID):
					newdata.extend([data[i]])
					break
		return newdata
	
