from python:3.10-alpine

RUN mkdir /app

WORKDIR /app

COPY ./src/requirements.txt /app

COPY ./src/waittorun.sh /app

RUN pip install -r requirements.txt

COPY ./src/main.py /app

EXPOSE 8000

#CMD [ "uvicorn", "main:app" , "--host", "0.0.0.0"]
CMD [ "sh", "waittorun.sh"]