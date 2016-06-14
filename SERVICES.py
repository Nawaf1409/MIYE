import csv
import time
import copy
import datetime
from COMMONFUNCTIONS import *
from CUSTOMERS import *

class services(object):

	def __init__(self,filename):
		self.filename = filename

	def printServices(self):
		time.sleep(0.5)
		cf = commonfunctions('SERVICES.csv')
		allService = cf.csvToListOfRow()
		allService_DF = cf.convertListToDf(allService)
		allService_DF = allService_DF.set_index('Service ID')
		print(allService_DF)
		
	def addService(self):
		time.sleep(0.5)
		print("")
		cf = commonfunctions('SERVICES.csv')
		allService = cf.csvToListOfRow()	
		allService_DF = cf.convertListToDf(allService)
		allService_DF = allService_DF.set_index('Service ID')
		print("These are the present services:")
		time.sleep(0.5)
		print("")		
		print(allService_DF)
		
		entry1 = 1
		
		while entry1 == 1:
			try:
				time.sleep(0.5)
				print()			
				serviceId1 = input("Enter the Service ID : ")
				serviceId = int(serviceId1)
			except:
				serviceId  = 9999999

			if serviceId not in [9999999]:
				serviceId = serviceId1
				entry1 = 2
			else:
				time.sleep(0.5)
				print("Please enter a number")	
			
		serviceName = input("Enter the Service Name : ")
		serviceType = input("Enter the Service Type : ")
	
		entry2 = 1
		
		while entry2 == 1:
			try:			
				rate1 = input("Enter the Rate ($/min) : ")
				rate = float(rate1)
			except:
				rate  = 9999999
			
			if rate not in [9999999]:
				rate = rate
				entry2 = 2
			else:
				time.sleep(0.5)
				print("Please enter a number")

		entry3 = 1
		
		while entry3 == 1:
			try:			
				duration = input("Enter Duration : ")
				duration = int(duration)
			except:
				duration  = 9999999
			
			if duration not in [9999999]:
				duration = duration
				entry3 = 2
			else:
				time.sleep(0.5)
				print("Please enter a number")		
		
		allService.append([str(serviceId),serviceName,serviceType,str(rate),str(duration)])
		allService_DF = cf.convertListToDf(allService)
		allService_DF.to_csv('SERVICES.csv',index=False)
		time.sleep(0.5)
		print("")
		print("Service has been added")	
		time.sleep(0.5)
		print("")
		cf = commonfunctions('SERVICES.csv')
		allService = cf.csvToListOfRow()	
		allService_DF = cf.convertListToDf(allService)
		allService_DF = allService_DF.set_index('Service ID')
		print(allService_DF)
		
	def availService(self):
		"""
			All available services at a given day & time
		"""

		entry2 = 1
		entry3 = 1
		while entry2 == 1 and entry3 == 1:
			time.sleep(0.5)
			print()
			while entry2 == 1:
				try:			
					inputDate = input("Enter date in format(MM-DD-YYYY): ")
					month, day, year = map(int, inputDate.split('-'))
					entry2 = 0
				except:
					print("Wrong date format")

			while entry3 == 1:
				try:			
					inputTime = input("Enter Time(HH:MM): ")
					hour, minute = map(int, inputTime.split(':'))
					entry3 = 0
				except:
					print("Wrong time format")	
			
		userDateTime = datetime.datetime(year,month,day,hour,minute,0,0)
			
		cf = commonfunctions('RESERVATIONS.csv')
		allReservations = cf.csvToListOfRow()
		
		notAvailServiceName = [[allReservations[0][5],allReservations[0][6],allReservations[0][7],allReservations[0][8],allReservations[0][9]]]

		for i in range(1,len(allReservations)):
			timeBooked = int(allReservations[i][9])
			startTime = datetime.datetime.strptime(allReservations[i][10],"%Y-%m-%d %H:%M:%S")
			endTime = datetime.datetime.strptime(allReservations[i][10],"%Y-%m-%d %H:%M:%S") + datetime.timedelta(minutes=timeBooked)
			active = allReservations[i][11]
			if userDateTime >= startTime and userDateTime <= endTime and active == 'Y':
				newList = [allReservations[i][5],allReservations[i][6],allReservations[i][7],allReservations[i][8],allReservations[i][9]]
				if newList not in notAvailServiceName:
					notAvailServiceName.append(newList)

		cf_serve = commonfunctions('SERVICES.csv')
		allServices = cf_serve.csvToListOfRow()
		
		availServiceName = [[allReservations[0][5],allReservations[0][6],allReservations[0][7],allReservations[0][8],allReservations[0][9]]]
		availServiceName.append(allServices[1])
		availServiceName.append(allServices[2])
		
		for i in range(3,len(allServices)):
			if allServices[i] not in notAvailServiceName:
				availServiceName.append(allServices[i])
		
		time.sleep(0.5)
		print()
		availServiceName_DF = cf.convertListToDf(availServiceName)
		availServiceName_DF = availServiceName_DF.set_index('Service ID')
		print(availServiceName_DF)
			
	def availTimeService(self):
		"""
			display of available times for a particular service 
			between a given start and end day & time
		"""
		time.sleep(0.5)
		print()
		cf = commonfunctions('SERVICES.csv')
		allService = cf.csvToListOfRow()		
		allService_DF = cf.convertListToDf(allService)
		allService_DF = allService_DF.set_index('Service ID')
		print(allService_DF)

		entry = 1
		
		while entry == 1:
			try:		
				time.sleep(0.5)
				print()	
				serviceId1 = input("Enter the Service ID : ")
				serviceId = int(serviceId1)
			except:
				serviceId  = 9999999

			if serviceId not in [9999999]:
				if cf.checkServiceID(serviceId1):
					serviceId = serviceId1
					entry = 2
				else:
					time.sleep(0.5)
					print()			
					print("No Service ID with this value")	
			else:
				time.sleep(0.5)
				print("Please enter a number")	
				
		entry1 = 1
		entry2 = 1
		
		while entry1 == 1 and entry2 == 1:
			time.sleep(0.5)
			print()
			while entry1 == 1:
				try:			
					inputDate1 = input("Enter Start date in format(MM-DD-YYYY): ")
					month1, day1, year1 = map(int, inputDate1.split('-'))
					entry1 = 0
				except:
					print("Wrong date format")

			while entry2 == 1:
				try:			
					inputTime1 = input("Enter Start Time(HH:MM): ")
					hour1, minute1 = map(int, inputTime1.split(':'))
					entry2 = 0
				except:
					print("Wrong time format")	
			
		startDateTime = datetime.datetime(year1,month1,day1,hour1,minute1,0,0)
	
		entry3 = 1
		entry4 = 1
		
		while entry3 == 1 and entry4 == 1:
			time.sleep(0.5)
			print()
			while entry3 == 1:
				try:
					inputDate2 = input("Enter End date in format(MM-DD-YYYY): ")
					month2, day2, year2 = map(int, inputDate2.split('-'))
					entry3 = 0
				except:
					print("Wrong date format")

			while entry4 == 1:
				try:			
					inputTime2 = input("Enter End Time(HH:MM): ")
					hour2, minute2 = map(int, inputTime2.split(':'))
					entry4 = 0
				except:
					print("Wrong time format")	
			
		endDateTime = datetime.datetime(year2,month2,day2,hour2,minute2,0,0)

		cf = commonfunctions('RESERVATIONS.csv')
		allReservations = cf.csvToListOfRow()
		
		inRangeReserve = []
		
		for i in range(1,len(allReservations)):
			timeBooked = int(allReservations[i][9])
			bookedStartDateTime = datetime.datetime.strptime(allReservations[i][10],"%Y-%m-%d %H:%M:%S")
			bookedEndDateTime = datetime.datetime.strptime(allReservations[i][10],"%Y-%m-%d %H:%M:%S") + datetime.timedelta(minutes=timeBooked)
			active = allReservations[i][11]
			bookedServeID = allReservations[i][5]
			#print("bookedStartDateTime :",bookedStartDateTime,"++","bookedEndDateTime :",bookedEndDateTime,"++","startDateTime :",startDateTime,"++","endDateTime :",endDateTime,"++")
			if startDateTime <= bookedStartDateTime and endDateTime >= bookedEndDateTime and active == 'Y' and bookedServeID not in ('1','2') and bookedServeID == serviceId:
				inRangeReserve.append(str(bookedStartDateTime))
				inRangeReserve.append(str(bookedEndDateTime))

		if len(inRangeReserve) == 0:
		
			print()
			time.sleep(0.5)
			print("All time slots are available")
					
		else:
		
			inRangeReserve = list(set(inRangeReserve))
			inRangeReserve.sort()
			
			inRangeReserve = cf.groupByDate(inRangeReserve)
			dateRange = cf.makeListOfDates(startDateTime,endDateTime)
			
			print()
			time.sleep(0.5)
			print("Available time slots are:")
			print()
			time.sleep(0.5)
			cf.printDates(dateRange,inRangeReserve,startDateTime,endDateTime)			
			
		#return inRangeReserve
				

	def availTimeCust(self):
		"""
			display of available time slots for the customer 
			between the current moment and the customer’s checkout
		"""	
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
		
		startDateTime = datetime.datetime.now()
		endDateTime = datetime.datetime.strptime(custInfo[1][4] + " 08:00:00","%m/%d/%Y %H:%M:%S")
		
		cf = commonfunctions('RESERVATIONS.csv')
		allReservations = cf.csvToListOfRow()
		
		inRangeReserve = []
		
		custInfo[0].append('Active')
		custInfo[1].append('Y')
		custReservations = cf.returnListFromMainList(allReservations,custInfo)
		
		for i in range(1,len(custReservations)):
			timeBooked = int(custReservations[i][9])
			bookedStartDateTime = datetime.datetime.strptime(custReservations[i][10],"%Y-%m-%d %H:%M:%S")
			bookedEndDateTime = datetime.datetime.strptime(custReservations[i][10],"%Y-%m-%d %H:%M:%S") + datetime.timedelta(minutes=timeBooked)
			active = custReservations[i][11]
			bookedCustID = custReservations[i][0]
			#print("bookedStartDateTime :",bookedStartDateTime,"++","bookedEndDateTime :",bookedEndDateTime,"++","startDateTime :",startDateTime,"++","endDateTime :",endDateTime,"++")
			if startDateTime <= bookedStartDateTime and endDateTime >= bookedEndDateTime:
				inRangeReserve.append(str(bookedStartDateTime))
				inRangeReserve.append(str(bookedEndDateTime))
		
		if len(inRangeReserve) == 0:
		
			print()
			time.sleep(0.5)
			print("All time slots are available")
					
		else:
		
			inRangeReserve = list(set(inRangeReserve))
			inRangeReserve.sort()
			
			inRangeReserve = cf.groupByDate(inRangeReserve)
			dateRange = cf.makeListOfDates(startDateTime,endDateTime)
			
			print()
			time.sleep(0.5)
			print("Available time slots are:")
			print()
			time.sleep(0.5)
			cf.printDates(dateRange,inRangeReserve,startDateTime,endDateTime)
										
		#return inRangeReserve
		
		
		