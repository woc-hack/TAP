from oscar import Author, Commit, Project, Commit_info
import sys
from datetime import datetime
from config import filter
# assume readin author dump

for line in sys.stdin:
    num_prjs = 0
    author_set = set()
    for prj in Author(line.rstrip()).project_names:
        first, last = [32503736037, 0]
        for cmt in Project(prj).commit_shas:
            try:
                record = Commit_info(cmt).time_author
            except TypeError as e:
                sys.stderr.write(str(e)+'\n')
                continue
            if int(record[0]) < first:
                first = int(record[0])
            if int(record[0]) > last:
                last = int(record[0])
            begin_date = int(datetime.utcfromtimestamp(first).strftime('%Y%m%d'))
            end_date = int(datetime.utcfromtimestamp(last).strftime('%Y%m%d'))
            if (end_date-begin_date > filter["length_project"]*10000):
                print(line.rstrip())
                sys.stdout.flush()
                break
        if (end_date-begin_date > filter["length_project"]*10000):
            break
