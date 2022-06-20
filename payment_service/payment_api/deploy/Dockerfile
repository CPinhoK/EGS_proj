from python:3.10-alpine

RUN apk update 
RUN apk add --no-cache mariadb-connector-c-dev
RUN apk add bind-tools 
RUN apk add vim
RUN apk add curl
RUN apk add --no-cache gcc libressl-dev musl-dev libffi-dev py-cryptography


RUN mkdir /app

WORKDIR /app

COPY ./src/requirements.txt /app

RUN pip install -r requirements.txt

COPY ./src/main.py /app

COPY ./src/waittorun.sh /app

COPY ./src/verify_databaseup.sh /app

EXPOSE 8000

EXPOSE 3306

#CMD [ "uvicorn", "main:app" , "--host", "0.0.0.0"]

CMD [ "sh", "waittorun.sh"]