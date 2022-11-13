#!/usr/bin/env python
import pika
import time

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='weewoo', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body.decode())
    time.sleep(body.count(b'.'))
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


# Important information is here: https://www.rabbitmq.com/tutorials/tutorial-two-python.html
channel.basic_qos(prefetch_count=1)  # This will tell the channel to not dispatch it until it has acknowledged
channel.basic_consume(queue='weewoo', on_message_callback=callback)

channel.start_consuming()
