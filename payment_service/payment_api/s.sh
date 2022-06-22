sudo docker build -t registry.deti:5000/zppinho/papi:latest -f deploy/Dockerfile .

sudo docker push registry.deti:5000/zppinho/papi:latest

kubectl delete -f deployment.yaml 

kubectl apply -f deployment.yaml 

