import sys, os
sys.path.append('/srv/mautec/www/MercadoPy')
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
    sendLog ('pedido.testPedido', message)

queue = konstantes('PIKA', 'queue')
# ENVIO DO LOGIN/PASSWORD E RECOLHA DO TOKEN PARA FUTUROS ACESSOS E CONFIGURACAO CANAL RSP
Appid   = {"Name" : "Python cmd line", "Version" : "3.6", "Appsys": "Arm Raspbian" }
Param   = {"Login": "sergio.moreira@gmail.com","Password": "veiM4biu","Sistema" : 2, "Appid": Appid }
Api     = {"Name": "autenticador.Token", "Param": Param}
testAPI = TestAPI('pedido.testPedido') 
testAPI.Message["Api"] =  Api
Log("MENSAGEM DE LOGIN PARA FORNECIMENTO TOKEN COMUNICACAO")
testAPI.sendMessageToQueue(queue);
testAPI.startConsuming(testAPI.getMessage)
if 'Token' in testAPI.Result.keys():
    testAPI.setAuthorizationWith(testAPI.Result['Token'], testAPI.Result['Validade'])
    print(testAPI.Result['Token'], testAPI.Result['Validade'])
else:
    Log("TOKEN NAO RECEBIDO")
    sys.exit(0)

# CRIACAO PEDIDO PROB PARAMETROS 1
teste = "CRIACAO PEDIDO PROB PARAMETROS 1"
Param   = {"ClienSte": 1}
Api     = {"Name": "pedido.NovoPedido", "Param": Param}
testAPI.Message["Api"] =  Api
Log(teste)
testAPI.sendMessageToQueue(queue);
testAPI.startConsuming(testAPI.getMessage)
if testAPI.Result['Result'] != "ERROR PARAM NOT FOUND":
    print(f"FALHA TESTE {teste}")
    sys.exit(0)
else:
    print(f"TESTE {teste}: OK")

# CRIACAO PEDIDO PROB PARAMETROS 2
teste = "CRIACAO PEDIDO PROB PARAMETROS 2"
Param   = {"Cliente": 'a1'}
Api     = {"Name": "pedido.NovoPedido", "Param": Param}
testAPI.Message["Api"] =  Api
Log(teste)
testAPI.sendMessageToQueue(queue);
testAPI.startConsuming(testAPI.getMessage)
if testAPI.Result['Result'] != "ERROR PARAM QUALITY":
    print(f"FALHA TESTE {teste}")
    sys.exit(0)
else:
    print(f"TESTE {teste}: OK")

# CRIACAO PEDIDO PROB PARAMETROS 3
teste   = "CRIACAO PEDIDO PROB PARAMETROS 3"
Param   = {"Cliente": -1}
Api     = {"Name": "pedido.NovoPedido", "Param": Param}
testAPI.Message["Api"] =  Api
Log(teste)
testAPI.sendMessageToQueue(queue);
testAPI.startConsuming(testAPI.getMessage)
if testAPI.Result['Result'] != "ERROR PARAM VALUE":
    print(f"FALHA TESTE {teste}")
    sys.exit(0)
else:
    print(f"TESTE {teste}: OK")

# CRIACAO PEDIDO PROB PARAMETROS 4
teste   = "CRIACAO PEDIDO PROB PARAMETROS 4"
Param   = {"Cliente": 200}
Api     = {"Name": "pedido.NovoPedido", "Param": Param}
testAPI.Message["Api"] =  Api
Log(teste)
testAPI.sendMessageToQueue(queue);
testAPI.startConsuming(testAPI.getMessage)
if testAPI.Result['Result'] != "PROBLEMA NOVO PEDIDO":
    print(f"FALHA TESTE {teste}")
    print(testAPI.Result)
    sys.exit(0)
else:
    print(f"TESTE {teste}: OK")

# CRIACAO NOVO PEDIDO
teste   = "CRIACAO NOVO PEDIDO"
Param   = {"Cliente": 1}
Api     = {"Name": "pedido.NovoPedido", "Param": Param}
testAPI.Message["Api"] =  Api
Log(teste)
testAPI.sendMessageToQueue(queue);
testAPI.startConsuming(testAPI.getMessage)
if testAPI.Result['Result'] != "OK":
    print(f"FALHA TESTE {teste}")
    pp.pprint(testAPI.Result)
    sys.exit(0)
else:
    print(f"TESTE {teste}: OK")

Pedido = testAPI.Result["Pedido"]
Log(f"Pedido no.:{Pedido}")

# REMOCAO DO PEDIDO CRIADO
teste   = f"REMOCAO DO PEDIDO {Pedido} CRIADO"
Param   = {"Pedido": Pedido}
Api     = {"Name": "pedido.RemovePedido", "Param": Param}
testAPI.Message["Api"] =  Api
Log(teste)
testAPI.sendMessageToQueue(queue);
testAPI.startConsuming(testAPI.getMessage)
if testAPI.Result['Result'] != "OK":
    print(f"FALHA TESTE {teste}")
    pp.pprint(testAPI.Result)
    sys.exit(0)
