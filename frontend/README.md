To deploy the djando project:

install requirements.txt

create environment: python3.8 -m venv venv

enter the environment: source venv/bin/activate

enter the project: cd egs

run migrations: python3.8 manage.py migrate

create superuser: python 3.8 manage.py createsuperuser

run server: python3.8 manage.py runserver

