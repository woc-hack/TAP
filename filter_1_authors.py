from oscar import Author, Commit, Project, Commit_info
import sys
from datetime import datetime
from config import filter
# assume readin author dump

for line in sys.stdin:
    first, last = [32503736037, 0]
    for cmt in Author(line.strip()[1:-1]).commit_shas:
        #in tuple, ("unixtime", "<email>")
        record = Commit_info(cmt).time_author
        if int(record[0]) < first:
            first = int(record[0])
        if int(record[0]) > last:
            last = int(record[0])
    begin_date = int(datetime.utcfromtimestamp(first).strftime('%Y%m%d'))
    end_date = int(datetime.utcfromtimestamp(last).strftime('%Y%m%d'))
    if (end_date-begin_date > filter["lenght_developemnt"]*10000):
        print(line.strip()[1:-1])
