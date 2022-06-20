docker build -t registry.deti:5000/hugom/auth-api:latest -f Dockerfile.app --no-cache .

docker push registry.deti:5000/hugom/auth-api:latest
