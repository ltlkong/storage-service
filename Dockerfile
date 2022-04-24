FROM python
WORKDIR /usr/src/app
COPY ./ .
RUN pip install -r requirments.txt
# waiting for db
CMD sleep 25 && python app.py
EXPOSE 5001
