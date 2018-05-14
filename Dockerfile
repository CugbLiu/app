FROM python:2.7-slim
RUN mkdir /app
ADD requirements.txt /app/requirements.txt
WORKDIR /app
RUN apt-get update
RUN pip install -r requirements.txt

