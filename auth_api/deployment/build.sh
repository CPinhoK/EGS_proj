sudo docker build -t registry.deti:5000/hugom/auth-app:test -f Dockerfile.app .
sudo docker build -t registry.deti:5000/hugom/nginx-proxy -f Dockerfile.nginx .
