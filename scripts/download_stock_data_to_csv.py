from sentiment_vs_stock.Stock_Price_Manipulation import stock_data

if __name__=='__main__':
	stock_name = 'TSLA'
	interval_seconds = 3600
	#
	response = stock_data.get_stock_data(interval_seconds, 10, stock_name)
	table = stock_data.parse_stock_data(response['data'], interval_seconds)
	print stock_data.get_stock_table_string(table)
	stock_data.write_stock_table_to_csv(table, stock_name+'.csv')
	print ''
	print 'Saved to %s.csv'%(stock_name)
#
