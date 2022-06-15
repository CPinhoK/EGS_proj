FROM python:3.10-alpine

MAINTAINER Diogo Baptista

RUN apk update
RUN apk add --no-cache gcc libressl-dev musl-dev libffi-dev py-cryptography
RUN mkdir /app
RUN mkdir /app/www/

WORKDIR /app

COPY ./src/requirements.txt /app

RUN pip install -r requirements.txt

COPY ./src/main.py /app

EXPOSE 8000/tcp

VOLUME /app/www/

ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0"]