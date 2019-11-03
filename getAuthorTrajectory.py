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
import gzip
import subprocess

#input_file = 'test_author_list.txt'
input_file = '../TAP/Result/author/cmtNum500.2Y.5devper'
output_file = 'author_data.csv'

class ProjectNames:
        def __init__(self):
                self.p_dict = {}
                self.print_process = False
        def getCanonicalName(self, project_names):
                mapped_pn = list(set(project_names).intersection(set(self.p_dict.keys())))
                if len(mapped_pn) > 0:
                        return self.p_dict[mapped_pn[0]]
                # for pn in project_names:
                #       if pn in self.p_dict.keys():
                #               return self.p_dict[pn]
                found_canon_name = False;
                fork_name = ""
                for pn in project_names:
                        user_process = subprocess.Popen("zgrep '" + pn + "' /da0_data/basemaps/gz/pP.map", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                        canon_fork_pair, err = user_process.communicate()
                        if self.print_process:
                                print(canon_fork_pair)
                        if canon_fork_pair != "":
                                canon_name = canon_fork_pair.split(";")[0]
                                if canon_name == "abb":
                                        if len(canon_fork_pair.split(";")) == 2:
                                                continue
                                        else:
                                                canon_name = canon_fork_pair.split(";")[1]
                                found_canon_name = True;
                                fork_name = pn
                                break
                if found_canon_name:
                        self.p_dict[fork_name] = canon_name
                        return canon_name
                else:
                        print("Could not find canonical name for this project! Use as is.")
                        self.p_dict[project_names[0]] = project_names[0]
                        return project_names[0]

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
                        project = pn.getCanonicalName(Commit(commit).project_names)
                        forks = len(Commit(commit).project_names)
			commit_message_dictionary[timestamp] = [author_name, timestamp, commit, len(message), len(full_message), type, sentiment, cleaned_message, project, forks]
	ordered_commit_message_dictionary = OrderedDict(sorted(commit_message_dictionary.items(), key=lambda t: t[0]))
	df = pd.DataFrame.from_dict(ordered_commit_message_dictionary, orient='index')
	out_file = open(output_file, 'a')
	df.to_csv(out_file, mode='a', header=False, index=False)
	out_file.close()

pn = ProjectNames()
#setup headers in output file and remove old data
df = pd.DataFrame(columns=['author_name', 'timestamp', 'sha','message_len', 'full_message_len', 'type','sentiment', 'message', 'project', 'forks'])
out_file = open(output_file, 'w')
df.to_csv(out_file, index=False)
out_file.close()

in_file = open(input_file)
# lines = in_file.readline()
lines = [line.rstrip('\n') for line in in_file]
# while line:
for line in lines[:2]:
        print(line)
	author_name = line.rstrip()
	get_author_data(author_name)
	line = in_file.readline()
in_file.close()
