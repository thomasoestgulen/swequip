#!/usr/bin/env python

import os
import time
import datetime
import MySQLdb

import parameters as p

global c
global db

class SQL():
    
    def __init__(self):
        try:
            global db
            global c
            
            db = MySQLdb.connect(p.host, p.username, p.pword,"swequip")
            c = db.cursor()
            print("Connected to database...")
        except:
            print ("Waiting for server...")
    
    def getEmployee(self):
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





def main():
    SQL.getEmployee()


    
if __name__ == '__main__':
    main()    


        
