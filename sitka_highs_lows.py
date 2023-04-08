import csv
from datetime import datetime

import matplotlib.pyplot as plt


filename = 'data/sitka_weather_2018_simple.csv'

with open(filename) as f:
	reader = csv.reader(f)
	header_row = next(reader)
	high_index = header_row.index('TMAX')
	low_index = header_row.index('TMIN')
	date_index = header_row.index('DATE')
	# Get the dates and high and low temperatures from this file.
	dates, highs, lows = [], [], []
	for row in reader:
		current_date = datetime.strptime(row[date_index], '%Y-%m-%d')
		high = int(row[high_index])
		low = int(row[low_index])
		dates.append(current_date)
		highs.append(high)
		lows.append(low)

# Indexing every header with its position in the list.
#for index, column_header in enumerate(header_row):
#	print(index, column_header)
#results = [print(index, column_header) for index, column_header in enumerate(header_row)]

#Plot the high and low temperatures
plt.style.use('seaborn')
fig, ax = plt.subplots()
ax.plot(dates, highs, c='red', alpha=0.5)
ax.plot(dates, lows, c='blue', alpha=0.5)
ax.fill_between(dates, highs, lows, facecolor='blue', alpha=0.1)
#Format plot.
ax.set_title("Daily high and low temperatures - 2018", fontsize=24)
ax.set_xlabel('Dates', fontsize=16)
fig.autofmt_xdate()
ax.set_ylabel("Temperature (F)", fontsize=16)
ax.tick_params(axis='both', which='major', labelsize=16)
plt.get_current_fig_manager().full_screen_toggle()
plt.show()