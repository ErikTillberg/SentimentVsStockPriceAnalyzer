'''
To run this, you need to pip install nltk and twython.
Once you install those, you need to download the corpora.
Run python:
	import nltk
	nltk.download()
In the GUI, select the Vader and punkt tokenizer data sets.

References:
http://www.nltk.org/api/nltk.sentiment.html#module-nltk.sentiment.vader
http://www.nltk.org/howto/sentiment.html

Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model
for Sentiment Analysis of Social Media Text. Eighth International Conference
on Weblogs and Social Media (ICWSM-14). Ann Arbor, MI, June 2014.
'''
#
from __future__ import print_function
from nltk.sentiment.vader import SentimentIntensityAnalyzer
#
sid = SentimentIntensityAnalyzer()
# make this global so we don't have to repeatedly initialize it
#
def get_sentiment_from_text(text):
	return sid.polarity_scores(text)
#
if __name__ == '__main__':
	print(get_sentiment_from_text("This iphone is amazing."))
#