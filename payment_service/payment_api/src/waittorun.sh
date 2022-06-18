#!/bin/bash

echo "Waiting for database to launch on 3306..."

nc -z -w 1 paymentapi-db 3306

while [ ! $? -eq 0 ]
do
  sleep 1
  echo $? | nc -z -w 1 paymentapi-db 3306
done

sleep 3
echo "Database launched"

nohup uvicorn main:app --host 0.0.0.0 & nohup sh verify_databaseup.sh