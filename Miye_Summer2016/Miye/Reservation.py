import csv
import time
import pandas as pd
import datetime
import copy

class Menues :
    def __init__(self):
        print( )
        time.sleep(0.1)
        print( "(1) Customer Information" )
        time.sleep(0.1)
        print( "(2) Register Services" )
        time.sleep(0.1)
        print( "(3) Quit!" )
        time.sleep(0.1)

class Customer(Menues):
    pass
    def getGuestInfo(self):
        """         read from csv and print customer information    """
        time.sleep(0.5)
        print()
        GuestID = input( "Enter Guest ID: " )
        GuestInfo = self.csvGetCustInfo('CUSTOMERS.csv',GuestID)
        print()
        for i in range(1,len(GuestInfo)):
            for j in range(0,len(GuestInfo[0])-1):
                time.sleep(0.5)
                print(GuestInfo[0][j],":",GuestInfo[i][j+1])
        return GuestInfo
    def csvGetCustInfo(self,filename,guestID):
        data = []
        newdata = []
        """ 
        Converts the data from '.csv' file to list 
        where row is presented as a list
        """
     
        with open(filename, "rt", encoding='ascii') as csvfile:
            csvreader = csv.reader('CUSTOMERS.csv', delimiter=',', quotechar='|')
            data = list(csvreader)
            newdata = [data[0]]
            for i in range(0,len(data)):
                if data[i][0] == str():
                    newdata.extend([data[i]])
                    break
        return newdata
#class Servicese:
    
    
#class reservation(Customer,Servicese):
    
    
    
#class Bills(reservation):
    
    
#class Cancleation(Customer,Servicese):


def main():
    menue=Customer()
    menue.getGuestInfo()
 
 
    
    
    
    
main()
