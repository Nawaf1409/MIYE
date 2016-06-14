import csv
import time
import pandas as pd
import datetime
import copy
from CUSTOMERS import *
from SERVICES import *
from COMMONFUNCTIONS import *
from RESERVATIONS import *

def convertListToDf1(inputList):
	"""
		Converts an list object to a DataFrame
	"""
	newInputList = inputList[:]
	header = newInputList[0]
	newInputList.remove(header)
	inputList_df = pd.DataFrame(newInputList,columns = header)
	return inputList_df

def getCustInfo():
	""" 
		read from csv and print Guest information
	"""
	entry = 1
	
	while entry == 1:
		time.sleep(0.5)
		print()
		try:			
			custID = input( "Enter Guest ID: " )
			custID = int(custID)
		except:
			custID  = 9999999
		print()
		presentDate = datetime.datetime.now().date()
		if custID not in [9999999]:
			cust = customers('CUSTOMERS.csv')
			custInfo =  cust.csvGetCustInfo(custID)		
			for i in range(1,len(custInfo)):
				checkInDate = datetime.datetime.strptime(custInfo[i][3] ,"%m/%d/%Y").date()
				if checkInDate > presentDate:
					time.sleep(0.5)
					print("Check in date  is of :",checkInDate.strftime('%m-%d-%Y'),"which is above Present Date :",presentDate.strftime('%m-%d-%Y'))
					time.sleep(0.5)
					custInfo = []
					break
				else:
					for j in range(0,len(custInfo[0])):
						time.sleep(0.5)
						print(custInfo[0][j],":",custInfo[i][j])
			entry = 2
			if len(custInfo) == 1:
				print("The entered Guest ID is not registered")
		else:
			time.sleep(0.5)
			print("Please enter a number")

	return custInfo
	
def setServices():
	"""
		this function selects a service for a
		particular Guest
	"""
	entryCust = 1
	
	while entryCust == 1:
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
				entryCust = 2
		else:
			time.sleep(0.5)
			print("Please enter a number")
	
	time.sleep(0.5)
	print()
	print("The service will be booked for :",custInfo[1][1],custInfo[1][2])
	cf1 = commonfunctions('SERVICES.csv')
	allService = cf1.csvToListOfRow()
	chosenService_LIST_bkp = []
	chosenService_LIST = copy.deepcopy(allService[0:1])
	chosenService_LIST[0].extend(['Registered DateTime'])
	allService_DF = convertListToDf1(allService)
	allService_DF = allService_DF.set_index('Service ID')
	continueServiceSel = 'Y'
	cf2 = commonfunctions('RESERVATIONS.csv')
	oldReservations = cf2.csvToListOfRow()
	reservation = copy.deepcopy(oldReservations[:])
	
	while continueServiceSel == 'Y':

		cf3 = commonfunctions('RESERVATIONS.csv')
		oldReservations = cf3.csvToListOfRow()
		chosenService_LIST = copy.deepcopy(allService[0:1])
		chosenService_LIST[0].extend(['Registered DateTime'])
		chosenService_LIST[0].extend(['Active'])
		reservation = copy.deepcopy(oldReservations[:])
		time.sleep(0.5)
		print()
		print(allService_DF)
		time.sleep(0.5)
		print()
		chosenService = input("Enter Service ID : ")
		entry1 = 1
		entry2 = 1
		entry3 = 1
		month = 0
		day = 0
		year = 0
		hour = 0
		minute = 0
		
		while entry1 == 1:
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
			
			registeredStartTime = datetime.datetime(year,month,day,hour,minute,0,0)
			
			if isDateTimeInRange(custInfo,registeredStartTime):
				entry1 = 0
			else:
				entry2 = 1
				entry3 = 1

		for i in range(1,len(allService)):
			if allService[i][0] == chosenService:
				if inTimeSlot(allService[i],registeredStartTime) or allService[i][0] in ('1','2'):
					if isCustAvailable(custInfo,oldReservations,registeredStartTime):
						if isServiceAvailable(allService[i],oldReservations,registeredStartTime) or allService[i][0] in ('1','2'):
							chosenService_LIST.append(allService[i])
							chosenService_LIST[len(chosenService_LIST)-1].extend([registeredStartTime])
							chosenService_LIST[len(chosenService_LIST)-1].extend(['Y'])
							print()
							for j in range(0,len(chosenService_LIST[0])-1):	
								time.sleep(0.5)	
								if j == len(chosenService_LIST[0])-2:
									print(chosenService_LIST[0][j],":",registeredStartTime.strftime('%m-%d-%Y %H:%M'))
								else:
									print(chosenService_LIST[0][j],":",chosenService_LIST[len(chosenService_LIST)-1][j])
							print("Service price :",float(chosenService_LIST[len(chosenService_LIST)-1][3]) * int(chosenService_LIST[len(chosenService_LIST)-1][4]),"$")
							makeReservation(custInfo,chosenService_LIST,oldReservations,reservation)
						else:
							print("This Time Slot is full")
					else:
						print("You already have another service at the same time")
				else:
					print("Out of Working Hours")
		chosenService_LIST_bkp.extend(copy.deepcopy(chosenService_LIST[:]))
		time.sleep(0.5)
		print()
		continueServiceSel = input("Do you want to add some more Services? (Y/N) : ")

	chosenService_DF = convertListToDf1(chosenService_LIST)
	chosenService_DF = chosenService_DF.set_index('Service ID')
		
	chosenService_DF_bkp = convertListToDf1(chosenService_LIST_bkp)
	chosenService_DF_bkp = chosenService_DF_bkp.set_index('Service ID')
	
	if len(chosenService_LIST_bkp) == 1:
		time.sleep(0.5)
		print()
		print("No services were registered")
	#else:
	#	print("The following services are registered")
	#	print(chosenService_DF_bkp)

