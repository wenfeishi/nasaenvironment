from django.shortcuts import render
from django.http import HttpResponse
import numpy as np
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import components
import pandas as pd
import MySQLdb as DB
import sys
import os
import json
from django.conf import settings
from bokeh.io import curdoc,vform
from bokeh.models import ColumnDataSource, DataRange1d, Range1d, VBox, HBox, Select
from bokeh.palettes import Blues4
from bokeh.plotting import Figure

#import requests
BASE_DIR = settings.BASE_DIR
STATIC=os.path.join(BASE_DIR, 'static')
PICS = os.listdir(os.path.join(BASE_DIR, 'static/img'))
# Create your views here.

print PICS

def index(request):

    return render(request, 'index.html')
    
def earthquake(request):

    return render(request, 'earthquake.html')
    
def bird(request):

    return render(request, 'bird.html')
	
def img(request):
	
	img_path=os.path.join(STATIC, 'img/Temprature.png')
	return render(request,'{% load staticfiles %}<img src=" {% static "img/Temprature.png" %}">')
	
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
		
	plot = Figure(x_range=[1895,2016], y_range=[-10,8], plot_width=1000, tools="", toolbar_location=None)
	plot.title = "Plot of temprature of month %s from 1895-2015" % month[0]
	colors = Blues4[0:3]
	plot.border_fill_color = "whitesmoke"
	plot.xaxis.axis_label = "Year"
	plot.yaxis.axis_label = "Temperature (F)"
	plot.axis.major_label_text_font_size = "8pt"
	plot.axis.axis_label_text_font_size = "8pt"
	plot.axis.axis_label_text_font_style = "bold"
	plot.x_range = DataRange1d(range_padding=0.0, bounds=None)
	plot.grid.grid_line_alpha = 0.3
	plot.grid[0].ticker.desired_num_ticks = 12
	plot.line(year, USCRN, color='#A6CEE3', legend='AAPL')
	plot.line(year, CLIMDIV, color='#B2DF8A', legend='GOOG')
	plot.line(year, CMBUSHCN, color='#33A02C', legend='IBM')
	

	#fig=plt.figure(figsize=(16,12))
	#plt.xlabel('Year')
	#plt.ylabel('Temprature')
	#plt.style.use('ggplot')
	#plt.plot(year,USCRN,'ro-')
	#plt.plot(year,CLIMDIV,'go-')
	#plt.plot(year,CMBUSHCN,'bo-')
	#plt.axis([1895,2016,-10,8])
	#plt.title('Plot of temprature of month %s from 1895-2015' %month[0])
	#os.remove(os.getcwd() + '\Temprature.png')
	#plt.savefig(os.path.join(BASE_DIR, 'static\img\Temprature.png'),dpi=80)
	#plt.savefig(os.path.join(BASE_DIR, 'static\img\Temprature2.png'),dpi=80)
	#fig.clf()
	#plt.close(fig)
	#img=open(os.getcwd() + '\Temprature.png',"rb")
	#response = django.http.HttpResponse(content_type="image/png")
	#plt.savefig(response, format="png")
	#img=open("Temprature.png", "rb")
	#img.save(response, "PNG")
    #img.close()
	#image_bytes = requests.get(os.path.join(BASE_DIR, 'static\img\Temprature.png').content
	#image_bytes.save(response,"PNG")#lambda x: x.startswith('Temprature')
	#f = open(os.path.join(BASE_DIR, 'static\img\Temprature.png'),"rb")
	#img = f.read()
	#f.close()
	cur.close()
	cnx.close()	
	script,div=components(plot)
	return render(request, "temp.html",{"this_script": script, "this_div": div})
	#return HttpResponse(month)
	#return HttpResponse(
        #json.dumps(month),
        #content_type='image/png')
	#with open(os.path.join(BASE_DIR, 'static\img\Temprature.png'), "rb") as f:
	    #return HttpResponse(f.read(), content_type="image/png")
