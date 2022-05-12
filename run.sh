# !/bin/bash


docker build . -t storage-service
docker run -it -p 5001:5001 -e ENVIRONMENT=prod -v ./storage:/usr/src/app/storage -v ./logs:/usr/src/app/logs storage-service
