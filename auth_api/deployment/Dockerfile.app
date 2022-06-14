FROM python:3.8-alpine

RUN mkdir /auth_app

RUN mkdir /auth_app/templates

WORKDIR /auth_app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY auth.py auth.py

COPY templates/ templates/

ENTRYPOINT ["python3" , "auth.py"]
