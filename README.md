# Dent

## How to setup 
### GNU/Linux 
1. Clone this project: `git clone https://github.com/kasprzykapps/dent.git`
2. Go to project directory: `cd dent`
3. Create a virtual environment: `virtualenv venv`
4. Activate virtual environment: `source venv/bin/activate`
5. Install requirements package: `pip install -r requirements.txt`
6. Check new migrations: `python manage.py makemirations`
7. Migrate website app database: `python manage.py migrate website`
8. Migrate project database: `python manage.py migrate`
9. Create super user: `python manage.py createsuperuser`
10. Finally run the project: `python manage.py runserver`

### Windows
1. Clone this project: `git clone https://github.com/kasprzykapps/dent.git`
2. Go to project directory: `cd dent`
3. Create a virtual environment: `virtualenv venv`
4. Activate virtual environment: `venv\Scripts\activate`
5. Install requirements package: `pip install -r requirements.txt`
6. Check new migrations: `python manage.py makemirations`
7. Migrate website app database: `python manage.py migrate website`
8. Migrate project database: `python manage.py migrate`
9. Create super user: `python manage.py createsuperuser`
10. Finally run the project: `python manage.py runserver`

##### Troubleshooting
1. Database is not updating: `python manage.py migrate --run-syncdb`