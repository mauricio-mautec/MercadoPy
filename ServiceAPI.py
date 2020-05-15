import time
import random
from   pathlib import Path
import pika
import json
import importlib
from   importlib import util
import unicodedata
import sys, os
from   utility import *

def Log(message):
    sendLog('ServiceApi', message)

def Api(ch, method, properties, data):
    npid = os.fork()
    if npid != 0:
        return

    if len(data.strip()) == 0:
        Log("NO JSON")
        sys.exit(0)

    # CLEAN DATA
    result  = cleanData(data)

    # CHECK API FORMAT
    data, checked = checkedApiJSON(result)
    if not checked:
        sys.exit(0)

    Param           = data['Api']['Param']                 # JSON string: {'Login': 'user', 'Password': 'encoded secret'}
    cltIP           = '127.0.0.1'                          # client IP addr
    Param['__IP__'] = cltIP                                # Add IP to Param
    ApiReq          = data['Api']['Name'].split('.')       # nome do recurso em api/<recurso>
    Api             = ApiReq[0].capitalize()               # nome do arquivo py api/<recurso>/<Recurso.py>
    modName         = "api.{}.{}".format(ApiReq[0], Api)   # api.autenticador.Autenticador exemplo para o caso de autenticador
    clsName         = ApiReq[1]                            # nome da classe em Autenticador.py

    # CHECK REQUESTED MODULE AND CLASS
    if checkedRequest(modName, clsName):
        sys.exit(0)

    modObj    = importlib.import_module(modName)            # import das classes disponiveis no recurso
    modClass  = getattr(modObj, clsName)                    # utiliza classe solicitada, no caso  Login
    modInst   = modClass(Param)                             # instancia de Login passando metodo e JSON de parametros
    
    # VERIFY EXECUTE METHOD
    if not hasattr(modInst, 'Execute'):
        message = (f"{modObj} does not have Execute()")
        Log(message)
        sys.exit(0)

    # EXECUTE METHOD EXECUTE
    message = (f"Served {ApiReq[1]}")
    Log(message)
    result  = modInst.Execute()                            # Metodo comum a todas as classes analisa JSON e processa
    
    # SEND RESPONSE
    Result = f"{result}"
    sendMessage(data['Rsp'], Result)
    sys.exit(0)

def checkedRequest(modName, className):       
    try:
        myapi = importlib.util.find_spec(modName)
    
    except:
        message = ("Module Api not found")
        Log(message)
        return False
        
    modObj = importlib.import_module(modName)              # import das classes disponiveis no recurso
    if not hasattr(modObj, className):
        message = (f"{modObj} does not have {className}")
        Log(message)
        return False

def checkedApiJSON(result):
    # VERIFICA QUALIDADE JSON
    try:
        data = json.loads(result)                              # ENCODED JSON STRING TO PYTHON DATA
    except:
        message = ("Incorrect JSON format")
        Log(message)
        return (result, False)

    if type(data) is not dict:
        message = ("Wrong object type")
        Log(message)
        return (result, False)

    if 'Api' not in list(data.keys()):
        message = ("Api not present")
        Log(message)
        return (result, False)

    if 'Rsp' not in list(data.keys()):
        message = ("Rsp not present")
        Log(message)
        return (result, False)
    
    if 'Name' not in list(data['Api'].keys()):
        message = ("Api.Name not present")
        Log(message)
        return (result, False)

    if 'Param' not in list(data['Api'].keys()):
        message = ("Api.Param not present")
        Log(message)
        return (result, False)

    return (data, True)


connectURL   = konstantes('PIKA', 'url')
exchange     = konstantes('PIKA', 'exchange_direct')
queue        = konstantes('PIKA', 'queue')
parametros   = pika.URLParameters(connectURL)
connect      = pika.BlockingConnection(parametros)
channel      = connect.channel()
channel.exchange_declare(exchange=exchange, exchange_type='direct')
channel.queue_declare(queue = queue)
channel.queue_bind(exchange=exchange, queue=queue)

channel.basic_consume(queue, on_message_callback=Api, auto_ack=True, exclusive=False)
info = ('[*] Waiting for messages')
print(info)
Log(info)
channel.start_consuming()

