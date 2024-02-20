import os
import pika
import time

from common import ensure_channel


queue_name = os.getenv('RABBITMQ_QUEUE_NAME', 'ha-test-queue')
channel = ensure_channel(queue_name)

process_delay_in_milli_seconds = int(
    os.getenv('PROCESS_DELAY_IN_MILLI_SECONDS', 10))


def receive_and_ack_message(ch, method, properties, body):
    print(" [x] received --> %r" % body, end='')
    time.sleep(process_delay_in_milli_seconds / 1000.0)
    # Acknowledge that the message has been received
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print(" --> done")


print(' [!] waiting for messages. To exit press CTRL+C')

while True:
    try:
        print(" [!] starting to consume")
        for method, properties, body in channel.consume(queue_name, auto_ack=False, inactivity_timeout=1):
            if method is not None:
                receive_and_ack_message(channel, method, properties, body)
            else:
                print(" [!] no message, waiting for more")
                channel = ensure_channel(queue_name)

    except KeyboardInterrupt:
        break
    except (pika.exceptions.ConnectionClosedByBroker, pika.exceptions.StreamLostError, pika.exceptions.ChannelClosedByBroker) as conn_closed:
        print(f" [!] connection closed by broker, trying to re-connect")

        channel = ensure_channel(queue_name)

        print(' [!] re-connected')
