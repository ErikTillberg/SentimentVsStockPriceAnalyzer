import logging

from nltk_vader_sentiment_analysis import get_sentiment_from_text
from ..Stock_Price_Manipulation import stock_data
from ..mongo_helpers import loop_over_collection

_logger = logging.getLogger(__name__)

def add_vader_sentiment_to_collection(collection_name, log_debugging=False):
	def process_record(record, collection, counter):
		try:
			sentiment = get_sentiment_from_text(record['text'])
			collection.update_one({
				'_id': record['_id']
			},
			{
				'$set': {
					'sentiment': sentiment
				}
			})
		except:
			pass
		#
	#
	loop_over_collection(collection_name, process_record, 1000)
#
if __name__ == '__main__':
	logging.basicConfig(level=logging.DEBUG)
	#
	collection_name = 'apple_filtered'
	#
	add_vader_sentiment_to_collection(collection_name, True)
#