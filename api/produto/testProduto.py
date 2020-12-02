import sys, os
sys.path.append('/root/dockerCtrl/MercadoPy')
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

def Log (message):
    sendLog ('produto.testProduto', message)

queue = konstantes('PIKA', 'queue')

teste = "ENVIO DO LOGIN/PASSWORD E RECOLHA DO TOKEN PARA FUTUROS ACESSOS E CONFIGURACAO CANAL RSP"
Appid   = {"Name" : "Python cmd line", "Version" : "3.6", "Appsys": "Arm Raspbian" }
Param   = {"Login": "sergio.moreira@gmail.com","Password": "veiM4biu","Sistema" : 2, "Appid": Appid }
Api     = {"Name": "autenticador.Token", "Param": Param}
testAPI = TestAPI('produto.testProduto') 
testAPI.Message["Api"] =  Api
Log(teste)
testAPI.sendMessageToQueue(queue);
testAPI.startConsuming(testAPI.getMessage)
if 'Token' in testAPI.Result.keys():
    testAPI.setAuthorizationWith(testAPI.Result['Token'], testAPI.Result['Validade'])
else:
    Log("TOKEN NAO RECEBIDO")
    sys.exit(0)

teste = "APRESENTACAO DE UM PRODUTO EXISTENTE"
Param   = {"Produto": 3}
Api     = {"Name": "produto.MostraProduto", "Param": Param}
testAPI.Message["Api"] =  Api
Log(teste)
testAPI.sendMessageToQueue(queue);
testAPI.startConsuming(testAPI.getMessage)
if testAPI.Result['Result'] != "OK":
    print(f"FALHA TESTE {teste}")
    sys.exit(0)
else:
    print(f"TESTE {teste}: OK")
    Log(testAPI.Result['Data'])

teste = "APRESENTACAO DE UM PRODUTO EXISTENTE - PROBLEMA PARAMETRO"
Param   = {"Pruto": 3}
Api     = {"Name": "produto.MostraProduto", "Param": Param}
testAPI.Message["Api"] =  Api
Log(teste)
testAPI.sendMessageToQueue(queue);
testAPI.startConsuming(testAPI.getMessage)
if testAPI.Result['Result'] != "ERROR PARAM NOT FOUND":
    print(f"FALHA TESTE {teste}")
    sys.exit(0)
else:
    print(f"TESTE {teste}: OK")

teste = "APRESENTACAO DE UM PRODUTO EXISTENTE - PROBLEMA QUALIDADE PARAMETRO 1"
Param   = {"Produto": 'tres'}
Api     = {"Name": "produto.MostraProduto", "Param": Param}
testAPI.Message["Api"] =  Api
Log(teste)
testAPI.sendMessageToQueue(queue);
testAPI.startConsuming(testAPI.getMessage)
if testAPI.Result['Result'] != "ERROR PARAM QUALITY":
    print(f"FALHA TESTE {teste}")
    Log(testAPI.Result)
    sys.exit(0)
else:
    print(f"TESTE {teste}: OK")
    Log(testAPI.Result)

teste = "APRESENTACAO DE UM PRODUTO - PROBLEMA QUALIDADE PARAMETRO 2"
Param   = {"Produto": 9.878 }
Api     = {"Name": "produto.MostraProduto", "Param": Param}
testAPI.Message["Api"] =  Api
Log(teste)
testAPI.sendMessageToQueue(queue);
testAPI.startConsuming(testAPI.getMessage)
if testAPI.Result['Result'] != "PROBLEMA MOSTRA PEDIDO":
    print(f"FALHA TESTE {teste}")
    Log(testAPI.Result)
    sys.exit(0)
else:
    print(f"TESTE {teste}: OK")

teste = "APRESENTACAO DE UM PRODUTO - PROBLEMA QUALIDADE PARAMETRO 3"
Param   = {"Produto": -1 }
Api     = {"Name": "produto.MostraProduto", "Param": Param}
testAPI.Message["Api"] =  Api
Log(teste)
testAPI.sendMessageToQueue(queue);
testAPI.startConsuming(testAPI.getMessage)
if testAPI.Result['Result'] != "ERROR PARAM VALUE":
    print(f"FALHA TESTE {teste}")
    print(testAPI.Result)
    sys.exit(0)
else:
    print(f"TESTE {teste}: OK")

teste = "APRESENTACAO DE UM PRODUTO - PROBLEMA QUALIDADE PARAMETRO 4"
Param   = {"Produto": 0}
Api     = {"Name": "produto.MostraProduto", "Param": Param}
testAPI.Message["Api"] =  Api
Log(teste)
testAPI.sendMessageToQueue(queue);
testAPI.startConsuming(testAPI.getMessage)
if testAPI.Result['Result'] != "ERROR PARAM VALUE":
    print(f"FALHA TESTE {teste}")
    print(testAPI.Result)
    sys.exit(0)
else:
    print(f"TESTE {teste}: OK")
