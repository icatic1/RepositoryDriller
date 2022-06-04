[![icatic1](https://img.shields.io/badge/Version-v.1.0.0-brightgreen)]()
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-%23FE5196?logo=conventionalcommits&logoColor=white)](https://conventionalcommits.org)
# Repository Driller

A simple Python script for the analysis and evaluation of Git Repositories for best practices in two languages.


### Why should I use this project ?

It makes for a great input in evaluating and grading repositories, both on atommic commits and commit messages.


### Setup

You need `python>3.5` to run this script.

The project depends on the `pydriller` library, install it with pip:
`pip install pydriller`


### How to run?

You can run the script from the command-line using
```
python git_evaluation.py target_folder -e
```
or
```
python git_evaluation.py target_folder -b
```
- target_folder - the folder with cloned repositories
- "-e" / "-b"  - the chosen language (if nothing is sent as this parameter the default language is english)

The output is the `results.txt` file on Desktop which will have the following columns
```
repository_path, author, evaluation
```


### Contributing

You are welcome to contribute to the code via pull requests.  Please have a
look at the [NLeSC
guide](https://nlesc.gitbooks.io/guide/content/software/software_overview.html)
for guidelines about software development.
