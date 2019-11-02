
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
			print((timestamp,sha,language))	
	                results.append((timestamp,sha,language))

		

	return results

if __name__ == '__main__':
	print(author2language('Warner Losh <imp@FreeBSD.org>'))