def combinedReservation(custInfo,chosenService_LIST):
	reservation = [custInfo[0] + chosenService_LIST[0]]
	for i in range(1,len(custInfo)):
		for j in range(1,len(chosenService_LIST)):
			reservation.append(custInfo[i] + chosenService_LIST[j])
	return reservation

def makeReservation(custInfo,chosenService_LIST,oldReservations,reservation):
	presentReservation = combinedReservation(custInfo,chosenService_LIST)

	if len(oldReservations) >  1:
		reservation.extend(presentReservation[1:])
	else:
		reservation = presentReservation

	reservation_DF = convertListToDf1(reservation)
	reservation_DF.to_csv('RESERVATIONS.csv',index=False)

def isDateTimeInRange(custInfo,registeredStartTime):
	checkOutDate = datetime.datetime.strptime(custInfo[1][4],"%m/%d/%Y")
	if registeredStartTime.date() <= checkOutDate.date():
		if registeredStartTime >= datetime.datetime.now():
			return True
		else:
			time.sleep(0.5)
			print()			
			print("Can't book the time slot is expired")
			return False
	else:
		time.sleep(0.5)
		print()
		print("Can't book because the registered date is above Check Out Date")
		return False
	
def isServiceAvailable(choosenService,oldReservations,registeredStartTime):
	for i in range(1,len(oldReservations)):
		if oldReservations[i][5] == choosenService[0]:
			if checkDateAvailable(oldReservations[i],registeredStartTime) == True:
				continue
			else:
				return False
	return True
	
def isCustAvailable(custInfo,oldReservations,registeredStartTime):
	for i in range(1,len(oldReservations)):
		if oldReservations[i][0] == custInfo[1][0]:
			if checkDateAvailable(oldReservations[i],registeredStartTime) == True:
				continue
			else:
				return False
	return True

