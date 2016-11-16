from sentiment_vs_stock.Stock_Price_Manipulation import stock_data

if __name__=='__main__':
	stock_name = 'TSLA'
	interval_seconds = 3600
	#
	response = stock_data.get_stock_data(interval_seconds, 10, stock_name)
	table = stock_data.parse_stock_data(response['data'], response['columns'], interval_seconds)
	stock_data.write_stock_table_to_csv(table['data'], table['columns'], stock_name+'.csv')
	print stock_data.get_stock_table_string(table['data'], table['columns'])
	print ''
	print 'Saved to %s.csv'%(stock_name)
#
