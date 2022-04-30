from git import InvalidGitRepositoryError
from pydriller import *
import os
import sys


def getAllRepositories(stringFolder, language):
    stringFolder = stringFolder.replace("\\", "/")
    stringFolder = stringFolder.replace("\\\\", "/")

    my_list = os.listdir(stringFolder)

    urls = []
    for f in my_list:
        urls.append(stringFolder + "/" + f)

    for rep in urls:
        try:  # treba se ograditi od repozitorija bez Git-a u sebi da ne bi bilo problema
            r = Repository(rep)
            author = ""
            for commit in r.traverse_commits():
                author = commit.author.name
                break
            eComm = None
            eDMM = evaluationDMM(rep)
            if language == "-b":
                eComm = bosnianCommit(rep)
            else:
                eComm = englishCommit(rep)
            print(rep + " -- " + author)
            with open(
                    os.path.join(os.path.expanduser('~'), 'Desktop', 'results.txt'), 'a+'
            ) as f:
                f.write(rep + "," + author + "," + str(eComm * 0.8 + eDMM * 0.2) + "\r\n")
            f.close()
        except InvalidGitRepositoryError:
            print("Nije ispravan git repository")


def modifiedFilesPerCommit(commit, stringFileName):
    for f in commit.modified_files:
        if ".xml" or ".fxml" in f.filename:
            if commit.modified_files != 1 and f.change_type == "Added":
                return True
        if len(f.changed_methods) == 1:
            return True
        if f.filename == stringFileName:
            if f.nloc is not None and f.nloc > 2:
                return True

    return False


def englishCommit(repoString):
    full = 0
    length = 0
    startingWords = ["Initial", "Create", "Fix", "Add", "Remove", "Change", "Clear", "Initialize", "Merge", "Submit",
                     "Handle", "Update", "Set", "Move", "Force", "Expand", "Edit", "Check", "Modify", "Bump",
                     "Refactor"]
    commits = Repository(repoString).traverse_commits()
    for commit in commits:
        send = 1
        message = commit.msg
        words = message.split(" ")

        if words[0].endswith("ing") or words[0].endswith("ed"):
            print("Wrong1")
            send -= 0.15
        if words[0][0].islower():
            print("Wrong2")
            send -= 0.15
        if not words[0] in startingWords:
            print("Wrong3")
            send -= 0.25
            if words[0][0].islower():
                send += 0.1
        if words[len(words) - 1].endswith("."):
            print("Wrong4")
            send -= 0.1
        if len(message) >= 50:
            print("Wrong5")
            send -= 0.25
        containsFile = False

        for w in words:
            if w != "Initial" and w != "Refactor" and w != "Change" and w != "Edit" and w != "Modify":
                if modifiedFilesPerCommit(commit, w):
                    containsFile = True
            else:
                containsFile = True

        if not containsFile:
            print("Wrong6")
            send -= 0.1

        full += send
        length += 1

    return full / length


def bosnianCommit(repoString):
    full = 0
    length = 0

    startingWordsBosnian = ["Dodan", "Promjen", "Isprav", "Reorganiz", "Zavrsen", "Inicijaliz",
                            "Spoj", "Preda", "Obrad", "Ažurira", "Postav", "Pomjer", "Forsir", "Prošir", "Ured",
                            "Izmijen",
                            "Refaktor", "Kreira", "Uklon"]
    commits = Repository(repoString).traverse_commits()
    for commit in commits:
        send = 1
        message = commit.msg
        words = message.split(" ")

        if words[0].endswith("ing") or words[0].endswith("ed"):
            # print("Wrong1")
            send -= 0.15
        if words[0][0].islower():
            # print("Wrong2")
            send -= 0.15
        send -= 0.25
        search = True
        for onePart in startingWordsBosnian:
            if onePart in words[0] or onePart.lower() in words[0]:
                if onePart == "Inicijaliz" or onePart == "Refaktor" or onePart == "Promjen" or onePart == "Izmijen" or onePart == "Ažurira":
                    search = False
                send += 0.25
        if words[len(words) - 1].endswith("."):
            # print("Wrong4")
            send -= 0.1
        if len(message) >= 50:
            # print("Wrong5")
            send -= 0.25
        containsFile = False

        for w in words:
            if search:
                if modifiedFilesPerCommit(commit, w):
                    containsFile = True
            else:
                containsFile = True

        if not containsFile:
            # print("Wrong6")
            send -= 0.1

        full += send
        length += 1

    return full / length


def evaluationDMM(repoString):
    rm = Repository(repoString)
    allunit = 0
    allcomplex = 0
    allinterfac = 0
    size = 0
    for commit in rm.traverse_commits():
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

    # dodano kao izjednačavanje ocjenjivanja
    if unitocjena < 0.5:
        unitocjena += 0.25
    if complexocjena < 0.7:
        complexocjena += 0.15

    finalna = (unitocjena + complexocjena + interocjena) / 3
    return finalna


if __name__ == '__main__':
    send = ""
    if len(sys.argv) == 3:
        send = sys.argv[2]
    getAllRepositories(sys.argv[1], send)
