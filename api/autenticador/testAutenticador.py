import sys, os
sys.path.append('/api');
import time
import random
from   pathlib import Path
import pika
import json
import importlib
import unicodedata
import uuid
from utility import *
import pprint
pp = pprint.PrettyPrinter(indent=4)

queue = konstantes('PIKA', 'queue')

testAPI = TestAPI('autenticador.testAutenticador')

def Log (message):
    sendLog ('autenticador.testAutenticador', message)

print("\n==========================================", "TESTE AUTENTICADOR")
N = 0

#'LOGIN/PASSWORD COM LOGIN INCORRETO'
teste = 'LOGIN/PASSWORD COM LOGIN INCORRETO'
Appid   = {"Name" : "testPython", "Version" : "1.0", "Appsys": "python3 linux" }
Param   = {"Login": "sergxio.moreira@gmail.com","Password": "veiM4biu","Sistema" : 2, "Appid": Appid }
Api     = {"Name": "autenticador.Token", "Param": Param}
testAPI.Message["Api"] =  Api
Log(teste)
testAPI.sendMessageToQueue(queue);
testAPI.startConsuming(testAPI.getMessage)
if testAPI.Result['Result'] != 'Login/Password NOT OK':
    print (f"FALHA TESTE {teste} : TOKEN NAO RECEBIDO")
    pp.pprint(Param)
    pp.pprint(testAPI.Result)
    sys.exit(0)
else:
    N += 1 
    print(f"TESTE {N} {teste} OK")

#'LOGIN/PASSWORD COM PASSWORD INCORRETO'
teste = 'LOGIN/PASSWORD COM PASSWORD INCORRETO'
Param   = {"Login": "sergio.moreira@gmail.com","Password": "VeiM4biu","Sistema" : 2, "Appid": Appid }
Api     = {"Name": "autenticador.Token", "Param": Param}
testAPI.Message["Api"] =  Api
Log(teste)
testAPI.sendMessageToQueue(queue);
testAPI.startConsuming(testAPI.getMessage)
if testAPI.Result['Result'] != 'Login/Password NOT OK':
    print (f"FALHA TESTE {teste} : TOKEN NAO RECEBIDO")
    pp.pprint(Param)
    pp.pprint(testAPI.Result)
    sys.exit(0)
else:
    N += 1 
    print(f"TESTE {N} {teste} OK")

teste = 'LOGIN/PASSWORD RECEBE TOKEN AUTORIZADO'
Param   = {"Login": "sergio.moreira@gmail.com","Password": "veiM4biu","Sistema" : 2, "Appid": Appid }
Api     = {"Name": "autenticador.Token", "Param": Param}
testAPI.Message["Api"] =  Api
Log(teste)
testAPI.sendMessageToQueue(queue);
testAPI.startConsuming(testAPI.getMessage)
if 'Token' in testAPI.Result.keys():
    testAPI.setAuthorizationWith(testAPI.Result['Token'], testAPI.Result['Validade'])
else:
    N += 1 
    print (f"FALHA TESTE {N} {teste} TOKEN NAO RECEBIDO")
    pp.pprint(Param)
    pp.pprint(testAPI.Result)
    sys.exit(0)

if testAPI.Result['Result'] != 'OK':
    print (f"FALHA TESTE {teste}")
    pp.pprint(Param)
    pp.pprint(testAPI.Result)
    sys.exit(0)
else:
    N += 1 
    print(f"TESTE {N} {teste} OK")


#teste = 'ENVIO TOKEN PARA VALIDACAO'
teste = 'ENVIO TOKEN PARA VALIDACAO'
testAPI.Message["Api"] = {"Name": "autenticador.TokenValidate"}
Log(teste)
testAPI.sendMessageToQueue(queue);
testAPI.startConsuming(testAPI.getMessage)
if testAPI.Result['Result'] != 'OK':
    print (f"FALHA TESTE {teste}")
    pp.pprint(Param)
    pp.pprint(testAPI.Result)
    sys.exit(0)
else:
    N += 1 
    print(f"TESTE {N} {teste} OK")

# ENVIO TOKEN EXPIRADO
# ANTES DE ATIVAR - ALTERAR MAXAGE
# PARA UM VALOR MENOR QUE 20 SEGUNDOS
import time
maxage   = int(konstantes('TOKEN', 'maxage'))
maxagedb = int(konstantes('TOKEN', 'maxagedb'))
teste    = f"ENVIO TOKEN EXPIRADO {maxage}s"
Log(teste)
if maxage < 20:
    time.sleep(maxagedb)
Api               = {"Name": "autenticador.TokenValidate"}
testAPI.Message["Api"] =  Api
testAPI.sendMessageToQueue(queue);
testAPI.startConsuming(testAPI.getMessage)
if testAPI.Result['Result'] != 'REQUEST NEW AUTHORIZATION':
    print (f"FALHA TESTE {teste}")
    pp.pprint(Param)
    pp.pprint(testAPI.Result)
    sys.exit(0)
else:
    N += 1 
    print(f"TESTE {N} {teste} OK")

teste = 'LOGIN/PASSWORD RECEBE USER INFO'
Param   = {"Login": "sergio.moreira@gmail.com","Password": "veiM4biu" }
Api     = {"Name": "autenticador.UserInfo", "Param": Param}
testAPI.Message["Api"] =  Api
Log(teste)
testAPI.sendMessageToQueue(queue);
testAPI.startConsuming(testAPI.getMessage)
testAPI.showMessage(testAPI.Result)
if testAPI.Result['Result'] != 'OK':
    print (f"FALHA TESTE {teste}")
    pp.pprint(Param)
    pp.pprint(testAPI.Result)
    sys.exit(0)
else:
    N += 1 
    print(f"TESTE {N} {teste} OK")
