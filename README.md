# modbus-py-client

A lightweight application that allows control of a Zerova charger with Modbus.

The backend is built on the pymodbus library, and can be used as a library for other projects.

The frontend will be either PyQT or React.



## Dependencies notes

 - https://www.minitool.com/news/pip-uninstall.html

## pyqt note
 - pyqt6-tools only allow python 3.5 -3.9   https://pypi.org/project/pyqt6-tools/#installation
 - To open the QT GUI designer, run command `pyqt6-tools designer`, then select or create a .ui file

## github
### Recommended Steps for push:
Create and switch to the new branch:

 - `git checkout -b new-branch-name`: create a new branch if needed
 - `git add .`
 - `git commit -m "Descriptive commit message"`
 - `git push origin new-branch-name`

### Recommended Steps for updating code from remote to local repo using rebase:
 - `git fetch origin`: Get the latest changes from the remote
 - `git checkout B`: Switch to the local branch B if needed
 - `git rebase origin/A`: apply the changes from remote branch A on top of the current changes in local branch B

 - `git rebase --continue`: During a rebase, if there are conflicts, Git will pause and ask you to resolve them. After resolving conflicts, continue the rebase process
 - `git rebase --abort`: abort the rebase in case something goes wrong