# bom-squad

# CAPSTONE Project for BOM Squad

## [ ----- GETTING STARTED ----- ]

For setting up your local repository and environment for the first time, follow the instructions below:
---

1. **Clone the repository** into your local project folder:  
    * >git clone [GITHUB](https://github.com/marlonlewis2020/bom-squad.git "Repository")


2. **CD into the cloned repo**:
    * `cd bom-squad`


3. **Create your venv**:
    * create venv (option 1): 
        * `python3 -m venv venv`
    * create venv (Python 3.4 and higher): 
        * `python -m venv venv`
4. **Activate your virtual environment**:
    * activate venv (WINDOWS): 
        * `.\venv\Scripts\activate`
    * activate venv (MAC): 
        * `source myvenv/bin/activate`
5. **Install the requirements**:
    `pip install -r requirements.txt`
6. **checkout the develop branch**: 
    * `git checkout develop`
    * Set upstream remote branch: 
        * `git push -u origin develop`

7. **Set Environmental path variable** so the project modules can be found and accessed:

    * Right click on This PC (My Computer)

    * Then select, Properties > Advanced System Settings > Environment Variables >

    * Add "C:\Python310" to the path variable 
        * (or it may be "C:\Python27", etc. In your C drive look for the Python folder name)

        * OR, Under system variables, create a new Variable called "PythonPath"
        
        * In this variable put 
            >C:\Python27\Lib;C:\Python27\DLLs;C:\Python27\Lib\lib-tk;C:\path\to\project\root\folder”

8. **Create the Databases** in the environment you are connected to: 
    * In terminal, type "flask shell"
    * In the flask shell, type `db.create_all()`
    * type `exit()` to leave flask shell

9. **Setup .env file**
    * copy the contents of the .env.example file

    * create a new file in the "bom-squad/app" directory and name it .env

    * paste the contents from the .env.example file you copied

    * Generate a secret key using any available method, or open a python shell and run the following code:
    ```Python
    import secrets
    print(secrets.token_hex())
    ```

    * copy the secret code generated and paste it as the value for the SECRET_KEY variable in your newly created .env file
***

## [ ----- DEVELOPING CODE ----- ]

**Git WorkFlow**

When implementing/creating a new feature/requirement, use the following git command in terminal when in the local repo folder:

1. (a) git flow feature start <<branch_name>>
   i.e. `git flow feature start BOM-1`
2. `git pull`

3. Edit the correct section of the app with your code
***




## [ ----- ADDING COMPLETED CODE ----- ]

When completed a feature implementation, use the following git command in terminal when in the local repo folder:

1. (a) git flow feature publish <<branch_name>>
    * `git flow feature publish BOM-1`

2. Make NO further changes, commits or pushes to the branch.

3. Checkout to master: 
    * `git checkout master`

4. Delete your local branch: 
    * `git branch -d BOM-1`

5. Create Pull Request: Go to github, go to your branch and click on pull requests

6. Ensure "compare" is set to your branch and click on "New pull request"

7. Review changes and click "Create pull request"

8. Add a short comment and click "Create pull request"

***

## [ ----- ENVIRONMENT DEPENDENCIES ----- ]
1. Python 3.10.7
2. MySQL Workbench 8.0
3. XAMPP 8.2.0

[XAMPP 8.2.0](https://www.apachefriends.org/download.html?/ "XAMPP Download link") includes:
* Apache 2.4.54
* MariaDB 10.4.27
* PHP 8.2.0
* phpMyAdmin 5.2.0
* OpenSSL 1.1.1
* XAMPP Control Panel 3.2.4
* Webalizer 2.23-04
* Mercury Mail Transport System 4.63
* FileZilla FTP Server 0.9.41
* Tomcat 8.5.78 (with mod_proxy_ajp as connector)
* Strawberry Perl 5.32.1.1 Portable

