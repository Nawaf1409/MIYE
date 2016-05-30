import csv
import time
import pandas as pd
import datetime
import copy
	
def convertListToDf(inputList):
	"""
		Converts an list object to a DataFrame
	"""
	newInputList = inputList[:]
	header = newInputList[0]
	newInputList.remove(header)
	inputList_df = pd.DataFrame(newInputList,columns = header)
	return inputList_df

def csvGetCustInfo(filename,custID):
	""" 
		Converts the data from '.csv' file to list 
		where row is presented as a list
	"""
	data = []
	newdata = []
	with open(filename, "rt", encoding='ascii') as csvfile:
		csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
		data = list(csvreader)
		newdata = [data[0]]
		for i in range(0,len(data)):
			if data[i][0] == str(custID):
				newdata.extend([data[i]])
				break
	return newdata

def getCustInfo():
	""" 
		read from csv and print Guest information
	"""
	time.sleep(0.5)
	print()
	custID = input( "Enter Guest ID: " )
	custInfo = csvGetCustInfo('CUSTOMERS.csv',custID)
	print()
	for i in range(1,len(custInfo)):
		for j in range(0,len(custInfo[0])):
			time.sleep(0.5)
			print(custInfo[0][j],":",custInfo[i][j])
	return custInfo

def csvToListOfRow(filename):
	""" 
		Converts the data fron '.csv' file to list 
		where row is presented as a list
	"""
	data = []
	with open(filename, "rt", encoding='ascii') as csvfile:
		csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
		data = list(csvreader)
	return data
	
def printServices():
	time.sleep(0.5)
	allService = csvToListOfRow('SERVICES.csv')
	allService_DF = convertListToDf(allService)
	allService_DF = allService_DF.set_index('Service ID')
	print(allService_DF)
	
def setServices():
	"""
		this function selects a service for a
		particular Guest
	"""
	custID = input( "Enter Guest ID? " )
	custInfo = csvGetCustInfo('CUSTOMERS.csv',custID)
	time.sleep(0.5)
	print()
	print("The service will be booked for :",custInfo[1][1],custInfo[1][2])
	allService = csvToListOfRow('SERVICES.csv')
	chosenService_LIST = copy.deepcopy(allService[0:1])
	chosenService_LIST[0].extend(['Registered DateTime'])
	allService_DF = convertListToDf(allService)
	allService_DF = allService_DF.set_index('Service ID')
	continueServiceSel = 'Y'
	oldReservations = csvToListOfRow('RESERVATIONS.csv')
	reservation = copy.deepcopy(oldReservations[:])
	
	while continueServiceSel == 'Y':

		time.sleep(0.5)
		print()
		print(allService_DF)
		time.sleep(0.5)
		print()
		chosenService = input("Enter Service ID : ")
		print()
		
		inputDate = input("Ener date in format(MM-DD-YYYY): ")
		month, day, year = map(int, inputDate.split('-'))

		inputTime = input("Enter Time(HH:MM): ")
		hour, minute = map(int, inputTime.split(':'))
		registeredStartTime = datetime.datetime(year,month,day,hour,minute,0,0)

		for i in range(1,len(allService)):
			if allService[i][0] == chosenService:
				if isServiceAvailable(allService[i],oldReservations,registeredStartTime) and isCustAvailable(custInfo,oldReservations,registeredStartTime) and inTimeSlot(allService[i],registeredStartTime):
					chosenService_LIST.append(allService[i])
					chosenService_LIST[len(chosenService_LIST)-1].extend([registeredStartTime])
					print()
					for j in range(0,len(chosenService_LIST[0])):	
						time.sleep(0.5)					
						print(chosenService_LIST[0][j],":",chosenService_LIST[len(chosenService_LIST)-1][j])
					print("Service price :",float(chosenService_LIST[len(chosenService_LIST)-1][3]) * int(chosenService_LIST[len(chosenService_LIST)-1][4]),"$")
				else:
					print("Out of Working Hours")
		time.sleep(0.5)
		print()
		continueServiceSel = input("Do you want to add some more Services? (Y/N) : ")
		
	chosenService_DF = convertListToDf(chosenService_LIST)
	chosenService_DF = chosenService_DF.set_index('Service ID')
	time.sleep(0.5)
	print()
	if len(chosenService_LIST) == 1:
		print("No services were registered")
	else:
		print("The following services are registered")
		print(chosenService_DF)

	presentReservation = makeReservation(custInfo,chosenService_LIST)

	if len(oldReservations) >  1:
		reservation.extend(presentReservation[1:])
	else:
		reservation = presentReservation

	reservation_DF = convertListToDf(reservation)
	reservation_DF.to_csv('RESERVATIONS.csv',index=False)
	return chosenService_LIST
 
def makeReservation(custInfo,chosenService_LIST):
	reservation = [custInfo[0] + chosenService_LIST[0]]
	for i in range(1,len(custInfo)):
		for j in range(1,len(chosenService_LIST)):
			reservation.append(custInfo[i] + chosenService_LIST[j])
	return reservation
	
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
	custInfo = csvGetCustInfo('CUSTOMERS.csv',custID)
	reservations = csvToListOfRow('RESERVATIONS.csv')
	print("Guest Name :",custInfo[1][1],custInfo[1][2])
	billFor = copy.deepcopy([[reservations[0][6],reservations[0][7],'Date','Time','Cost']])
	totalCost = 0
	for i in range(1,len(reservations)):
		if reservations[i][0] == custInfo[1][0]:
			timeBooked = int(reservations[i][9])
			startTime = datetime.datetime.strptime(reservations[i][10],"%Y-%m-%d %H:%M:%S")
			endTime = datetime.datetime.strptime(reservations[i][10],"%Y-%m-%d %H:%M:%S") + datetime.timedelta(minutes=timeBooked)
			cost = float(reservations[i][8]) * float(reservations[i][9])
			billFor.extend(copy.deepcopy([[reservations[i][6],reservations[i][7],str(startTime.date()),str(startTime.time()) + ' - ' + str(endTime.time()),cost]]))
			totalCost = totalCost + cost
	billFor.extend(copy.deepcopy([['-------------','-------------------','-----------','--------------------','----']]))
	billFor.extend(copy.deepcopy([['Total Bill : ','','','',totalCost]]))
	billFor_DF = convertListToDf(billFor)
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
	print( "(2) Make a Reservation" )
	time.sleep(0.1)
	print( "(3) Print Bill" )
	time.sleep(0.1)
	print( "(4) Quit!" )
	time.sleep(0.1)
	
def main():
	
	custInfo = []
	chosenService_LIST = []

	""" the main user-interaction loop """
	while True:
		print("****************************************************")
		allOptions()
		print()
		print("****************************************************")
		time.sleep(0.5)
		try:			
			yourChoice = input("Choose an option : ")
			yourChoice = int(yourChoice)
		except:
			yourChoice  = 10000		
		
		if yourChoice in [1,2,3,4]:

			if yourChoice == 1:
				custInfo = getCustInfo()
				print()
				
			if yourChoice == 2:
				if custInfo == []:
					printServices()
				else:
					chosenService_LIST = setServices()
				print()
				
			if yourChoice == 3:
				makeBill()
				print()
				
			if yourChoice == 4:
				print()
				print("****************************************************")
				break				
			
		else:
			print()
			time.sleep(0.5)
			print("Enter a number between 0 to 4")
			
	print()
	time.sleep(0.5)
	print("****Thank you for using our application****")

main()


