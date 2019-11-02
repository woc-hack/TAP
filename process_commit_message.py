###########
#pre-requisites: must install textblob (pip install --user textblob)
#		 must install pandas (pip install --user pandas)
#		 must have NLTK corpora (python -m textblob.download_corpora)
###########

from oscar import *
from textblob import TextBlob 
import re 
from collections import OrderedDict
import pandas as pd

input_file = './test_author_list.txt'
#input_file = '../TAP/Result/author/cmtNum500.2Y.5devper'
output_file = 'author_data.csv'

#from https://github.com/ckeditor/ckeditor5-design/wiki/Git-commit-message-convention
types_by_convention = set(['Feature', 'Fix', 'Other', 'Code style', 'Docs', 'Internal', 'Tests', 'Revert'])

#assumes commit messages follow convention described in 
#https://github.com/ckeditor/ckeditor5-design/wiki/Git-commit-message-convention
def determine_commit_type(message):
	split_by_colon = message.split(':')
	if len(split_by_colon) > 1:
		if split_by_colon[0] in types_by_convention:
			return split_by_colon[0]
	return 'na'

#cleans message text by removing links and special characters using regex
#original code from https://www.geeksforgeeks.org/twitter-sentiment-analysis-using-python/
def clean_message(message): 
	return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", message).split()) 

#gets sentiment of message using textblob's sentiment method
#original code from https://www.geeksforgeeks.org/twitter-sentiment-analysis-using-python/
def get_message_sentiment(message): 
        textblob_object = TextBlob(clean_message(message)) 
        return textblob_object.sentiment.polarity

def get_author_data(author_name):
	commit_message_dictionary = {}
	for commit in Author(author_name).commit_shas:
		message = Commit(commit).message
		if len(message) > 0:
			cleaned_message = clean_message(message)
			full_message = Commit(commit).full_message
			timestamp = Commit_info(commit).time_author[0]
			type = determine_commit_type(message)
			sentiment = get_message_sentiment(message)
			commit_message_dictionary[timestamp] = [author_name, timestamp, commit, len(message), len(full_message), type, sentiment, cleaned_message]
	ordered_commit_message_dictionary = OrderedDict(sorted(commit_message_dictionary.items(), key=lambda t: t[0]))
	df = pd.DataFrame.from_dict(ordered_commit_message_dictionary, orient='index')
	out_file = open(output_file, 'a')
	df.to_csv(out_file, mode='a', header=False, index=False)
	out_file.close()

#setup headers in output file and remove old data
df = pd.DataFrame(columns=['author_name', 'timestamp', 'sha','message_len', 'full_message_len', 'type','sentiment', 'message'])
out_file = open(output_file, 'w')
df.to_csv(out_file, index=False)
out_file.close()

in_file = open(input_file)
line = in_file.readline()
while line:
	author_name = line.rstrip()
	get_author_data(author_name)
	line = in_file.readline()
in_file.close()
