from operator import itemgetter

import requests

from plotly.graph_objs import Bar
from plotly import offline

# Make and API call and store the response.
url = 'https://hacker-news.firebaseio.com/v0/topstories.json'
r = requests.get(url)
print(f"Status code: {r.status_code}")

# Process information about each submission.
submission_ids = r.json()
submission_dicts = []
for submission_id in submission_ids[:30]:
	# Make a separate API call for each submission.
	url = f"https://hacker-news.firebaseio.com/v0/item/{submission_id}.json"
	r = requests.get(url)
	print(f"id: {submission_id}\tstatus: {r.status_code}")
	response_dict = r.json()

	# Build a dictionary for each article.
	if 'descendants' in response_dict:
		submission_dict = {
		'title': response_dict['title'],
		'hn_link': f"https://news.ycombinator.com/?id={submission_id}",
		'comments': response_dict['descendants']
		}

		submission_dicts.append(submission_dict)

submission_dicts = sorted(submission_dicts, key=itemgetter('comments'), reverse=True)

for submission_dict in submission_dicts:
	print(f"\nTitle: {submission_dict['title']}")
	print(f"Discussion link: {submission_dict['hn_link']}")
	print(f"Comments: {submission_dict['comments']}")

submission_links, submission_comments, titles = [], [], []
for submission_dict in submission_dicts:
	title = submission_dict['title']
	submission_url = submission_dict['hn_link']
	submission_link = f"<a href='{submission_url}'>{title[:15]}...</a>"

	submission_links.append(submission_link)
	submission_comments.append(submission_dict['comments'])
	titles.append(title)

data = [{
	'type': 'bar',
	'x': submission_links,
	'y': submission_comments,
	'marker': {
		'color': 'rgb(60, 100, 150)',
		'line': {'width': 1.5, 'color': 'rgb(25, 25, 25)'},
	},
	'opacity': 0.6,
	'hovertext': titles,
}]

my_layout = {
	'title': 'Most-commented articles on Hacker-news',
	'titlefont': {'size': 28},
	'title_x': 0.5,
	'xaxis': {
		'title': 'Article',
		'titlefont': {'size': 20},
		'tickfont': {'size': 8},
	},
	'yaxis': {
		'title': 'Comments',
		'titlefont': {'size': 24},
		'tickfont': {'size': 14},
	},
}

figure = {'data': data, 'layout': my_layout}
offline.plot(figure, filename='hn_comments.html')