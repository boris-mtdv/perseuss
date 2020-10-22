FROM python:3.8

COPY . /perseuss
WORKDIR /perseuss
RUN pip install -r requirements.txt
EXPOSE 5000
CMD python ./app.py