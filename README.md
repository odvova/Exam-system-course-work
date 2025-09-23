# Online Examination System
Online Examination System in Django

LINK: https://exam-system-odvova-dd6d748d9ba5.herokuapp.com/
## Getting started
### Requirements
 - Python 3.6+
 - PIP
 - venv

### Installation
```
# Clone the repository
git clone https://github.com/odvova/Exam-system-course-work.git

# Enter into the directory
cd Exam-system-course-work/

# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Install the dependencies
pip install -r requirements.txt

# Apply migrations.
python manage.py migrate
```
### Configuration
Create `.env` file in cwd and add the following
```
SECRET_KEY=''
DEBUG=True

EMAIL_USER=''
EMAIL_PASS=''
```
### Starting the application
```
python manage.py runserver
```


