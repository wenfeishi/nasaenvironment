# hello.py

import numpy as np
import matplotlib.pyplot as plt
import MySQLdb as DB
import sys

cnx = DB.connect(host='ec500-nasa.csmyiysxb7lc.us-east-1.rds.amazonaws.com',user='root',passwd='nasaenvironment',db='environment')
cur = cnx.cursor()
#cur.execute("SELECT VERSION()")
#data = cur.fetchone()
#print "Database Version:%s" % data
#sql = "SELECT * FROM environment.Temp_Deviation_Monthly WHERE Month=2"
year =[]
month=[]
USCRN =[]
CLIMDIV =[]
CMBUSHCN =[]
try:
  cur.execute("SELECT * FROM environment.Temp_Deviation_Monthly WHERE Month=1")
  data=cur.fetchall()

  for row in data:
   year.append(row[0])
   
	
  for row in data:
    month.append(row[1])
 
  for row in data:
    USCRN.append(row[2])
	
  for row in data:
    CLIMDIV.append(row[3])  
	
  for row in data:
    CMBUSHCN.append(row[4])    	
	
except:
   print "Error: unable to fecth data"

plt.figure(figsize=(16,12))
plt.xlabel('Year')
plt.ylabel('Temprature')
plt.plot(year,USCRN,'ro-')
plt.plot(year,CLIMDIV,'go-')
plt.plot(year,CMBUSHCN,'bo-')
plt.axis([1895,2016,-10,8])
plt.title('Plot of temprature from 1895-2015')

plt.show()
#plt.savefig('Temprature.png',dpi=80)
if cnx:
  cnx.close()