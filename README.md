# EGS_proj

Project for EGS subject at Universidade de Aveiro to deploy a online shop called EGS - Eletronic Geek Software, store that manages an online shop of software.

## FOLDERS

Each folder contains the work of each part of the team that together complete the goal of this project.

### - [auth_api](https://github.com/CPinhoK/EGS_proj/tree/main/auth_api)

This folder contains the code to execute and authentication API

#### Author: Hugo Moinheiro

### - [frontend](https://github.com/CPinhoK/EGS_proj/tree/main/frontend)

This folder contains the code to execute the frontend of EGS store - Eletronic Geek Software Store

#### Author: Mariana Pinto

### - [payment_service](https://github.com/CPinhoK/EGS_proj/tree/main/payment_service)

This folder contains the code to execute the payment API and Payment FrontEnd

#### Author: Paulo Pinho

### - [stock_api](https://github.com/CPinhoK/EGS_proj/tree/main/stock_api)

This folder contains the code to execute the stock API

#### Author: Diogo Batista

## DEPLOYMENT DOCKER
Instructions to build the docker file:

- Build Docker: 
```bash 
sudo docker build -t [namecontainer] -f deploy/Dockerfile . 
```

- Run docker: 
```bash 
sudo docker run -ti --rm [namecontainer]
```

- Run docker on a given port: 
```bash 
sudo docker run -it -rm -p [port] [name container] 
```

- Stop container: 
```bash 
sudo docker stop [idcontainer]
```

- See all containers: 
```bash
sudo docker ps -a
```

- See containers running: 
``` bash
sudo docker ps
```

- Delete a container: 
```bash
sudo docker rm -f [idcontainer]
```

- Delete a image: 
```bash
sudo docker image rm [OPTIONS] IMAGE [IMAGE...]
```

- Prune everything
```bash
sudo docker system prune
```

- Docker-compose build
```bash
sudo docker-compose build --no-cache
```

- Docker-compose Up
```bash
sudo docker-compose up -d
```

- Docker-compose Down
```bash
sudo docker-compose down
```

- Docker-compose logs
```bash
sudo docker-compose logs
```

## Kubernetes instructions
Instructions for kubernetes:

- Create namespace
```bash
kubectl create ns [namespace]
```

- Launch deployment
```bash
kubectl apply -f deployment.yaml 
```

- Build docker image
```bash
sudo docker build -t [image_name] .

sudo docker build -t [image_name] -f Dockerfile.app .
```

- Push docker image
```bash
sudo docker push [image_name]
```

- Get pods 
```bash
kubectl get pods -n [namespace]
```

- Enter shell inside pod
```bash
kubectl exec -ti [podname] -n [namespace] --/bin/bash
```
