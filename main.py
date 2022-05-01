from git import InvalidGitRepositoryError
from pydriller import *
import os
import sys


def getAllRepositories(stringFolder, language):
    if language == "" or language is None:
        language = "-e"
    if not language == "-e" and not language == "-b":
        print("The chosen language is not supported by RepositoryDriller. Please use -e for English or -b for Bosnian.")
        print("The default language is English if you don't send that parameter.")
        return

    # Windows fix for forward-slash symbol
    stringFolder = stringFolder.replace("\\", "/")
    stringFolder = stringFolder.replace("\\\\", "/")

    my_list = os.listdir(stringFolder)

    urls = []
    for f in my_list:
        urls.append(stringFolder + "/" + f)

    for rep in urls:
        try:  # not a Git Repository
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
                    os.path.join(os.path.expanduser('~'), 'Desktop', 'results.txt'), 'a+',  encoding="utf-8"
            ) as f:
                # DMM evaluation taken for 20% of the final grade
                f.write(rep + "," + author + "," + str(eComm * 0.8 + eDMM * 0.2) + "\r\n")
            f.close()
        except InvalidGitRepositoryError:
            print("Not a Git repository")


def modifiedFilesPerCommit(commit, stringFileName):
    for f in commit.modified_files:
        if ".xml" or ".fxml" in f.filename:
            if commit.modified_files != 1 and f.change_type == ModificationType.ADD:
                return True
        if len(f.changed_methods) == 1:
            return True
        if f.filename == stringFileName:
            if f.nloc is not None and f.nloc > 2:
                return True

    return False


def commitMessageBoth(message, bosnian):
    words = message.split(" ")
    evaluation = 0
    if words[0][0].islower():
        evaluation -= 0.15
        if bosnian:
            evaluation -= 0.1
    if words[len(words) - 1].endswith("."):
        evaluation -= 0.1
        if bosnian:
            evaluation -= 0.1
    if len(message) >= 50:
        evaluation -= 0.25
    return evaluation


def englishCommit(repoString):
    fullEvaluation = 0
    numberOfCommits = 0
    startingWords = ["Initial", "Create", "Fix", "Add", "Remove", "Change", "Clear", "Initialize", "Merge", "Submit",
                     "Handle", "Update", "Set", "Move", "Force", "Expand", "Edit", "Check", "Modify", "Bump",
                     "Refactor"]

    commits = Repository(repoString).traverse_commits()
    for commit in commits:
        evaluation = 1
        message = commit.msg
        words = message.split(" ")

        # Rules for evaluation
        if words[0].endswith("ing") or words[0].endswith("ed"):
            evaluation -= 0.15
        if not words[0] in startingWords:
            evaluation -= 0.25
            if words[0][0].islower():
                evaluation += 0.1
        evaluation += commitMessageBoth(message, False)
        containsFile = False

        for w in words:
            if w != "Initial" and w != "Refactor" and w != "Change" and w != "Edit" and w != "Modify":
                if modifiedFilesPerCommit(commit, w):
                    containsFile = True
            else:
                containsFile = True

        if not containsFile:
            evaluation -= 0.1

        fullEvaluation += evaluation
        numberOfCommits += 1

    return fullEvaluation / numberOfCommits


def bosnianCommit(repoString):
    fullEvaluation = 0
    numberOfCommits = 0

    startingWordsBosnian = ["Dodan", "Promjen", "Isprav", "Reorganiz", "Zavrsen", "Inicijaliz",
                            "Spoj", "Preda", "Obrad", "Ažurira", "Postav", "Pomjer", "Forsir", "Prošir", "Ured",
                            "Izmijen",
                            "Refaktor", "Kreira", "Uklon", "Initial"]

    commits = Repository(repoString).traverse_commits()
    for commit in commits:
        evaluation = 1
        message = commit.msg
        words = message.split(" ")

        # Rules for evaluation
        evaluation -= 0.2
        search = True
        for onePart in startingWordsBosnian:
            if onePart in words[0] or onePart.lower() in words[0]:
                if onePart == "Inicijaliz" or onePart == "Refaktor" or onePart == "Promjen" or onePart == "Izmijen" or onePart == "Ažurira" or onePart == "Initial":
                    search = False
                evaluation += 0.2
        evaluation += commitMessageBoth(message, True)
        containsFile = False

        for w in words:
            if search:
                if modifiedFilesPerCommit(commit, w):
                    containsFile = True
            else:
                containsFile = True

        if not containsFile:
            evaluation -= 0.1

        fullEvaluation += evaluation
        numberOfCommits += 1

    return fullEvaluation / numberOfCommits


def evaluationDMM(repoString):
    rm = Repository(repoString)
    allUnitEval = 0
    allComplexityEval = 0
    allInterfaceEval = 0
    size = 0

    for commit in rm.traverse_commits():
        size += 1
        if commit.dmm_unit_size is not None:
            allUnitEval += commit.dmm_unit_size
        if commit.dmm_unit_complexity is not None:
            allComplexityEval += commit.dmm_unit_complexity
        if commit.dmm_unit_interfacing is not None:
            allInterfaceEval += commit.dmm_unit_interfacing

    unitEval = allUnitEval / size
    complexityEval = allComplexityEval / size
    interfaceEval = allInterfaceEval / size

    # More realistic evaluation
    if unitEval < 0.5:
        unitEval += 0.25
    if complexityEval < 0.7:
        complexityEval += 0.15

    finalEvaluationDMM = (unitEval + complexityEval + interfaceEval) / 3
    return finalEvaluationDMM


if __name__ == '__main__':
    secondParameter = ""
    if len(sys.argv) == 3:
        secondParameter = sys.argv[2]
    getAllRepositories(sys.argv[1], secondParameter)
