# shared_project
Modern Cryptography Project
The code in this reposiory implements a cryptographically secure and GDPR compliant system for managing a student registration system. The system gathers personal information including information on disabilities
The project requires Python 3 and MongoDB. 
Setting up the project requires the following steps;
1. Set up the python virtual enviornment
python3 -m venv project-venv
source project-venv/bin/activate
2. Install required packages
cd cyber-project
pip3 install -r requirements.txt
3. Create two databases with a collection named users in each:
use cyberStudents;
db.createCollection('users');
use cyberStudentsTest;
db.createCollection('users');
4. Once created the server contains functionality for the following;
    registering new users (api/handlers/registration.py)
    logging in (api/handlers/login.py)
    logging out (api/handlers/logout.py)
    displaying profile (api/handlers/user.py)
