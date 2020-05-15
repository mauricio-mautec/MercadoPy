#!/usr/bin/env python
import pika
from utility import *
import pprint
connectURL   = konstantes('PIKA', 'url')
parametros   = pika.URLParameters(connectURL)
connect      = pika.BlockingConnection(parametros)
channel      = connect.channel()
exchange     = konstantes('PIKA', 'exchange_fanout')

channel.exchange_declare(exchange=exchange, exchange_type='fanout')

result      = channel.queue_declare(queue='', exclusive=True)
queue_name  = result.method.queue

channel.queue_bind(exchange=exchange, queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    result = cleanData(body)
    rsldata = json.loads(result)
    pprint.pprint(rsldata)
    print('----------------------------------------------------------------------\n')
        
        
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
channel.start_consuming()
