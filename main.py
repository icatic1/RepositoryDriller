from pydriller import *
import os
import sys



def listOfRepos():
    urls = ["https://github.com/icatic1/Promnesia", "https://github.com/ooad-2020-2021/Grupa2-Fukupno"]
    for commit in Repository(path_to_repo=urls).traverse_commits():
        print("Project {},Author {}, commit {}, date {}".format(
            commit.project_path, commit.author.name, commit.hash, commit.author_date))


def modifiedFilesPerCommit(commit, stringFileName):
    for f in commit.modified_files:
        if f.filename == stringFileName:
            if f.nloc is not None and f.nloc > 2:
                return True

    return False




if __name__ == '__main__':
    listOfRepos()
