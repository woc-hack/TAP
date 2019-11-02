import os
from comment_parser import comment_parser
from oscar import Author,Commit,Commit_info

def author2comment(one):
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
			addition = ''
			deletion = ''
			for diff in diffs:
				if diff.startswith('>'):
					addition = addition + diff[1:]
				if diff.startswith('<'):
					deletion = deletion + diff[1:]

			add_comment_words = 0
			add_comment_line = 0
			dele_comment_words = 0
			dele_comment_line = 0

			add_comment = comment_parser.extract_comments_from_str(addition)
			for item in add_comment:
				add_comment_line = add_comment_line + item.line_number
				add_comment_words = add_comment_words + len(item.text.split(' '))

			dele_comment = comment_parser.extract_comments_from_str(deletion)
			for item in dele_comment:
				dele_comment_line = dele_comment_line + item.line_number
				dele_comment_words = dele_comment_words + len(item.text.split(' '))

			comment_lines = abs(add_comment_line - dele_comment_line)
			comment_words = abs(add_comment_words - dele_comment_words)
			results.apppend((timestamp,sha,comment_lines,comment_words))
			print((comment_lines,comment_wordso))

	return results

if __name__ == '__main__':
	print(author2comment('Warner Losh <imp@FreeBSD.org>'))





