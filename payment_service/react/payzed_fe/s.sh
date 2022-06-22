sudo docker build -t registry.deti:5000/zppinho/preact:latest -f deploy/Dockerfile .

sudo docker push registry.deti:5000/zppinho/preact:latest

kubectl delete -f react-deployment.yaml 

kubectl apply -f react-deployment.yaml 

