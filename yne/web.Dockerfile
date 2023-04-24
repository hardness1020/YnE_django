FROM docker.io/library/python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

RUN apt-get update && \
    apt-get install -y wget && \
    curl -o cloud-sql-proxy https://storage.googleapis.com/cloud-sql-connectors/cloud-sql-proxy/v2.2.0/cloud-sql-proxy.linux.amd64 && \
    chmod +x /app/cloud-sql-proxy