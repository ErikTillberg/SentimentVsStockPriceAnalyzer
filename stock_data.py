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
	lines = text[num_of_header_lines].split("\n")
	#
	return {'header':text[0:num_of_header_lines], 'data':lines}
#
def parse_stock_data(data):
	table = []
	last_time_stamp = None
	#
	for x in data:
		if x.strip() != '':
			line = [y.strip() for y in x.split(',')]
			if line[0][0] == 'a':
				line[0] = int(line[0][1:])
				last_time_stamp = line[0]
			else:
				line[0] = int(last_time_stamp)+interval*int(line[0])
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
			table.append(line)
		#
	#
	return table
#
def get_stock_table_string(table):
	t = PrettyTable(['DATE', 'CLOSE', 'HIGH', 'LOW', 'OPEN', 'VOLUME', 'DATE_STR'])
	for x in table:
		t.add_row(x)
	return t
#
def write_stock_table_to_csv(table, filename):
	with open(filename, 'wb') as f:
		wr = csv.writer(f, quoting=csv.QUOTE_ALL)
		wr.writerow(['DATE', 'CLOSE', 'HIGH', 'LOW', 'OPEN', 'VOLUME', 'DATE_STR'])
		for x in table:
			wr.writerow(x)
		#
	#
#
if __name__=='__main__':
	response = get_stock_data(3600, 30, 'AAPL')
	print response['header']
	table = parse_stock_data(response['data'])
	print get_stock_table_string(table)
	write_stock_table_to_csv(table, 'temp.csv')
#
