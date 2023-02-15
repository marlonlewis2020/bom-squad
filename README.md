# bom-squad
CAPSTONE Project for BOM Squad



{ ----- GETTING STARTED ----- ]
For setting up your local repository and envrionment for the first time, follow the instructions below:
1. clone the repository into your local project folder: "git clone https://github.com/marlonlewis2020/bom-squad.git"
2. cd into the cloned repo
3. Create your venv

    To Create your virtual environment:
    create venv (option 1): python3 -m venv venv
    create venv (Python 3.4 and higher): python -m venv venv

    Activate your virtual environment:
    activate venv (WINDOWS): .\venv\Scripts\activate
    activate venv (MAC): source myvenv/bin/activate

4. Install the requirements:
    pip install -r requirements.txt

5. checkout the develop branch: "git checkout develop"
6. Set upstream remote branch: "git push -u origin develop"




[ ----- DEVELOPING CODE ----- ]
When implementing/creating a new feature/requirement, use the following git command in terminal when in the local repo folder:
1. (a) git flow feature start <<branch_name>> 
    i.e. "git flow feature start BOM-1"
2. git pull

3. Edit the correct section of the app with your code




[ ----- ADDING COMPLETED CODE ----- ]
When completed a feature implementation, use the following git command in terminal when in the local repo folder:
1. (a) git flow feature publish <<branch_name>>
    i.e. "git flow feature publish BOM-1"

2. Make NO further changes, commits or pushes to the branch.

3. Checkout to master: "git checkout master"

4. Delete your local branch: git branch -d <<branch_name>> 

5. Create Pull Request: Go to github, go to your branch and click on pull requests

6. Ensure "compare" is set to your branch and click on "New pull request"

7. Review changes and click "Create pull request"

8. Add a short comment and click "Create pull request"



[ ----- ENVIRONMENT DEPENDENCIES ----- ]
Python 3.10.7
MySQL Workbench 8.0
XAMPP 8.2.0

XAMPP 8.2.0 (https://www.apachefriends.org/download.html?/) includes:
    Apache 2.4.54
    MariaDB 10.4.27
    PHP 8.2.0
    phpMyAdmin 5.2.0
    OpenSSL 1.1.1
    XAMPP Control Panel 3.2.4
    Webalizer 2.23-04
    Mercury Mail Transport System 4.63
    FileZilla FTP Server 0.9.41
    Tomcat 8.5.78 (with mod_proxy_ajp as connector)
    Strawberry Perl 5.32.1.1 Portable
