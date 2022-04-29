from pydriller import *
import os
import sys

def getAllRepositories(stringFolder):
    with open(
            os.path.join(os.path.expanduser('~'), 'Desktop', 'results.txt'), 'w+'
    ) as f:
        stringFolder = stringFolder.replace("\\", "/")
        stringFolder = stringFolder.replace("\\\\", "/")

    f.close()

    my_list = os.listdir(stringFolder)

    urls = []
    for f in my_list:
        urls.append(stringFolder + "/" + f)

    for rep in urls:
        try:  # treba se ograditi od repozitorija bez Git-a u sebi da ne bi bilo problema
            r = Repository(rep)
            for commit in r.traverse_commits():
                break
            evaluationDMM(rep)
            print("")
        except Exception:
            print("Ovo nije ispravan git repository")



def listOfRepositories():
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

def englishCommit(repoString):
    full = 0
    length = 0
    startingWords = ["Initial", "Create", "Fix", "Add", "Remove", "Change", "Clear", "Initialize", "Merge", "Submit",
                     "Handle", "Update", "Set", "Move", "Force", "Expand", "Edit", "Check", "Modify", "Bump", "Refactor"]
    commits = Repository(repoString).traverse_commits()
    for commit in commits:
        send = 1
        message = commit.msg
        words = message.split(" ")
        print(words)
        if words[0].endswith("ing") or words[0].endswith("ed"):
            print("Wrong1")
            send -= 0.15
        if words[0][0].islower():
            print("Wrong2")
            send -= 0.15
        if not words[0] in startingWords:
            print("Wrong3")
            send -= 0.25
        if words[len(words) - 1].endswith("."):
            print("Wrong4")
            send -= 0.1
        if len(message) >= 50:
            print("Wrong5")
            send -= 0.25
        containsFile = False

        for w in words:
            if w != "Initial" and w != "Initialize":
                if modifiedFilesPerCommit(commit, w):
                    containsFile = True
            else:
                containsFile = True

        if not containsFile:
            print("Wrong6")
            send -= 0.1

        full += send
        length+=1

    return full/length

def evaluationDMM(repoString):
    rm = Repository(repoString)
    allunit = 0
    allcomplex = 0
    allinterfac = 0
    size = 0
    name = ""
    for commit in rm.traverse_commits():
        if name == "":
            name = commit.project_path  # mozda umjesto toga author.name

        size += 1
        if commit.dmm_unit_size is not None:
            allunit += commit.dmm_unit_size
        if commit.dmm_unit_complexity is not None:
            allcomplex += commit.dmm_unit_complexity
        if commit.dmm_unit_interfacing is not None:
            allinterfac += commit.dmm_unit_interfacing

    unitocjena = allunit / size
    complexocjena = allcomplex / size
    interocjena = allinterfac / size

    finalna = (unitocjena + complexocjena + interocjena) / 3
    print('Finalna ocjena {}', finalna)
    with open(
            os.path.join(os.path.expanduser('~'), 'Desktop', 'results.txt'), 'a+'
    ) as f:
        # f = open("results.txt", "a+")
        f.write(name + " " + str(finalna) + "\r\n")
    f.close()
    return finalna


if __name__ == '__main__':
    print('Number of arguments:', len(sys.argv), 'arguments.')
    print('Argument List:', str(sys.argv))
    # getAllrepos(sys.argv[1])
    # DMM_ocjena("https://github.com/icatic1/Promnesia")
    # englishCommit("https://github.com/vljubovic/c9etf")
    # DMM_ocjena("https://github.com/vljubovic/c9etf")
    a = englishCommit("https://github.com/adzaferbeg1/AuctionApp")
    b = evaluationDMM("https://github.com/adzaferbeg1/AuctionApp")
    print(a)
    print(b)
    print(a * 0.75 + b * 0.25)
