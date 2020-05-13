import configparser
from itsdangerous.serializer import Serializer
from itsdangerous            import TimestampSigner
from itsdangerous.exc import BadSignature, BadData
import pprint 
import unicodedata
import sys, os
import pika
import json
import uuid

def konstantes(name,key):
    arqini     = "/srv/mautec/www/MercadoPy/config.ini"
    config     = configparser.ConfigParser()
    config.read (arqini)
    if name in config:
        Result = config[name][key]
        return Result
    else:
        raise Exception()

def sendMessage(queue, message):
    connectURL   = konstantes('PIKA', 'url')
    exchange     = konstantes('PIKA', 'exchange')
    parametros   = pika.URLParameters(connectURL)
    connect      = pika.BlockingConnection(parametros)
    channel      = connect.channel()
    channel.exchange_declare (exchange=exchange, exchange_type='direct')
    channel.queue_declare    (queue = queue)
    channel.queue_bind       (exchange=exchange, queue=queue)
    channel.basic_publish    (exchange=exchange, routing_key=queue, body=message)

def sendLog(api, message):
    data = {  "Api" : api, "Result" : message }
    jmsg = json.dumps(data)
    sendMessage('LOG', jmsg)

def testToken(Param):       
    hugekey  = konstantes('TOKEN', 'hugekey')
    timekey  = konstantes('TOKEN', 'timekey')
    maxage   = int (konstantes('TOKEN', 'maxage'))

    Sessao  = Param['Token']
    # TOKEN ASSINADO COM VALORES DE SESSAO
    slrz    = Serializer(hugekey)
    try:
        Token  = slrz.loads(Sessao)
        # This payload is decoded and safe
    except BadSignature as e:
        msgError = '{"Api":"utility.testToken", "Result":"BAD TOKEN"}'
        return (False, msgError, 0)

    st        = TimestampSigner (timekey)
    val       = Param['Validade']
    Sistema   = val

    if not st.validate(Sistema, max_age = maxage):
        msgError = '{"Api":"utility.testToken", "Result":"EXPIRED"}'
        return (False, msgError, 0)

    if not Token['__IP__'] == Param['__IP__']:
        msgError = '{"Api":"utility.testToken", "Result":"BAD IP"}'
        return (False, msgError, 0)

    return (True, '{"Api":"utility.testToken", "Result":"OK"}', Token['AuthID'])

class TestAPI():
    Auth     = False    
    Token    = ''
    Validade = '' 
    Message  = {}
    def __init__(self):
        queueid          = uuid.uuid4()
        self.clientQueue = queueid.hex
        self.connectURL  = konstantes('PIKA', 'url')
        self.exchange    = konstantes('PIKA', 'exchange')
        self.parametros  = pika.URLParameters(self.connectURL)
        self.connect     = pika.BlockingConnection(self.parametros)
        self.channel     = '' 
        self.Result      = {}
    
    def getMessage (self, ch, method, properties, data):
        data = data.strip()
        data = data.decode('UTF-8')
        # CLEAN DATA
        dataCls = unicodedata.normalize('NFD', data)
        result  = dataCls.encode('ascii', 'ignore').decode('ascii')
        try:
            data = json.loads(result)    
        except:
            data = {}
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
            if 'Param' not in self.Message['Api'].keys():
                self.Message['Api']['Param'] = {} 
            
            self.Message['Api']['Param']['Token']    = self.Token   
            self.Message['Api']['Param']['Validade'] = self.Validade   

        self.showMessage(self.Message)
        message = json.dumps(self.Message)
        sendMessage(queue, message)

    def setAuthorizationWith (self, token, validate):
        self.Token    = token
        self.Validade = validate
        self.Auth     = True

    def showMessage (self, what):
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(what)


data =  {
            "Api": {
                "Name": "autenticador.Token",
                "Param": {
                    "Login": "sergio.moreira@gmail.com",
                    "Password": "veiM4biu",
                    "Sistema" : 2,
                    "Appid" : { "Name" : "hudflutter", "Version" : "text da versao", "Appsys": "win64, android trálálá, iphone"}
                }
            },
            "Rsp": "answerChannel"
        }