else:
    print(f"TESTE {teste}: OK")

# CRIACAO NOVO PEDIDO
teste   = "CRIACAO NOVO PEDIDO"
Param   = {"Cliente": 1}
Api     = {"Name": "pedido.NovoPedido", "Param": Param}
testAPI.Message["Api"] =  Api
Log(teste)
testAPI.sendMessageToQueue(queue);
testAPI.startConsuming(testAPI.getMessage)
if testAPI.Result['Result'] != "OK":
    print(f"FALHA TESTE {teste}")
    print("ENVIADO:")
    pp.pprint(Api)
    print("RECEBIDO:")
    pp.pprint(testAPI.Result)
    sys.exit(0)
else:
    Pedido = testAPI.Result["Pedido"]
    Log(f"Pedido no.: {Pedido}")

# LISTAR ARTIGOS PARA VENDA
teste   = "LISTAR ARTIGOS PARA VENDA"
Api     = {"Name": "pedido.MostraArtigoVenda"}
testAPI.Message["Api"] =  Api
Log(teste)
testAPI.sendMessageToQueue(queue);
testAPI.startConsuming(testAPI.getMessage)
if testAPI.Result['Result'] != "OK":
    print(f"FALHA TESTE {teste}")
    pp.pprint(testAPI.Result)
    sys.exit(0)
else:
    print(f"TESTE {teste}: OK")

ArtigoList = testAPI.Result['Data']

pyobj = ArtigoList[0]
art_1 = pyobj['id']

pyobj = ArtigoList[1]
art_2 = pyobj['id']

pyobj = ArtigoList[2]
art_3 = pyobj['id']

# INSERIR UM ITEM PRESENTE NO ESTOQUE_VENDA
teste   = "INSERIR UM ITEM PRESENTE NO ESTOQUE_VENDA"
Param   = {"Pedido" : Pedido, "Artigo": art_1, "Quantidade": 1}
Api     = {"Name": "pedido.NovoItemPedido", "Param": Param}
testAPI.Message["Api"] =  Api
Log(teste)
testAPI.sendMessageToQueue(queue);
testAPI.startConsuming(testAPI.getMessage)
if testAPI.Result['Result'] != "OK":
    print(f"FALHA TESTE {teste}")
    pp.pprint(testAPI.Result)
    sys.exit(0)
else:
    print(f"TESTE {teste}: OK")

# INSERIR UM ITEM AUSENTE NO ESTOQUE_VENDA
teste   = "INSERIR UM ITEM AUSENTE NO ESTOQUE_VENDA"
Param   = {"Pedido" : Pedido, "Artigo": art_2, "Quantidade": 1}
Api     = {"Name": "pedido.NovoItemPedido", "Param": Param}
testAPI.Message["Api"] =  Api
Log(teste)
testAPI.sendMessageToQueue(queue);
testAPI.startConsuming(testAPI.getMessage)
if testAPI.Result['Result'] != "PROBLEMA NOVO ITEM PEDIDO":
    print(f"FALHA TESTE {teste}")
    pp.pprint(testAPI.Result)
    sys.exit(0)
else:
    print(f"TESTE {teste}: OK")
    Log(testAPI.Result)

# INSERIR UM ITEM AUSENTE NO ESTOQUE_VENDA
teste   = "INSERIR UM ITEM EM QTD A MENOR NO ESTOQUE_VENDA"
Param   = {"Pedido" : Pedido, "Artigo": art_3, "Quantidade": 3}
Api     = {"Name": "pedido.NovoItemPedido", "Param": Param}
testAPI.Message["Api"] =  Api
Log(teste)
testAPI.sendMessageToQueue(queue);
testAPI.startConsuming(testAPI.getMessage)
if testAPI.Result['Result'] != "PROBLEMA NOVO ITEM PEDIDO":
    print(f"FALHA TESTE {teste}")
    pp.pprint(testAPI.Result)
    sys.exit(0)
else:
    print(f"TESTE {teste}: OK")
    Log(testAPI.Result)

# INSERIR UM ITEM COMPOSTO (VENDA PRODUTO) PRESENTE NO ESTOQUE_VENDA
teste   =  "INSERIR UM ITEM COMPOSTO (VENDA PRODUTO) PRESENTE NO ESTOQUE_VENDA"
Param   = {"Pedido" : Pedido, "Artigo": 62, "Quantidade": 1}
Api     = {"Name": "pedido.NovoItemPedido", "Param": Param}
testAPI.Message["Api"] =  Api
Log(teste)
testAPI.sendMessageToQueue(queue);
testAPI.startConsuming(testAPI.getMessage)
if testAPI.Result['Result'] != "OK":
    print(f"FALHA TESTE {teste}")
    pp.pprint(testAPI.Result)
    sys.exit(0)
else:
    print(f"TESTE {teste}: OK")
    Log(testAPI.Result)
