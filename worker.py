#!/usr/bin/env python
import pika
import time

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))

channel = connection.channel()
channel.queue_declare(queue='task_queue', durable=True)


print(' [*] Waiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body.decode())
    connection2 = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel2 = connection2.channel()
    channel2.queue_declare(queue='weewoo', durable=True)
    message = body.decode() + ' received'
    channel2.basic_publish(
        exchange='',  # This publishes the thing to a default exchange
        routing_key='weewoo',
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
        ))
    connection2.close()
    ch.basic_ack(delivery_tag=method.delivery_tag)


# Important information is here: https://www.rabbitmq.com/tutorials/tutorial-two-python.html
channel.basic_qos(prefetch_count=1)  # This will tell the channel to not dispatch it until it has acknowledged
channel.basic_consume(queue='task_queue', on_message_callback=callback)

channel.start_consuming()
