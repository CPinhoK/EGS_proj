docker build -t registry.deti:5000/hugom/auth-db:latest -f Dockerfile.db --no-cache .

docker push registry.deti:5000/hugom/auth-db:latest
