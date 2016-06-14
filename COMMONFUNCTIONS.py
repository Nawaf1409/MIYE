import csv
import pandas as pd
import copy
import datetime
from operator import itemgetter

class commonfunctions(object):

	def __init__(self,filename):
		self.filename = filename

	def csvToListOfRow(self):
		""" 
			Converts the data fron '.csv' file to list 
			where row is presented as a list
		"""
		data = []
		with open(self.filename, "rt", encoding='ascii') as csvfile:
			csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
			data = list(csvreader)
		return data

	def convertListToDf(self,inputList):
		"""
			Converts an list object to a DataFrame
		"""
		newInputList = inputList[:]
		header = newInputList[0]
		newInputList.remove(header)
		inputList_df = pd.DataFrame(newInputList,columns = header)
		return inputList_df

	def returnListFromMainList(self,mainList,smallList):
		"""
			returns mainList rows which
			matches smallList
		"""
		newMainList = copy.deepcopy(mainList)
		newSmallList = copy.deepcopy(smallList)
		mainHeader = copy.deepcopy(newMainList[0:1])
		smallHeader = copy.deepcopy(newSmallList[0:1])
		newMainList.remove(newMainList[0])
		newSmallList.remove(newSmallList[0])
		
		newMainList = sorted(newMainList, key=itemgetter(0))
		newSmallList = sorted(newSmallList, key=itemgetter(0))
		returnList = []
		columns = []

		for i in range(0,len(smallHeader[0])):
			for j in range(0,len(mainHeader[0])):
				if smallHeader[0][i] == mainHeader[0][j]:
					columns.append(j)
	
		returnList = copy.deepcopy(mainHeader[0:1])
		matchFlag = True
		count = 0
		for j in range(1,len(mainList)):
			for i in range(1,len(smallList)):
				matchFlag = True
				for k in range(0,len(smallList[0])):
					if matchFlag == False:
						break
					count = 0
					for l in columns:
						if matchFlag == False:
							break
						count = count + 1
						if smallList[i][k] == mainList[j][l] and matchFlag:
							matchFlag = True
							#print("if smallList["+ str(i) +"]["+ str(k) +"] :",smallList[i][k])
							#print("if mainList["+ str(j) +"]["+ str(l) +"] :",mainList[j][l])
							#print("if matchFlag :",matchFlag)
							#print("if count :",str(count))	
							if k < len(smallList[0]) - 1:
								k = k + 1
						else:
							matchFlag = False
							#print("else smallList["+ str(i) +"]["+ str(k) +"] :",smallList[i][k])
							#print("else mainList["+ str(j) +"]["+ str(l) +"] :",mainList[j][l])
							#print("else matchFlag :",matchFlag)
							#print("else count :",str(count))							
							break
						if matchFlag and count == len(columns):
							returnList.append(mainList[j])
		
		return returnList

	def checkServiceID(self,serviceID):
		cf = commonfunctions('SERVICES.csv')
		allService = cf.csvToListOfRow()
		for i in range(1,len(allService)):
			if serviceID == allService[i][0]:
				return True
		return False


	def groupByDate(self,inputList):

		presentDateTime = datetime.datetime.strptime(inputList[0],"%Y-%m-%d %H:%M:%S")
		previousDateTime = datetime.datetime.strptime(inputList[0],"%Y-%m-%d %H:%M:%S")
		returnList = [[presentDateTime.strftime("%Y-%m-%d %H:%M:%S")]]
		count = 0

		for i in range(1,len(inputList)):
			presentDateTime = datetime.datetime.strptime(inputList[i],"%Y-%m-%d %H:%M:%S")
			if presentDateTime.strftime("%Y-%m-%d") == previousDateTime.strftime("%Y-%m-%d"):
				returnList[count].append(presentDateTime.strftime("%Y-%m-%d %H:%M:%S"))
				previousDateTime = presentDateTime
			else:
				count = count + 1
				returnList.append([presentDateTime.strftime("%Y-%m-%d %H:%M:%S")])
				previousDateTime = presentDateTime
		
		return returnList

	def makeListOfDates(self,startDateTime,endDateTime):
	
		presentDate = startDateTime
		returnList = []
		while presentDate.strftime("%Y-%m-%d") != endDateTime.strftime("%Y-%m-%d"):
			returnList.append(presentDate.strftime("%Y-%m-%d"))
			presentDate = presentDate + datetime.timedelta(days=1)
		returnList.append(presentDate.strftime("%Y-%m-%d"))
		return returnList
		
	def printDates(self,inputList1,inputList2,startDateTime,endDateTime):
		
		l = 0
		m = 0
		n = 0
		startDateTimeBKP = startDateTime
		printDate = 'L'
		for i in range(0,len(inputList1)):
			print(inputList1[i])
			m = m + 1
			for j in range(l,len(inputList2)):
				presentDateTime = datetime.datetime.strptime(inputList2[j][0],"%Y-%m-%d %H:%M:%S")
				if inputList1[i] == presentDateTime.strftime("%Y-%m-%d"):
					startDateTime = startDateTimeBKP
					n = 1
					for k in range(0,len(inputList2[j])):
						presentDateTime = datetime.datetime.strptime(inputList2[j][k],"%Y-%m-%d %H:%M:%S")						
						#print("inputList1[0] :",inputList1[0])
						#print("presentDateTime :",presentDateTime.strftime("%Y-%m-%d %H:%M:%S"))
						#print("startDateTime :",startDateTime.strftime("%Y-%m-%d %H:%M:%S"))
						if startDateTime == presentDateTime and k == 0:
							printDate = 'L'	
						elif startDateTime < presentDateTime and k == 0:	
							varPresentDateTime = presentDateTime - datetime.timedelta(minutes=1)
							print("    ",startDateTime.strftime("%H:%M:%S"),'to',varPresentDateTime.strftime("%H:%M:%S"))
							printDate = 'L'	
						elif k == len(inputList2[j]) - 1:
							if printDate == 'L':								
								varPresentDateTime = presentDateTime + datetime.timedelta(minutes=1)
								varEndDateTimeStr = presentDateTime.strftime("%Y-%m-%d") + " 20:00:00"
								varEndDateTime = datetime.datetime.strptime(varEndDateTimeStr,"%Y-%m-%d %H:%M:%S")
								if varPresentDateTime <= varEndDateTime:
									if endDateTime >= varEndDateTime:
										print("    ",varPresentDateTime.strftime("%H:%M:%S"),'to 20:00:00')	
									else:
										print("    ",varPresentDateTime.strftime("%H:%M:%S"),'to',endDateTime.strftime("%H:%M:%S"))	
								printDate = 'L'	
								startDateTime = startDateTime + datetime.timedelta(days=1)
								startDateTime = datetime.datetime.strptime(startDateTime.strftime("%Y-%m-%d") + " 08:00:00", "%Y-%m-%d %H:%M:%S")
								l = l+1
								m = 1
						elif k > 0 and printDate == 'R':
							varPresentDateTime = presentDateTime - datetime.timedelta(minutes=1)
							print(varPresentDateTime.strftime("%H:%M:%S"))
							printDate = 'L'
						elif k > 0 and printDate == 'L':
							varPresentDateTime = presentDateTime + datetime.timedelta(minutes=1)
							print("    ",varPresentDateTime.strftime("%H:%M:%S"),'to',end = " ")
							printDate = 'R'
				elif m == 0:
					printDate = 'L'	
					startDateTime = startDateTime + datetime.timedelta(days=1)
					startDateTime = datetime.datetime.strptime(startDateTime.strftime("%Y-%m-%d") + " 08:00:00", "%Y-%m-%d %H:%M:%S")
					m = m + 1
				elif startDateTimeBKP.strftime("%Y-%m-%d") < presentDateTime.strftime("%Y-%m-%d") and n == 0:
					print("    ",startDateTimeBKP.strftime("%H:%M:%S"),"to 20:00:00")
					startDateTimeBKP = startDateTimeBKP + datetime.timedelta(days=1)
					startDateTimeBKP = datetime.datetime.strptime(startDateTimeBKP.strftime("%Y-%m-%d") + " 08:00:00", "%Y-%m-%d %H:%M:%S")	
					break				
			
			#print("l:",l)
			#print("m:",m)
			if l == len(inputList2) and m != 1 and i == len(inputList1) - 1:
				varEndDateTimeStr = endDateTime.strftime("%Y-%m-%d") + " 20:00:00"
				varEndDateTime = datetime.datetime.strptime(varEndDateTimeStr,"%Y-%m-%d %H:%M:%S")
				if endDateTime < varEndDateTime:
					print("     08:00:00 to",endDateTime.strftime("%H:%M:%S"))	
				else:
					print("     08:00:00 to 20:00:00")
				startDateTime = startDateTime + datetime.timedelta(days=1)
				startDateTime = datetime.datetime.strptime(startDateTime.strftime("%Y-%m-%d") + " 08:00:00", "%Y-%m-%d %H:%M:%S")					
			elif j == len(inputList2) - 1 and m != 1:
				print("     08:00:00 to 20:00:00")
				startDateTime = startDateTime + datetime.timedelta(days=1)
				startDateTime = datetime.datetime.strptime(startDateTime.strftime("%Y-%m-%d") + " 08:00:00", "%Y-%m-%d %H:%M:%S")					
				

