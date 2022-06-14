sudo docker build -t registry.deti:5000/hugom/auth-app:v3 -f Dockerfile.app .
sudo docker build -t registry.deti:5000/hugom/nginx-proxy -f Dockerfile.nginx .
sudo docker push registry.deti:5000/hugom/auth-app:v3
sudo docker push registry.deti:5000/hugom/nginx-proxy
