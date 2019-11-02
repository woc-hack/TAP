import os
from oscar import Author,Commit,Commit_info

def author2loc(one):
	results = []
	shas = Author(one).commit_shas

	for sha in shas:
		timestamp = Commit_info(sha).time_author[0]
		files = os.popen('echo '+ sha +' | ssh da4 ~/lookup/cmputeDiff2.perl').readlines()
		for file in files:
			old_sha = file.strip().split(';')[-2]
			new_sha = file.strip().split(';')[-1]
			os.system('echo '+ old_sha + ' | ~/lookup/showCnt blob > old')
			os.system('echo '+ new_sha + ' | ~/lookup/showCnt blob > new')
			diffs = os.popen('diff old new')
			addition = -1
			deletion = -1
			for diff in diffs:
				if diff.startswith('>'):
					addition = addition + 1
				if diff.startswith('<'):
					deletion = deletion + 1
			results.apppend((timestamp,sha,addition,deletion))
			print((addition,deletion))

	return results

if __name__ == '__main__':
	print(author2loc('Warner Losh <imp@FreeBSD.org>'))





