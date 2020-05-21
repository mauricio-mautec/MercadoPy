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
queue = konstantes('PIKA', 'queue')

api   = 'autenticador.testAutenticador'
tC = TestAPI(api) 

def Log (message):
    sendLog (api, message)

#'LOGIN/PASSWORD COM LOGIN INCORRETO'
teste = 'LOGIN/PASSWORD COM LOGIN INCORRETO'
Appid   = {"Name" : "hudflutter", "Version" : "text da versao", "Appsys": "win64, android, iphone" }
Param   = {"Login": "sergxio.moreira@gmail.com","Password": "veiM4biu","Sistema" : 2, "Appid": Appid }
Api     = {"Name": "autenticador.Token", "Param": Param}
tC.Message["Api"] =  Api
Log(teste)
tC.sendMessageToQueue(queue);
tC.startConsuming(tC.getMessage)
if tC.Result['Result'] != 'Login/Password NOT OK':
    print (f"FALHA TESTE {teste} : TOKEN NAO RECEBIDO")
    sys.exit(0)
else:
    print(f"TESTE {teste}: OK")

#'LOGIN/PASSWORD COM PASSWORD INCORRETO'
teste = 'LOGIN/PASSWORD COM PASSWORD INCORRETO'
Appid   = {"Name" : "hudflutter", "Version" : "text da versao", "Appsys": "win64, android, iphone" }
Param   = {"Login": "sergio.moreira@gmail.com","Password": "VeiM4biu","Sistema" : 2, "Appid": Appid }
Api     = {"Name": "autenticador.Token", "Param": Param}
tC.Message["Api"] =  Api
Log(teste)
tC.sendMessageToQueue(queue);
tC.startConsuming(tC.getMessage)
if tC.Result['Result'] != 'Login/Password NOT OK':
    print (f"FALHA TESTE {teste} : TOKEN NAO RECEBIDO")
    sys.exit(0)
else:
    print(f"TESTE {teste}: OK")

teste = 'LOGIN/PASSWORD RECEBE TOKEN AUTORIZADO'
Appid   = {"Name" : "hudflutter", "Version" : "text da versao", "Appsys": "win64, android, iphone" }
Param   = {"Login": "sergio.moreira@gmail.com","Password": "veiM4biu","Sistema" : 2, "Appid": Appid }
Api     = {"Name": "autenticador.Token", "Param": Param}
tC.Message["Api"] =  Api
Log(teste)
tC.sendMessageToQueue(queue);
tC.startConsuming(tC.getMessage)
if 'Token' in tC.Result.keys():
    tC.setAuthorizationWith(tC.Result['Token'], tC.Result['Validade'])
else:
    print (f"FALHA TESTE {teste}: TOKEN NAO RECEBIDO")
    sys.exit(0)

if tC.Result['Result'] != 'OK':
    print (f"FALHA TESTE {teste}")
    sys.exit(0)
else:
    print(f"TESTE {teste}: OK")


#teste = 'ENVIO TOKEN PARA VALIDACAO'
teste = 'ENVIO TOKEN PARA VALIDACAO'
tC.Message["Api"] = {"Name": "autenticador.TokenValidate"}
Log(teste)
tC.sendMessageToQueue(queue);
tC.startConsuming(tC.getMessage)
if tC.Result['Result'] != 'OK':
    print (f"FALHA TESTE {teste}")
    sys.exit(0)
else:
    print(f"TESTE {teste}: OK")

# ENVIO TOKEN EXPIRADO
# ANTES DE ATIVAR - ALTERAR MAXAGE
# PARA UM VALOR MENOR QUE 20 SEGUNDOS
import time
maxage = int(konstantes('TOKEN', 'maxage'))
teste  = f"ENVIO TOKEN EXPIRADO {maxage}s"
Log(teste)
if maxage < 20:
    time.sleep(maxage + 20)
Api               = {"Name": "autenticador.TokenValidate"}
tC.Message["Api"] =  Api
tC.sendMessageToQueue(queue);
tC.startConsuming(tC.getMessage)
if tC.Result['Result'] != 'EMITIR NOVA AUTORIZACAO':
    print (f"FALHA TESTE {teste}")
    sys.exit(0)
else:
    print(f"TESTE {teste}: OK")

teste = 'LOGIN/PASSWORD RECEBE USER INFO'
Param   = {"Login": "sergio.moreira@gmail.com","Password": "veiM4biu" }
Api     = {"Name": "autenticador.UserInfo", "Param": Param}
tC.Message["Api"] =  Api
Log(teste)
tC.sendMessageToQueue(queue);
tC.startConsuming(tC.getMessage)
tC.showMessage(tC.Result)
if tC.Result['Result'] != 'OK':
    print (f"FALHA TESTE {teste}")
    sys.exit(0)
else:
    print(f"TESTE {teste}: OK")
