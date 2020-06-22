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

def cleanData (data):
    data    = data.strip()
    data    = data.decode('UTF-8')
    dataCls = unicodedata.normalize('NFD', data)
    result  = dataCls.encode('ascii', 'ignore').decode('ascii')
    return result

def sendMessage(queue, message, exch_type = 'direct'):
    connectURL   = konstantes('PIKA', 'url')
    parametros   = pika.URLParameters(connectURL)
    connect      = pika.BlockingConnection(parametros)
    channel      = connect.channel()

    if exch_type == 'direct':
        exchange = konstantes('PIKA', 'exchange_direct')
        channel.queue_declare (queue = queue)
        channel.exchange_declare (exchange=exchange, exchange_type='direct')
        channel.queue_bind       (exchange=exchange, queue=queue)
        channel.basic_publish    (exchange=exchange, routing_key=queue, body=message)
    else:    
        exchange = konstantes('PIKA', 'exchange_fanout')
        channel.exchange_declare (exchange=exchange, exchange_type='fanout')
        channel.basic_publish    (exchange=exchange, routing_key='', body=message)
        

def getOneMessage (exchange, queue):
    connectURL   = konstantes('PIKA', 'url')
    parametros   = pika.URLParameters(connectURL)
    connect      = pika.BlockingConnection(parametros)
    channel      = connect.channel()
    if queue == None:
        result     = channel.queue_declare (queue = '', exclusive=True)
        queue_name = result.method.queue
    else:
        queue_name = queue
    channel.queue_bind (exchange=exchange, queue=queue_name)
    method_frame, header_frame, body = channel.basic_get(queue = queue_name)        
    if  (not hasattr(method_frame, 'NAME'))  or method_frame.NAME == 'Basic.GetEmpty':
        connect.close()
        return '{}'
    else:            
        channel.basic_ack(delivery_tag=method_frame.delivery_tag)
        connect.close() 
        return body

def sendLog(api, message):
    data = {  "Api" : api, "Result" : message }
    jmsg = json.dumps(data)
    sendMessage('', jmsg, "fanout")

def getTokenData(Param):
    hugekey = konstantes('TOKEN', 'hugekey')
    maxage  = int (konstantes('TOKEN', 'maxage'))
    Sessao  = Param['Token']
    # TOKEN ASSINADO COM VALORES DE SESSAO
    slrz    = Serializer(hugekey)
    try:
        Token  = slrz.loads(Sessao)
        # This payload is decoded and safe
    except BadSignature as e:
        return (0, 0, 0, 0, 0)

    return (Token['Sistema'], Token['AuthID'], Token['UserID'], Token['__IP__'], maxage)

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
        return (False, msgError, 0, 0)

    st        = TimestampSigner (timekey)
    val       = Param['Validade']
    Sistema   = val

    if not st.validate(Sistema, max_age = maxage):
        msgError = '{"Api":"utility.testToken", "Result":"EXPIRED"}'
        return (False, msgError, 0, 0)

    if not Token['__IP__'] == Param['__IP__']:
        msgError = '{"Api":"utility.testToken", "Result":"BAD IP"}'
        return (False, msgError, 0, 0)

    return (True, '{"Api":"utility.testToken", "Result":"OK"}', Token['AuthID'], Token['Sistema'])

class TestAPI():
    Auth     = False    
    Token    = ''
    Validade = '' 
    Message  = {}
    def __init__(self, apiname):
        queueid          = uuid.uuid4()
        self.ApiName     = apiname
        self.clientQueue = queueid.hex
        self.connectURL  = konstantes('PIKA', 'url')
        self.exchange    = konstantes('PIKA', 'exchange_direct')
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

        if self.Auth and ('Token' in data) and ('Validade' in data):
            pprint.pprint(data)
            self.Message['Api']['Param']['Token']    = data['Token']   
            self.Message['Api']['Param']['Validade'] = data['Validade']   
            print ("TOKEN E VALIDADE ATUALIZADOS")
            

    def startConsuming (self, callBackFunc):    
        self.connect = pika.BlockingConnection(self.parametros)
        self.channel = self.connect.channel()
        self.channel.exchange_declare (exchange = self.exchange, exchange_type = 'direct')
        self.channel.queue_declare    (queue = self.clientQueue)
        self.channel.queue_bind       (exchange = self.exchange, queue = self.clientQueue)
        self.channel.basic_consume(self.clientQueue, on_message_callback=callBackFunc, auto_ack=True, exclusive=True)
        print(f'[{self.clientQueue}]')
        self.channel.start_consuming()

    def sendMessageToQueue (self, queue):    
        self.Message['Rsp'] = self.clientQueue
        if self.Auth:
            if 'Param' not in self.Message['Api'].keys():
                self.Message['Api']['Param'] = {} 
            
            self.Message['Api']['Param']['Token']    = self.Token   
            self.Message['Api']['Param']['Validade'] = self.Validade   

        message = json.dumps(self.Message)
        sendMessage(queue, message)

    def clrAuthorization(self):
        self.Auth     = False
        self.Token    = ''
        self.Validade = ''

    def setAuthorizationWith (self, token, validate):
        self.Token    = token
        self.Validade = validate
        self.Auth     = True

    def showMessage (self, what):
        sendLog(self.ApiName, what)


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
