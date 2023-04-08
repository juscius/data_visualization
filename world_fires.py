import csv
from datetime import datetime

from plotly.graph_objs import Scattergeo, Layout
from plotly import offline

num_rows = 10_000

filename='data/world_fires_1_day.csv'

with open(filename) as f:
	reader = csv.reader(f)
	header_row = next(reader)

	lons, lats, dates, brightness_list, hover_texts = [], [], [], [], []
	row_num = 0 

	for row in reader:
		date_index = header_row.index('acq_date')
		date = datetime.strptime(row[date_index], '%Y-%m-%d')

		lon_index = header_row.index('longitude')
		lat_index = header_row.index('latitude')

		brightness_index = header_row.index('brightness')
		brightness = float(row[brightness_index])
		
		label = f"{date.strftime('%m/%d/%y')} - {brightness}"

		dates.append(date)
		lats.append(row[lat_index])
		lons.append(row[lon_index])
		brightness_list.append(brightness)
		hover_texts.append(label)

		row_num += 1
		if row_num == num_rows:
			break
			
# Map the earthquakes.

data = [{
	'type': 'scattergeo',
	'lon': lons,
	'lat': lats,
	'text': hover_texts,
	'marker': {
		'size': [bright/20 for bright in brightness_list],
		'color': brightness_list,
		'colorscale': 'YlOrRd',
		'reversescale': False,
		'colorbar': {'title': 'Brightness'},
	},
}]

my_layout = Layout(title='World fires 1 day', title_x=0.5)

figure = {
	'data': data,
	'layout': my_layout,
	}

offline.plot(figure, filename='world_fires.html')