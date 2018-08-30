# this takes in the text of a call transcription and analyzes it for sentiment

from textblob import TextBlob
from nltk import *
# from nltk.tree import *

def analyzeSentiment(text):
	stmt = TextBlob(text).sentiment
	p = stmt.polarity
	result = ""
	if p > 0.5:
		result = "VERY HAPPY"
	elif p < 0.5 and p > 0.0:
		result = "SLIGHTLY HAPPY"
	elif p < 0.0 and p > -0.5:
		result = "SLIGHTLY ANGRY"
	elif p < -0.5:
		result = "VERY ANGRY"
	elif  p == 0:
		result = "NEUTRAL"
	else:
		result = "UNKNOWN"
	return result

#def makeTree(text):
