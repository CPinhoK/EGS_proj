#!/bin/bash

echo "Waiting for database to launch on 3306..."

nc -z db 3306

while [ $? -eq 0 ]
do
  sleep 0.1
  nc -z db; echo $? 
done

sleep 3
echo "Database launched"

uvicorn main:app --host 0.0.0.0