import os
import pika
import time


rabbitmq_host = os.getenv('RABBITMQ_HOST', 'rabbitmq-ha')
rabbitmq_port = os.getenv('RABBITMQ_PORT', 5672)
rabbitmq_user = 'rabbitmq'
rabbitmq_pass = 'rabbitmq'


def ensure_channel(queue_name):
    channel = None
    channel_ok = False

    while not channel_ok:
        try:
            channel = __ensure_channel(queue_name)
            channel_ok = True
        except Exception as e:
            print(f" [!] failed to create channel {e}, will retry in a second")
            time.sleep(1)

    return channel


def __ensure_channel(queue_name):
    credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_pass)
    connection_params = pika.ConnectionParameters(host=rabbitmq_host,
                                                  port=rabbitmq_port,
                                                  credentials=credentials)

    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()

    channel.queue_declare(queue=queue_name, durable=True)

    return channel
