from sentiment_vs_stock.Sentiment_Analysis.nltk_vader_sentiment_analysis import get_sentiment_from_text
from sentiment_vs_stock.mongo_helpers import loop_over_collection
from misc.logging_helper import setup_logging

if __name__ == '__main__':
	setup_logging('print_tweets')
	#
	collection_name = 'costco'
	num_of_tweets = 60
	#
	def process_record(record, collection, counter):
		print record['text'].encode('utf-8')
		print get_sentiment_from_text(record['text'])
		print
		#
		if counter > num_of_tweets:
			return False
		#
	#
	loop_over_collection(collection_name, process_record)
#