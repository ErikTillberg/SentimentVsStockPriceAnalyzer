import requests
import datetime
from prettytable import PrettyTable
import csv
#
def get_stock_data(interval_seconds, num_days, stock):
	num_of_header_lines = 7
	#
	r = requests.get("https://www.google.com/finance/getprices?i=%d&p=%dd&f=d,o,h,l,c,v&df=cpct&q=%s"%(interval_seconds, num_days, stock))
	#
	text = r.content.split("\n", num_of_header_lines)
	lines = text[len(text)-1].split("\n")
	#
	header = text[0:(len(text)-1)]
	#
	columns = header[4].split("=",1)[1].split(',')
	#
	return {'header':header, 'columns':columns, 'data':lines}
#
def parse_stock_data(data, columns, interval_seconds):
	new_data = []
	last_time_stamp = None
	#
	for x in data:
		if x.strip() != '':
			line = [y.strip() for y in x.split(',')]
			if line[0][0] == 'a':
				line[0] = int(line[0][1:])
				last_time_stamp = line[0]
			else:
				if line[0] == 'TIMEZONE_OFFSET=-300': continue 
				line[0] = int(last_time_stamp)+interval_seconds*int(line[0])
			#
			line.append(datetime.datetime.fromtimestamp(line[0]).strftime('%Y-%m-%d %H:%M:%S'))
			#
			for z in xrange(len(line)):
				try:
					line[z] = float(line[z])
				except ValueError:
					pass
				#
			#
			new_data.append(line)
		#
	#
	columns = list(columns)
	# makes a copy
	columns.append('DATE_STR')
	return {'data':new_data, 'columns':columns}
#
def get_stock_table_string(data, columns):
	t = PrettyTable(columns)
	for x in data:
		t.add_row(x)
	return t
#
def write_stock_table_to_csv(data, columns, filename):
	with open(filename, 'wb') as f:
		wr = csv.writer(f, quoting=csv.QUOTE_ALL)
		wr.writerow(columns)
		for x in data:
			wr.writerow(x)
		#
	#
#
if __name__=='__main__':
	stock_name = 'TSLA'
	interval_seconds = 3600
	#
	response = get_stock_data(interval_seconds, 10, stock_name)
	print response['header']
	table = parse_stock_data(response['data'], response['columns'], interval_seconds)
	print get_stock_table_string(table['data'], table['columns'])
	write_stock_table_to_csv(table['data'], table['columns'], stock_name+'.csv')
#
