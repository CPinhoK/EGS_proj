kubectl delete -f db-deployment.yaml

kubectl delete -f storage.yaml

kubectl delete -f mysql-secret.yaml

kubectl apply -f mysql-secret.yaml

kubectl apply -f storage.yaml

kubectl apply -f db-deployment.yaml
