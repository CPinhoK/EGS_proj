FROM python:3.10-alpine

MAINTAINER Mariana Pinto

RUN mkdir /frontend
RUN mkdir /frontend/www

WORKDIR /frontend

COPY deployment/requirements.txt /frontend

RUN pip install -r requirements.txt

COPY egs /frontend/

EXPOSE 8000/tcp

VOLUME /frontend/www

CMD ["python", "manage.py", "runserver", "0.0.0.0:7000"]
