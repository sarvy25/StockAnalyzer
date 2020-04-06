from flask import Flask, render_template, request, redirect, url_for, Response
from core import get_closing_prices
import os
from datetime import datetime
import matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
import io

app = Flask(__name__)

stock_names = ['Apple', 'Microsoft', 'Google', 'Facebook', 'Amazon']
logos = {'Apple': 'apple_logo.jpg',
		'Microsoft': 'microsoft_logo.jpg',
		'Google': 'google_logo.jpg',
		'Facebook': 'facebook_logo.png',
		'Amazon': 'amazon_logo.png'}

data_paths = {'Apple': 'data/aapl.us.txt',
			 'Microsoft': 'data/msft.us.txt',
			 'Google': 'data/googl.us.txt',
			 'Facebook': 'data/fb.us.txt',
			 'Amazon':'data/amzn.us.txt'
			}

descriptions = {'Apple': 'Apple Inc. is an American multinational technology company headquartered in Cupertino, California, that designs, develops, and sells consumer electronics, computer software, and online services.',
				'Microsoft': 'Microsoft Corporation is an American multinational technology company with headquarters in Redmond, Washington. It develops, manufactures, licenses, supports, and sells computer software, consumer electronics, personal computers, and related services.',
				'Google': 'Google LLC is an American multinational technology company that specializes in Internet-related services and products, which include online advertising technologies, search engine, cloud computing, software, and hardware.',
				'Facebook': 'Facebook is an American online social media and social networking service based in Menlo Park, California and a flagship service of the namesake company Facebook, Inc.',
				'Amazon': 'Amazon.com, Inc., is an American multinational technology company based in Seattle, with 750,000 employees. It focuses on e-commerce, cloud computing, digital streaming, and artificial intelligence.'
				}


@app.route("/plot*<string:selected_company>*<string:selected_month>.svg")
def plot_png(selected_company, selected_month):
	""" renders the plot on the fly.
	"""

	font = {'family':'serif',
			'serif':'Times',
	        'size'   : 24}

	matplotlib.rc('font', **font)

	month_prices = get_closing_prices(data_paths[selected_company])
	data = month_prices[selected_month]

	fig = Figure(figsize=(20, 10))
	axis = fig.add_subplot(1, 1, 1)
	xs = [x[0] for x in data]
	ys = [x[1] for x in data]
	axis.plot(xs, ys, 'g-*', linewidth=3, markersize=20)
	axis.set_xlabel('Day', fontsize=24)
	axis.set_ylabel('Closing Price', fontsize=24)
	axis.set_title('{} Closing Price for Month {}'.format(selected_company, selected_month))
	output = io.BytesIO()
	FigureCanvasAgg(fig).print_png(output)
	return Response(output.getvalue(), mimetype="image/svg")

@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		selected_company = request.form.get('company')
		month_prices = get_closing_prices(data_paths[selected_company])
		available_dates = month_prices.keys()
		available_dates = sorted(available_dates, key= lambda x: datetime.strptime(x, '%Y-%m'), reverse=True)
		selected_month = request.form.get('month')
		return render_template('index.html',
			logo_path=logos,
			companies=stock_names,
			selected_company=selected_company,
			descriptions=descriptions,
			available_dates=available_dates,
			data=month_prices[selected_month],
			selected_month=selected_month)
	else:
		selected_company = 'Google'

		month_prices = get_closing_prices(data_paths[selected_company])
		
		available_dates = month_prices.keys()
		available_dates = sorted(available_dates, key= lambda x: datetime.strptime(x, '%Y-%m'), reverse=True)
		selected_month = available_dates[0]
		return render_template('index.html',
			logo_path=logos,
			companies=stock_names,
			selected_company=selected_company,
			descriptions=descriptions,
			available_dates=available_dates,
			data=month_prices[selected_month],
			selected_month=selected_month)

@app.route('/about')
def about():
  return render_template('about.html')

if __name__ == '__main__':
  app.run(port=33507)
