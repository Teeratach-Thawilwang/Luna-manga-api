FROM python:3.11.9-slim

EXPOSE 8000

WORKDIR /data/main
COPY . ../

RUN apt-get update && apt-get install -y \
    python3-dev \
    libmagic-dev\
    default-libmysqlclient-dev \
    build-essential && \
    pip3 install --upgrade pip && \
    pip3 install -r requirements.txt --no-cache-dir
