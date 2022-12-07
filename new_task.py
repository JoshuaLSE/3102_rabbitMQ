"""
Test Scripts
User will run the script in python to load the rabbitMQ queues

The database shall preload with a set of 1000 items.

1) Which Queue do they want to load?
2) How many queue items do they want to load?
3) What are the sort of queue items they want to load?
"""
import random
import pika

"""
Get User Input
"""

queueTxt = "Which queue? "
itemsTxt = "How many queue items? "
randRangeTxt = "Range for randomisation? "

queue = input(queueTxt)
items = input(itemsTxt)
randRange = input(randRangeTxt)

if queue.isdigit() or items.isalpha() or randRange.isalpha():
    print("Queue must be alphabetical, Items & Random Range must be digit")
    exit(1)

items = int(items)  # This might be read from a file instead
randRange = int(randRange)

"""
Connecting to RabbitMQ
"""

try:
    # Queue Declaration
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()


    def publish_message(queueName, message):
        """
        Publishes message to destined queueName with message
        """
        channel.basic_publish(
            exchange='',  # This publishes the thing to a default exchange
            routing_key=queueName,
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ))
        print(" [x] Sent %r" % message)
        # connection.close()

except Exception as e:
    txt = "\nYour RabbitMQ server might not be running"
    print(txt.upper())
    exit(2)

"""
Sending Messages
"""

for i in range(items + 1):
    randomNumber = random.randrange(randRange)
    publish_message(queue, str(randomNumber))

"""
Finish Sending
"""

finish = "\nTesting completed for:\nQueue: {}" \
         "\nNumber of Items: {} " \
         "\nRange for Item Randomisation: {}"

print(finish.format(queue, items, randRange))