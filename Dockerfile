FROM python
WORKDIR /usr/src/app
COPY ./ .
ENV ENVIRONMENT=prod
RUN pip install -r requirements.txt
# waiting for db
CMD sleep 25 && python app.py
EXPOSE 5001
