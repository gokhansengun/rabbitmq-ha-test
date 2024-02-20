# Getting Started

## Install RabbitMQ

```bash
helm upgrade --install rabbitmq-ha \
  --version 12.11.2 \
  -f yaml/helm/rabbitmq-values.yml \
  oci://registry-1.docker.io/bitnamicharts/rabbitmq
```

## Install Python Producer and Consumer

```bash
kubectl apply -f yaml/deployment
```

## Local Development (Optional)

```bash
cd test-app
python3 -m venv ./venv
source venv/bin/activate
pip install -r requirements.txt
```

### on one terminal
```bash
cd test-app
source venv/bin/activate
python3 src/producer.py
```

### on another terminal
```bash
cd test-app
source venv/bin/activate
python3 src/consumer.py
```
