FROM python:3.12.1-slim-bookworm

COPY requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt

WORKDIR /app

COPY ./src /app

# to be passed either of the following from k8s definition
# CMD ["python", "producer.py"]
# CMD ["python", "consumer.py"]
