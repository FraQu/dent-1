# Dent

## How to setup 
### GNU/Linux 
1. Clone This Project `git clone https://github.com/kasprzykapps/dent.git`
2. Go to Project Directory `cd dent`
3. Create a Virtual Environment `virtualenv venv`
4. Activate Virtual Environment `source venv/bin/activate`
5. Install Requirements Package `pip install -r requirements.txt`
6. Check new migrations `python manage.py makemirations`
7. Migrate website app Database `python manage.py migrate website`
8. Migrate project Database `python manage.py migrate`
9. Create Super User `python manage.py createsuperuser`
10. Finally Run The Project `python manage.py runserver`

### Windows
1. Clone This Project `git clone https://github.com/kasprzykapps/dent.git`
2. Go to Project Directory `cd dent`
3. Create a Virtual Environment `virtualenv venv`
4. Activate Virtual Environment `venv\Scripts\activate`
5. Install Requirements Package `pip install -r requirements.txt`
6. Check new migrations `python manage.py makemirations`
7. Migrate website app Database `python manage.py migrate website`
8. Migrate project Database `python manage.py migrate`
9. Create Super User `python manage.py createsuperuser`
10. Finally Run The Project `python manage.py runserver`