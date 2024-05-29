FROM python:3.9

WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt --no-cache-dir
RUN pip install gunicorn==20.1.0
RUN apt-get update && apt-get install -y ncat