import pika
import sqlite3
from   utility import *
import pprint
import sys, os, signal

def callback(ch, method, properties, body):
    result = cleanData(body)
#    rsldata = json.loads(result)
#    pprint.pprint(rsldata)
#    print('----------------------------------------------------------------------\n')
    database = konstantes('LOGDB', 'database')
    con      = sqlite3.connect (database)
    cur      = con.cursor()
    stmt     = 'insert into servicelog(log) values (?)'
    cur.execute (stmt, (result,))
    con.commit()

def handleSIGCHLD(param1, param2):
    os.waitpid(-1, os.WNOHANG)

npid = os.fork()
if npid != 0:
    sys.exit(0)

signal.signal(signal.SIGCHLD, handleSIGCHLD)
connectURL   = konstantes('PIKA', 'url')

parametros   = pika.URLParameters(connectURL)
connect      = pika.BlockingConnection(parametros)
channel      = connect.channel()
exchange     = konstantes('PIKA', 'exchange_fanout')

channel.exchange_declare(exchange=exchange, exchange_type='fanout')

result      = channel.queue_declare(queue='', exclusive=True)
queue_name  = result.method.queue

channel.queue_bind(exchange=exchange, queue=queue_name)

print(' [*] Waiting for logs.')

channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
channel.start_consuming()
