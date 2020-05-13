import sys, os
sys.path.append('/srv/mautec/www/MercadoPy')
import time
import random
from   pathlib import Path
import pika
import json
import importlib
import unicodedata
import pprint
import uuid
from utility import *

class TestClient():
    Auth     = False    
    Token    = ''
    Validade = '' 
    Message  = {}
    def __init__(self):
        queueid          = uuid.uuid4()
        self.clientQueue = queueid.hex
        self.connectURL  = konstantes('PIKA', 'url')
        self.parametros  = pika.URLParameters(self.connectURL)
        self.connect     = pika.BlockingConnection(self.parametros)
        self.exchange    = 'MercadoServiceAPI'
        self.channel     = '' 
        self.Result      = {}
    
    def getMessage (self, ch, method, properties, data):
        data = data.strip()
        data = data.decode('UTF-8')
        # CLEAN DATA
        dataCls = unicodedata.normalize('NFD', data)
        result  = dataCls.encode('ascii', 'ignore').decode('ascii')
        data = json.loads(result)    
        self.channel.stop_consuming()
        self.channel.queue_delete(queue = self.clientQueue)
        self.channel.close()
        self.connect.close()
        self.Result = data

    def startConsuming (self, callBackFunc):    
        self.connect = pika.BlockingConnection(self.parametros)
        self.channel      = self.connect.channel()
        self.channel.exchange_declare (exchange = self.exchange, exchange_type = 'direct')
        self.channel.queue_declare    (queue = self.clientQueue)
        self.channel.queue_bind       (exchange = self.exchange, queue = self.clientQueue)
        self.channel.basic_consume(self.clientQueue, on_message_callback=callBackFunc, auto_ack=True, exclusive=True)
        print(f'[*] Waiting for messages from {self.clientQueue}')
        self.channel.start_consuming()

    def sendMessageToQueue (self, queue):    
        self.Message['Rsp'] = self.clientQueue
        if self.Auth:
            Param = { 'Token' : self.Token, 'Validade' : self.Validade }
            self.Message['Api']['Param'] = Param
            
        self.showMessage(self.Message)
        message = json.dumps(self.Message)
        self.connect = pika.BlockingConnection (self.parametros)
        self.channel = self.connect.channel()
        self.channel.exchange_declare (exchange = self.exchange, exchange_type = 'direct')
        self.channel.queue_declare    (queue = queue)
        self.channel.queue_bind       (exchange = self.exchange, queue = queue)
        self.channel.basic_publish    (exchange = self.exchange, routing_key=queue, body=message)

    def setAuthorizationWith (self, token, validate):
        self.Token    = token
        self.Validade = validate
        self.Auth     = True

    def showMessage (self, what):
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(what)

queue = konstantes('PIKA', 'queue')

# ENVIO DO LOGIN/PASSWORD E RECOLHA DO TOKEN PARA FUTUROS ACESSOS E CONFIGURACAO CANAL RSP
Appid   = {"Name" : "hudflutter", "Version" : "text da versao", "Appsys": "win64, android, iphone" }
Param   = {"Login": "sergio.moreira@gmail.com","Password": "veiM4biu","Sistema" : 2, "Appid": Appid }
Api     = {"Name": "autenticador.Token", "Param": Param}
tC = TestClient() 
tC.Message["Api"] =  Api
print("MENSAGEM DE LOGIN:")
tC.sendMessageToQueue(queue);
tC.startConsuming(tC.getMessage)
tC.showMessage(tC.Result)
if 'Token' in tC.Result.keys():
    tC.setAuthorizationWith(tC.Result['Token'], tC.Result['Validade'])
else:
    print("TOKEN NAO RECEBIDO")
    sys.exit(0)

# TESTE DO ENVIO DO TOKEN PARA VALIDACAO
Api     = {"Name": "autenticador.TokenValidate"}
tC.Message["Api"] =  Api
print(f"\n\nMENSAGEM ENVIADA AUTORIZACAO VALIDA:")
tC.sendMessageToQueue(queue);
tC.startConsuming(tC.getMessage)
tC.showMessage(tC.Result)

sys.exit(0)

# TESTE DO ENVIO DO TOKEN PARA VALIDACAO TOKEN EXPIRADO
import time
time.sleep(20)
Api     = {"Name": "autenticador.TokenValidate"}
tC.Message["Api"] =  Api
print(f"\n\nMENSAGEM ENVIADA AUTORIZACAO TOKEN EXPIRADO:")
tC.sendMessageToQueue(queue);
tC.startConsuming(tC.getMessage)
tC.showMessage(tC.Result)
