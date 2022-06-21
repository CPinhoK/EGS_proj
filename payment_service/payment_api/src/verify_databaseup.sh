#!/bin/bash
count=0
nc -z -w 1 paymentapi-db 3306

while [ ! $count -eq 3 ]
do 
  nc -z -w 1 paymentapi-db 3306  
  if [ ! $? -eq 0 ]
  then
    echo "counting up"
    count=$(( $count + 1 ))
  else
    #echo "reseting counter"
    count=0
  fi
  sleep 3
  #echo $count
done 

x=$(top -n 1 | grep uvicorn)
xdiv=$( echo $x | cut -d " " -f 1)

kill -9 $xdiv

echo $$

sleep 1

kill -9 $$  #not very elegant because this simply restarts the container