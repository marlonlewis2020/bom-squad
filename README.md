# bom-squad
CAPSTONE Project for BOM Squad



{ ----- GETTING STARTED ----- ]
For setting up your local repository and envrionment for the first time, follow the instructions below:
1. clone the repository into your local project folder: "git clone https://github.com/marlonlewis2020/bom-squad.git"
2. cd into the cloned repo
3. Create your venv

    To Create your virtual environment:
    create venv: python3 -m venv venv

    Activate your virtual environment:
    activate venv: .\venv\Scripts\activate

4. Install the requirements:
    pip install -r requirements.txt

5. checkout the develop branch: "git checkout develop"
6. Set upstream remote branch: "git push -u origin develop"




[ ----- DEVELOPING CODE ----- ]
When implementing/creating a new feature/requirement, use either of the 2 git commands in terminal when in the local repo folder:
1. (a) git flow feature start <<branch_name>> 
    i.e. "git flow feature start BOM-1"
or 
   (b) git checkout -b <<branch_name>> develop
    i.e. "git checkout -b BOM-1 develop"

2. git pull

3. Edit the correct section of the app with your code




[ ----- ADDING COMPLETED CODE ----- ]
When completed a feature implementation, use either of the 2 git commands in terminal when in the local repo folder:
1. (a) git flow feature publish <<branch_name>>
    i.e. "git flow feature publish BOM-1"
or
   (b) git push -u <<--up-stream remote branch>>
    i.e. "git push -u origin develop" or "git push"

2. Make NO further changes, commits or pushes to the branch.

3. Checkout to develop: "git checkout master"

4. Delete your local branch: git branch -d <<branch_name>> 

5. Go to github, go to your branch and click on pull requests

6. click on "New pull request"

7. Review changes and click "Create pull request"




