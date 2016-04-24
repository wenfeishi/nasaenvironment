from django.shortcuts import render
from django.http import HttpResponse
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
#import pandas as pd
import MySQLdb as DB
import sys
import os
import json
from django.conf import settings
#import requests
BASE_DIR = settings.BASE_DIR
PICS = os.listdir(os.path.join(BASE_DIR, 'static/img'))
# Create your views here.

print PICS

def index(request):

    return render(request, 'index.html')
	
def datavisualization(request):

    return render(request, 'data-visualization.html')
	
def temppng(request):

    return render(request, 'temppng.html')
	
def maps(request):

    return render(request, 'maps.html')
	
def temp(request):
	month = request.GET['month']
	cnx = DB.connect(host='ec500-nasa.csmyiysxb7lc.us-east-1.rds.amazonaws.com',user='root',passwd='nasaenvironment',db='environment')
	cur = cnx.cursor()
	#cur.execute("SELECT VERSION()")
	#data = cur.fetchone()
	#print "Database Version:%s" % data
	sql = "SELECT * FROM environment.Temp_Deviation_Monthly WHERE Month=%s" %month
	year =[]
	month=[]
	USCRN =[]
	CLIMDIV =[]
	CMBUSHCN =[]
	try:
		cur.execute(sql)
		data=cur.fetchall()

		for row in data:
			year.append(row[0])
			month.append(row[1])
			USCRN.append(row[2])
			CLIMDIV.append(row[3])  
			CMBUSHCN.append(row[4])    	
	
	except:
		print "Error: unable to fecth data"

	fig=plt.figure(figsize=(16,12))
	plt.xlabel('Year')
	plt.ylabel('Temprature')
	plt.style.use('ggplot')
	plt.plot(year,USCRN,'ro-')
	plt.plot(year,CLIMDIV,'go-')
	plt.plot(year,CMBUSHCN,'bo-')
	plt.axis([1895,2016,-10,8])
	plt.title('Plot of temprature of month %s from 1895-2015' %month[0])
	#os.remove(os.getcwd() + '\Temprature.png')
	plt.savefig(os.path.join(BASE_DIR, 'static/img/Temprature.png'),dpi=80)
	fig.clf()
	plt.close(fig)
	#img=open(os.getcwd() + '\Temprature.png',"rb")
	#response = django.http.HttpResponse(content_type="image/png")
	#plt.savefig(response, format="png")
	#img=open("Temprature.png", "rb")
	#img.save(response, "PNG")
    #img.close()
	#image_bytes = requests.get(os.path.join(BASE_DIR, 'static\img\Temprature.png').content
	#image_bytes.save(response,"PNG")#lambda x: x.startswith('Temprature')
	f = open(os.path.join(BASE_DIR, 'static/img/Temprature.png'),"rb")
	img = f.read()
	f.close()
	cur.close()
	cnx.close()	
	return HttpResponse(month)
	#return HttpResponse(
        #json.dumps(img),
        #content_type='image/png')
	#with open(os.path.join(BASE_DIR, 'static\img\Temprature.png'), "rb") as f:
	    #return HttpResponse(f.read(), content_type="image/png")