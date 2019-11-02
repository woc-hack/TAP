from oscar import Author, Commit, Project, Commit_info
import sys
from datetime import datetime
from config import filter
# assume readin author dump

for line in sys.stdin:
    num_prjs = 0
    author_set = set()
    for prj in Author(line.strip()[1:-1]).project_names:
        author_set.update(set(Project(prj).author_names))
        if len(author_set) > filter["number_developers"]:
            print(line.strip()[1:-1])
            sys.stdout.flush()
            break