def inTimeSlot(choosenService,registeredStartTime):
	timeBooked = int(choosenService[4])
	spaStartTime = datetime.datetime.strptime('08:00:00', "%H:%M:%S")
	spaEndTime = datetime.datetime.strptime('20:00:00', "%H:%M:%S")
	registeredEndTime = registeredStartTime + datetime.timedelta(minutes=timeBooked)
	#print("spaStartTime :",spaStartTime)
	#print("spaEndTime :",spaEndTime)
	#print("registeredStartTime :",registeredStartTime)
	#print("registeredEndTime :",registeredEndTime)
	if (spaStartTime.time() <= registeredStartTime.time() and registeredStartTime.time() <= spaEndTime.time()) and (spaStartTime.time() <= registeredEndTime.time() and registeredEndTime.time() <= spaEndTime.time()):
		return True
	else:
		return False

def makeBill():
	custID = input( "Enter Guest ID? " )
	cust = customers('CUSTOMERS.csv')
	custInfo =  cust.csvGetCustInfo(custID)
	cf = commonfunctions('RESERVATIONS.csv')
	reservations = cf.csvToListOfRow()
	print("Guest Name :",custInfo[1][1],custInfo[1][2])
	billFor = copy.deepcopy([[reservations[0][6],reservations[0][7],'Date','Time','Cost']])
	totalCost = 0
	for i in range(1,len(reservations)):
		if reservations[i][0] == custInfo[1][0] and reservations[i][11] == 'Y':
			timeBooked = int(reservations[i][9])
			startTime = datetime.datetime.strptime(reservations[i][10],"%Y-%m-%d %H:%M:%S")
			endTime = datetime.datetime.strptime(reservations[i][10],"%Y-%m-%d %H:%M:%S") + datetime.timedelta(minutes=timeBooked)
			cost = float(reservations[i][8]) * float(reservations[i][9])
			billFor.extend(copy.deepcopy([[reservations[i][6],reservations[i][7],str(startTime.date()),str(startTime.time()) + ' - ' + str(endTime.time()),cost]]))
			totalCost = totalCost + cost
	billFor.extend(copy.deepcopy([['------------','------------------','----------','-------------------','----']]))
	billFor.extend(copy.deepcopy([['Total Bill : ','','','',totalCost]]))
	billFor_DF = convertListToDf1(billFor)
	print()
	print("****************************************************")
	print(billFor_DF)
	
def checkDateAvailable(oldReservations,registeredStartTime):
	timeBooked = int(oldReservations[9])
	oldReservationsStartTime = datetime.datetime.strptime(oldReservations[10], "%Y-%m-%d %H:%M:%S")
	oldReservationsEndTime = oldReservationsStartTime + datetime.timedelta(minutes=timeBooked)
	registeredEndTime = registeredStartTime + datetime.timedelta(minutes=timeBooked)
	#print("oldReservationsStartTime :",oldReservationsStartTime)
	#print("oldReservationsEndTime :",oldReservationsEndTime)
	#print("registeredStartTime :",registeredStartTime)
	#print("registeredEndTime :",registeredEndTime)
	if registeredStartTime.date() == oldReservationsStartTime.date():
	#checking whether their is any same value as the registered date
		if (oldReservationsStartTime <= registeredStartTime and registeredStartTime <= oldReservationsEndTime) or (oldReservationsStartTime <= registeredEndTime and registeredEndTime <= oldReservationsEndTime):
			return False
	return True

def allOptions():
	""" a function that simply prints the all Options """
	print( )
	time.sleep(0.1)
	print( "(1) Guest Information" )
	time.sleep(0.1)
	print( "(2) Lookup Services" )
	time.sleep(0.1)
	print( "(3) Make a Reservation" )
	time.sleep(0.1)
	print( "(4) Cancel a Reservation" )
	time.sleep(0.1)
	print( "(5) Print Bill" )
	time.sleep(0.1)
	print( "(6) Quit!" )
	time.sleep(0.1)
	
