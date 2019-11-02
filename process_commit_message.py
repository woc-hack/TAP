###########
#pre-requisites: must install textblob (pip install --user textblob)
#		 must have NLTK corpora (python -m textblob.download_corpora)
###########

from oscar import *
from textblob import TextBlob 
import re 

#update to loop through list of authors after filters complete
author_name = 'First Last <email>'

#from https://github.com/ckeditor/ckeditor5-design/wiki/Git-commit-message-convention
types_by_convention = set(['Feature', 'Fix', 'Other', 'Code style', 'Docs', 'Internal', 'Tests', 'Revert'])

for commit in Author(author_name).commit_shas:
	message = Commit(commit).message
	if len(message) > 0:
		full_message = Commit(commit).full_message
		timestamp = Commit_info(commit).time_author[0]
		type = determine_commit_type(message)
		sentiment = get_message_sentiment(message)
		print(timestamp, commit, len(message), len(full_message), type, sentiment)

#assumes commit messages follow convention described in 
#https://github.com/ckeditor/ckeditor5-design/wiki/Git-commit-message-convention
def determine_commit_type(message):
	split_by_colon = message.split(':')
	if len(split_by_colon) > 1:
		if split_by_colon[0] in types_by_convention:
			return split_by_colon[0]
		else:
			return 'None'

#cleans message text by removing links and special characters using regex
#original code from https://www.geeksforgeeks.org/twitter-sentiment-analysis-using-python/
def clean_message(message): 
	return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", message).split()) 

#gets sentiment of message using textblob's sentiment method
#original code from https://www.geeksforgeeks.org/twitter-sentiment-analysis-using-python/
def get_message_sentiment(message): 
        textblob_object = TextBlob(clean_message(message)) 
        if textblob_object.sentiment.polarity > 0: 
            return 'positive'
        elif textblob_object.sentiment.polarity == 0: 
            return 'neutral'
        else: 
            return 'negative'
