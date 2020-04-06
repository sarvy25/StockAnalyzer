from datetime import datetime
import csv
def get_closing_prices(data_path):
	data = {}
	with open(data_path, 'r') as f:
		cf = csv.DictReader(f, fieldnames=['Date','Close'])
		for row in cf:
			try:
				cdate = datetime.strptime(row['Date'], '%Y-%m-%d')
				key = '{}-{}'.format(cdate.year, cdate.month)
				if key not in data:
					data[key] = []
				cclose = row['Close']
				data[key].append((cdate.day, cclose))
			except:
				continue
	return data
