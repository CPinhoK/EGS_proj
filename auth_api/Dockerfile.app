FROM python:3.10-alpine

RUN mkdir /auth_app

RUN mkdir /auth_app/templates

RUN apk update
RUN apk add --no-cache gcc libressl-dev musl-dev libffi-dev py-cryptography
RUN apk add curl

WORKDIR /auth_app

COPY requirements.txt /auth_app/requirements.txt

RUN pip install -r /auth_app/requirements.txt

COPY auth.py /auth_app/auth.py

COPY server.crt /auth_app/server.crt

COPY server.key /auth_app/server.key

COPY templates/ /auth_app/templates

EXPOSE 8006

ENTRYPOINT ["python3" , "auth.py"]
