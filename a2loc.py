import os
import csv
from oscar import Author,Commit,Commit_info

def author2loc(one):
	results = []
	shas = Author(one).commit_shas

	for sha in shas:
		timestamp = Commit_info(sha).time_author[0]
		files = os.popen('echo '+ sha +' | ssh da4 ~/lookup/cmputeDiff2.perl').readlines()
		for file in files:
			#print(file)
			old_sha = file.strip().split(';')[-2]
			new_sha = file.strip().split(';')[-1]
			addition = -1
			deletion = -1
			if old_sha:
				os.system('echo '+ old_sha + ' | ~/lookup/showCnt blob > old')
			else:
				addition = 0
				deletion = 0
			if new_sha:
				os.system('echo '+ new_sha + ' | ~/lookup/showCnt blob > new')
			else:
				addition = 0
				deletion = 0

			diffs = os.popen('diff old new')
			
			for diff in diffs:
				if diff.startswith('>'):
					addition = addition + 1
				if diff.startswith('<'):
					deletion = deletion + 1
			results.append({'Author':one,'TimeStamp':timestamp,'SHA':sha,'Addition':addition,'Deletion':deletion})
			#print((addition,deletion))

	return results

if __name__ == '__main__':
	author_file = open('../TAP/Result/author/cmtNum500.2Y.5devper')
    	authors = author_file.readlines()
    	headers = ['Author','TimeStamp','SHA','Adition','Deletion']
        with open('loc.csv','w') as f:
                f_csv = csv.DictWriter(f, headers)
                f_csv.writeheader()
                for author in authors:
                        results = author2loc(author.strip())
                        f_csv.writerows(results)





