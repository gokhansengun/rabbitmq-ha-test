import os
import pika
import time

from common import ensure_channel


queue_name = os.getenv('RABBITMQ_QUEUE_NAME', 'ha-test-queue')
channel = ensure_channel(queue_name)
index = 0

messages_in_a_second = int(os.getenv('MESSAGES_IN_A_SECOND', 1))

print(" [!] starting to produce")

while True:
    now_str = time.strftime("%Y%m%d-%H%M%S")

    message = f'msg index #{index} - {now_str}'

    try:
        channel.basic_publish(exchange='',
                              routing_key=queue_name,
                              body=message,
                              properties=pika.BasicProperties(
                                  delivery_mode=2,  # make message persistent
                              ))

        index += 1
        print(f" [x] sent - {message}")
    except (pika.exceptions.ConnectionClosedByBroker, pika.exceptions.StreamLostError) as conn_closed:
        print(f" [!] connection closed by broker, trying to re-connect")

        channel = ensure_channel(queue_name)

        continue

    time.sleep(1.0 / messages_in_a_second)
