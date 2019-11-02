import csv
from oscar import Author,Commit,Commit_info


extention = {'ASP':['asp'], 'ASP.NET':['aspx','axd','asd','asmx','ashx'],'C':['c','h'],'C#':['cs'],'CSS':['css'], 
'C++' : ['cc','cpp','c++','cp','hh'], 'HTML':['html','htm','xhtml','jhtml'], 'Java':['jsp','jspx','wss','do','action'],
 'JavaScript':['js'], 'Perl':['pl'], 'PHP':['php', 'php4', 'php3', 'phtml'], 'Python': ['py'], 'Ruby':['rb','rhtml'], 
 'XML':['xml','rss','svg'],'document': ['txt','md'] }

def author2language(one):
	results = []
	shas = Author(one).commit_shas
	
	for sha in shas:
		timestamp = Commit_info(sha).time_author[0]
		file_names = Commit(sha).changed_file_names
		language = 'Other'
		for name in file_names:
			if '.' in name:
				file_extention = name.split('.')[-1].lower()
			else:
				file_extention = ''
			if file_extention:
				for la in extention.keys():
					if file_extention in extention[la]:
						language = la
						break
			#print((one,timestamp,sha,language))	
	                results.append({'Author':one,'TimeStamp':timestamp,'SHA':sha,'Language':language})

		

	return results

if __name__ == '__main__':
	author_file = open('../TAP/Result/author/cmtNum500.2Y.5devper')
	authors = author_file.readlines()
	headers = ['Author','TimeStamp','SHA','Language']
	with open('language.csv','w') as f:
    		f_csv = csv.DictWriter(f, headers)
    		f_csv.writeheader()
		for author in authors:
			results = author2language(author.strip())
			f_csv.writerows(results)
	




