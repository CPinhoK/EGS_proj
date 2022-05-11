# FRONTEND

This repository contais the code to execute the frontend of EGS store - Eletronic Geek Software Store, a store that manages an online shop of software.

## LOCAL DEPLOYMENT

For test purposes it is possible to run a local deployment:

### Requirements
To install the necessary requirements create a virtual environment and install the necessary requirements:

```bash
pyhton -m venv venv
source venv/bin/activate
cd egs
pip install -r requirements.txt
```


### Run platform
To run the platform start the server. If the port is already in use, use another one (ex: 7000)

```bash
source venv/bin/activate
cd egs
python manage.py makemigrations
python manage.py migrate
python3.8 manage.py runserver 7000
```

### Create Super User
To create a super user run:

```bash
python manage.py createsuperuser
```

# Auhtors:
- Mariana Pinto
