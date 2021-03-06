from django.shortcuts import render
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import components
from os.path import join, dirname
import numpy as np
import pandas as pd

from bokeh.io import curdoc,vform
from bokeh.models import ColumnDataSource, DataRange1d, Range1d, VBox, HBox, Select
from bokeh.palettes import Blues4
from bokeh.plotting import Figure


STATISTICS = ['record_min_temp', 'actual_min_temp', 'average_min_temp', 'average_max_temp', 'actual_max_temp', 'record_max_temp']

def city(request):

    return render(request, 'city.html')
    
def energy(request):
    return render(request,'energy.html')

def simple_chart(request):
    plot = figure()
    plot.circle([1,2], [3,4])

    script, div = components(plot, CDN)

    return render(request, "simple_chart.html", {"the_script": script, "the_div": div})
	
# Create your views here.

# Filter for smoothing data originates from http://stackoverflow.com/questions/20618804/how-to-smooth-a-curve-in-the-right-way
def chart(request):
	def get_dataset(src, name, distribution):
		df = src[src.airport == name].copy()
		del df['airport']
		df['date'] = pd.to_datetime(df.date)
		df['left'] = df.date #- pd.DateOffset(days=0.5)
		df['right'] = df.date #+ pd.DateOffset(days=0.5)
		df = df.set_index(['date'])
		df.sort_index(inplace=True)
		if distribution == 'Smooth':
			window, order = 51, 3
			#for key in STATISTICS:
				#df[key] = savgol_filter(df[key], window, order)

		return ColumnDataSource(data=df)


	def make_plot(source, title):
		print("make plot")
		plot = Figure(x_axis_type="datetime", plot_width=1000, tools="", toolbar_location=None)
		plot.title = title
		colors = Blues4[0:3]

		plot.quad(top='record_max_temp', bottom='record_min_temp', left='left', right='right', color=colors[2], source=source, legend="Record")
		plot.quad(top='average_max_temp', bottom='average_min_temp', left='left', right='right', color=colors[1], source=source, legend="Average")
		plot.quad(top='actual_max_temp', bottom='actual_min_temp', left='left', right='right', color=colors[0], alpha=0.5, line_color="black", source=source, legend="Actual")

		# fixed attributes
		plot.border_fill_color = "whitesmoke"
		plot.xaxis.axis_label = None
		plot.yaxis.axis_label = "Temperature (F)"
		plot.axis.major_label_text_font_size = "8pt"
		plot.axis.axis_label_text_font_size = "8pt"
		plot.axis.axis_label_text_font_style = "bold"
		plot.x_range = DataRange1d(range_padding=0.0, bounds=None)
		plot.grid.grid_line_alpha = 0.3
		plot.grid[0].ticker.desired_num_ticks = 12

		return plot


	# set up callbacks
	def update_plot(attrname, old, new):
		print("update called")
		city = city_select.value
		plot.title = cities[city]['title']

		src = get_dataset(df, cities[city]['airport'], distribution_select.value)
		for key in STATISTICS + ['left', 'right']:
			source.data.update(src.data)


		# set up initial data
	print("main called")
	city = request.GET['city']
	print("city is %s" % city)
	if len(city)==0:
		city = 'Boston'
	distribution = 'Discrete'

	cities = {
		
		'Boston': {
			'airport': 'BOS',
			'title': 'Boston, MA',
		},
		'Austin': {
			'airport': 'AUS',
			'title': 'Austin, TX',
		},
		'Seattle': {
			'airport': 'SEA',
			'title': 'Seattle, WA',
		}
	}

	#city_select = Select(value=city, title='City', options=sorted(cities.keys()))
	#distribution_select = Select(value=distribution, title='Distribution', options=['Discrete', 'Smooth'])

	df = pd.read_csv(join(dirname(__file__), 'data/2015_weather.csv'))
	source = get_dataset(df, cities[city]['airport'], distribution)
	plot = make_plot(source, cities[city]['title'])

	#city_select.on_change('value', update_plot)
	#distribution_select.on_change('value', update_plot)

	#controls = VBox(city_select, distribution_select)
	s = HBox(plot)
	script,div=components(s)
	#script2,div2=components(plot)
	# add to document
	#curdoc().add_root(HBox(controls, plot))
	#script, div = components(vform(controls, plot))
	#script, div = components(HBox(controls, plot))
	return render(request, "chart.html",{"the_script": script, "the_div": div})
