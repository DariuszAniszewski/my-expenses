FROM python:3.8

WORKDIR /app

ADD requirements.txt /app

RUN pip install -r requirements.txt

ADD . /app

EXPOSE 8000
