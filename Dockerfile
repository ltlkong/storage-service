FROM ubuntu:20.04
COPY ./ /usr/src/app
WORKDIR /usr/src/app
RUN apt-get update && apt-get install -y python3-pip mariadb-server libmariadb-dev && pip3 install -r requirements.txt 
ENV ENVIRONMENT=prod
VOLUME [ "/usr/src/app/storage", "/usr/src/app/logs" ]
EXPOSE 5001
CMD service mysql start && mariadb -e "CREATE DATABASE storage;" && python3 app.py