def main_services():
	""" the showing up all services with different parameters loop """
	while True:
		time.sleep(0.5)
		print("")
		print("****************************************************")
		print( )
		time.sleep(0.1)
		print( "(1) All services" )
		time.sleep(0.1)
		print( "(2) All available services at a given day & time" )
		time.sleep(0.1)
		print( "(3) Available times for a particular service" )
		time.sleep(0.1)
		print( "(4) Available time slots till the customer's checkout" )
		time.sleep(0.1)		
		print( "(5) Quit!" )
		print("")
		print("****************************************************")
		print("")
		try:			
			yourChoice = input("Choose an option : ")
			yourChoice = int(yourChoice)
		except:
			yourChoice  = 10000	

		if yourChoice in [1,2,3,4,5]:

			if yourChoice == 1:
				serve = services('SERVICES.csv')
				print()
				serve.printServices()
				
			if yourChoice == 2:
				serve = services('SERVICES.csv')
				serve.availService()				
	
			if yourChoice == 3:
				serve = services('SERVICES.csv')
				serve.availTimeService()
				
			if yourChoice == 4:
				serve = services('SERVICES.csv')
				serve.availTimeCust()
				
			if yourChoice == 5:
				break					
	
		else:
			print()
			time.sleep(0.5)
			print("Enter a number between 1 to 5")	
			
	print()
	time.sleep(0.5)
	print("Main Menu of Clerk")
	
def main_manager():
	""" the main manager-interaction loop """
	while True:
		time.sleep(0.5)
		print("")
		print("****************************************************")
		print( )
		time.sleep(0.1)
		print( "(1) Add Service" )
		time.sleep(0.1)		
		print( "(2) Quit!" )
		print("")
		print("****************************************************")
		print("")
		try:			
			yourChoice = input("Choose an option : ")
			yourChoice = int(yourChoice)
		except:
			yourChoice  = 10000	

		if yourChoice in [1,2]:

			if yourChoice == 1:
				serve = services('SERVICES.csv')
				serve.addService()

			if yourChoice == 2:
				break					
	
		else:
			print()
			time.sleep(0.5)
			print("Enter a number between 1 to 2")	
			
	print()
	time.sleep(0.5)
	print("Manager account logged out")	
			
def main_clerk():
	
	custInfo = []
	chosenService_LIST = []

	""" the main clerk-interaction loop """
	while True:
		print("")
		print("****************************************************")
		allOptions()
		print()
		print("****************************************************")
		time.sleep(0.5)
		print("")
		try:			
			yourChoice = input("Choose an option : ")
			yourChoice = int(yourChoice)
		except:
			yourChoice  = 10000		
		
		if yourChoice in [1,2,3,4,5,6]:

			if yourChoice == 1:
				custInfo = getCustInfo()
				print()
				
			if yourChoice == 2:
				main_services()
				print()
				
			if yourChoice == 3:
				setServices()
				print()
				
			if yourChoice == 4:
				cR = reservations('RESERVATIONS.csv')
				cR.cancelReservation()
				print()
				
			if yourChoice == 5:
				makeBill()
				print()

			if yourChoice == 6:
				break					
			
		else:
			print()
			time.sleep(0.5)
			print("Enter a number between 1 to 6")
			
	print()
	time.sleep(0.5)
	print("Clerk account logged out")	

def main():
	""" the main interaction loop """

	while True:
		time.sleep(0.5)
		print("")
		print("****************************************************")
		print( )
		time.sleep(0.1)
		print( "(1) Manager" )
		time.sleep(0.1)
		print( "(2) Clerk" )	
		time.sleep(0.1)
		print( "(3) Quit!" )		
		print("")
		print("****************************************************")
		print("")
		try:			
			yourChoice = input("Choose an option : ")
			yourChoice = int(yourChoice)
		except:
			yourChoice  = 10000	

		if yourChoice in [1,2,3]:

			if yourChoice == 1:
				main_manager()

			if yourChoice == 2:
				main_clerk()
				
			if yourChoice == 3:
				print()
				print("****************************************************")
				break

		else:
			print()
			time.sleep(0.5)
			print("Enter a number between 1 to 3")
	
	print()
	time.sleep(0.5)
	print("****Thank you for using our application****")
	
#cR = reservations('RESERVATIONS.csv')
#cR.markActivityAsN()
main()


