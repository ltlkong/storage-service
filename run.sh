# !/bin/bash


docker build . -t storage-service
docker run -it -p 5001:5001 -e ENVIRONMENT=prod -v $(pwd)/storage:/usr/src/app/storage -v $(pwd)/logs:/usr/src/app/logs -v $(pwd)/db:/var/lib/mysql storage-service
