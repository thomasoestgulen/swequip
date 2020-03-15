#!/usr/bin/env python

import os
import time
import datetime
import MySQLdb
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

import parameters as p


global c
global db

def DTstring():
    t = datetime.datetime.fromtimestamp(time.time())
    strTime = t.strftime("%H:%M:%S")
    strDate = t.strftime("%Y-%m-%d")
    DT = strDate + ' ' + strTime
    return DT


def getRFID():
    print('Hold kortet mot leseren...')
    reader = SimpleMFRC522()
    try:
        RFID, text = reader.read()
     
    finally: 
        GPIO.cleanup()
        
    return(RFID)


def getEmployee():
    rfid = getRFID()
    sql = "SELECT employee.* FROM employee, card WHERE employee.ID = card.empID AND card.RFID = '{}'".format(rfid)
    try:
        c.execute(sql)     
        result = c.fetchall()
        if result is not None:
             print ('Navn: ' , result[0][1], result[0][2], '| Sign: ' , result[0][3], ' | e-mail: ' , result[0][4])
             return result[0][0]
    except:
        print ("read error")
    

def getEquipment():
    rfid = getRFID()
    sql = "SELECT * FROM equipment WHERE RFID = '{}'".format(rfid)
    try:
        c.execute(sql)     
        result = c.fetchall()
        if result is not None:
             #print ('Merke: ' , result[0][2], '| Type: ' , result[0][3], ' | Kommentar: ' , result[0][4], ' | NyDato: ' , result[0][5])
             return result[0][0]
    except:
        print ("read error")
    

def checkOut():
    '''
    Register an equipment checkout
    '''
    # Loans table: (empID, equipID, checkOutDT) VALUES ('1', '3', '2019-11-12 20-39-58')
    print('Hvem er du?')
    empID = getEmployee()
    time.sleep(2)
    print('Hva vil du laane?')
    equipID = getEquipment()

    sql = "INSERT INTO Loans (empID, equipID, checkOutDT) VALUES ({},{},'{}')".format(empID, equipID, DTstring())

    try:
        c.execute(sql)
        db.commit()
        print('Registrert i databasen!')
        #print('Lever den tilbake i god stand.')
    except:
        db.rollback()
    db.close()
    return None


def srcLoans():
    # Get all enteties in Loans of the presented equipment
    equip = getEquipment()
    sqlLoans = "SELECT Loans.* FROM Loans, equipment  WHERE equipment.ID = '{}' AND Loans.equipID = equipment.ID".format(equip)
    #print(sqlLoans)
    
    try:
        c.execute(sqlLoans)     
        result = c.fetchall()
#         print(result[0])
        res = (result[0][0], result[0][1], result[0][2], result[0][3])
        return res
    except:
        print ("read error")

def checkIn():
    '''
    Register the return of the equipment
    '''
    #print('Takk for at du leverer tilbake utstyret')
    
    loans = srcLoans()
    print(loans)
    
    # Timestamp
    DT = DTstring()
    
    # Use selected elements in sqlLoans and
    sqlxLoans = ("INSERT INTO xLoans (xID, xempID, xequipID, xcheckOutDT, checkInDT) "
                    " VALUES({0},{1},{2},'{3}','{4}')").format(loans[0],
                                                          loans[1],
                                                          loans[2],
                                                          loans[3],
                                                          DT)
    sqlLoansDEL = ("DELETE FROM Loans WHERE ID={};").format(loans[0])
    sql = sqlxLoans + "; " +  sqlLoansDEL
    print(sql)
    try:
        c.execute(sqlxLoans)
        c.execute(sqlLoansDEL)
        db.commit()
        print('Registrert i databasen!')
        print('Takk for at du leverte tilbake!')
    except:
        db.rollback()
        print("Fail")
    db.close()
    return None



def connectDB():
    try:
        global db
        global c
        
        db = MySQLdb.connect(p.host, p.username, p.pword,"swequip")
        c = db.cursor()
        print("Connected to database...")
    except:
        print ("Waiting for server...")

def main():
    checkIn()


    
if __name__ == '__main__':
    
    connectDB()
    
    try:
        db = MySQLdb.connect(p.host, p.username, p.pword,"swequip")
        c = db.cursor()
        print("Connected to database...")
    except:
        print ("Waiting for server...")
             
    try:
      main()
    except KeyboardInterrupt:
      print ("bye bye...")
      pass    