from COMMONFUNCTIONS import *
from CUSTOMERS import *
from operator import itemgetter
import time
import datetime
import csv
import numpy as np
	
class reservations(object):

	def __init__(self,filename):
		self.filename = filename

	def cancelReservation(self):
		"""
			Cancel a registered reservation
		"""
		
		cf = commonfunctions(self.filename)
		allReservations = cf.csvToListOfRow()
		custInfo = []
		
		entry1 = 1
		
		while entry1 == 1:
			try:
				time.sleep(0.5)
				print()
				custID = input( "Enter Guest ID : " )
				custID = int(custID)
			except:
				custID  = 9999999
			print()
			
			if custID not in [9999999]:
				cust = customers('CUSTOMERS.csv')
				custInfo =  cust.csvGetCustInfo(custID)
				if len(custInfo) == 1:
					print("The entered Guest ID is not registered")
				else:
					entry1 = 2
			else:
				time.sleep(0.5)
				print("Please enter a number")

		custInfo[0].append('Active')
		custInfo[1].append('Y')
		
		custReservations = cf.returnListFromMainList(allReservations,custInfo)
		if len(custReservations) == 1:
			time.sleep(0.5)
			print()		
			print("You have no reservations")
		else:
			custReservations_DF = cf.convertListToDf(custReservations)
			custReservations_DF1 = custReservations_DF.ix[:,6:11]
			custReservations_DF1.index = np.arange(1,len(custReservations_DF1)+1)
			custReservations_DF1.index.name = 'Rsv ID'
			print("You have the following reservations:")
			time.sleep(0.5)
			print()
			print(custReservations_DF1)
		
			try:
				time.sleep(0.5)
				print()
				RsvID = input( "Enter Rsv ID : " )
				RsvID = int(RsvID)
			except:
				RsvID  = 9999999
			print()
			
			for i in range(1,len(allReservations)):
				if allReservations[i] == custReservations[RsvID]:
					allReservations[i][11] = 'N'
			allReservations_DF = cf.convertListToDf(allReservations)
			allReservations_DF.to_csv('RESERVATIONS.csv',index=False)

			time.sleep(0.5)
			print("The reservation has been cancelled")

			custReservations = cf.returnListFromMainList(allReservations,custInfo)
			if len(custReservations) == 1:
				time.sleep(0.5)
				print()		
				print("You have no reservations left")
			else:
				custReservations_DF = cf.convertListToDf(custReservations)
				custReservations_DF1 = custReservations_DF.ix[:,6:11]
				custReservations_DF1.index = np.arange(1,len(custReservations_DF1)+1)
				custReservations_DF1.index.name = 'Rsv ID'	
				time.sleep(0.5)
				print()
				print("You have the following reservations:")
				time.sleep(0.5)
				print()
				print(custReservations_DF1)
		
	def markActivityAsN(self):
		"""
			Marks reservation which are not
			in Active state as 'N'
		"""
		cf = commonfunctions(self.filename)
		allReservations = cf.csvToListOfRow()
		presentDate = datetime.datetime.now()
		
		for i in range(1,len(allReservations)):
			oldReservation = datetime.datetime.strptime(allReservations[i][10],"%Y-%m-%d %H:%M:%S")
			if oldReservation < presentDate:
				allReservations[i][11] = 'N'

		allReservations_DF = cf.convertListToDf(allReservations)
		allReservations_DF.to_csv('RESERVATIONS.csv',index=False)
				

