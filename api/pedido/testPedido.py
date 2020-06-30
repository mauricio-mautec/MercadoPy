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

queue = konstantes('PIKA', 'queue')

def Log (message):
    sendLog ('pedido.testPedido', message)

print("\n==========================================", "TESTE PEDIDO")
N = 0

# ENVIO DO LOGIN/PASSWORD E RECOLHA DO TOKEN PARA FUTUROS ACESSOS E CONFIGURACAO CANAL RSP
teste   = "AUTENTICACAO E RECEBIMENTO DO TOKEN"
Appid   = {"Name" : "Python cmd line", "Version" : "3.6", "Appsys": "Arm Raspbian" }
Param   = {"Login": "sergio.moreira@gmail.com","Password": "veiM4biu","Sistema" : 2, "Appid": Appid }
Api     = {"Name": "autenticador.Token", "Param": Param}
testAPI = TestAPI('pedido.testPedido') 
testAPI.Message["Api"] =  Api
Log(teste)
testAPI.sendMessageToQueue(queue);
testAPI.startConsuming(testAPI.getMessage)
if 'Token' in testAPI.Result.keys():
    testAPI.setAuthorizationWith(testAPI.Result['Token'], testAPI.Result['Validade'])
    N += 1
    print(f"TESTE {N} {teste}: OK")
else:
    print(f"FALHA TESTE {teste}")
    pp.pprint(Param, '\n')
    pp.pprint(testAPI.Result['Result'])
    sys.exit(0)

# CRIACAO PEDIDO PROB PARAMETROS 1
teste   = "CRIACAO PEDIDO PROB PARAMETROS 1"
Param   = {"ClienSte": 1}
Api     = {"Name": "pedido.NovoPedido", "Param": Param}
testAPI.Message["Api"] =  Api
Log(teste)
testAPI.sendMessageToQueue(queue);
testAPI.startConsuming(testAPI.getMessage)
if testAPI.Result['Result'] != "ERROR PARAM NOT FOUND":
    print(f"FALHA TESTE {teste}")
    pp.pprint(Param, '\n')
    pp.pprint(testAPI.Result['Result'])
    sys.exit(0)
else:
    N += 1
    print(f"TESTE {N} {teste}: OK")

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
    pp.pprint(Param, '\n')
    pp.pprint(testAPI.Result['Result'])
    sys.exit(0)
else:
    N += 1
    print(f"TESTE {N} {teste}: OK")
    

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
    pp.pprint(Param, '\n')
    pp.pprint(testAPI.Result['Result'])
    sys.exit(0)
else:
    N += 1
    print(f"TESTE {N} {teste}: OK")
    

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
    pp.pprint(Param, '\n')
    pp.pprint(testAPI.Result['Result'])
    sys.exit(0)
else:
    N += 1
    print(f"TESTE {N} {teste}: OK")
    

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
    pp.pprint(Param)
    pp.pprint(testAPI.Result)
    sys.exit(0)
else:
    Pedido = testAPI.Result["Pedido"]
    N += 1
    print(f"TESTE {N} {teste} PEDIDO {Pedido}: OK")

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
    pp.pprint(Param)
    pp.pprint(testAPI.Result)
    sys.exit(0)
else:
    N += 1
    print(f"TESTE {N} {teste}: OK")
    


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
    pp.pprint(Param)
    pp.pprint(testAPI.Result)
    sys.exit(0)
else:
    Pedido = testAPI.Result["Pedido"]
    N += 1
    print(f"TESTE {N} {teste} {Pedido}: OK")


# LISTAR ARTIGOS PARA VENDA
teste   = "LISTAR ARTIGOS PARA VENDA"
Api     = {"Name": "pedido.MostraArtigoVenda"}
testAPI.Message["Api"] =  Api
Log(teste)
testAPI.sendMessageToQueue(queue);
testAPI.startConsuming(testAPI.getMessage)
if testAPI.Result['Result'] != "OK":
    print(f"FALHA TESTE {teste}")
    pp.pprint(Param)
    pp.pprint(testAPI.Result)
    sys.exit(0)
else:
    N += 1
    print(f"TESTE {N} {teste}: OK")
    

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
Api     = {"Name": "pedido.NovoItem", "Param": Param}
testAPI.Message["Api"] =  Api
Log(teste)
testAPI.sendMessageToQueue(queue);
testAPI.startConsuming(testAPI.getMessage)
if testAPI.Result['Result'] != "OK":
    print(f"FALHA TESTE {teste}")
    pp.pprint(Param)
    pp.pprint(testAPI.Result)
    sys.exit(0)
else:
    N += 1
    print(f"TESTE {N} {teste}: OK")
    

# INSERIR UM ITEM AUSENTE NO ESTOQUE_VENDA
teste   = "INSERIR UM ITEM AUSENTE NO ESTOQUE_VENDA"
Param   = {"Pedido" : Pedido, "Artigo": art_2, "Quantidade": 1}
Api     = {"Name": "pedido.NovoItem", "Param": Param}
testAPI.Message["Api"] =  Api
Log(teste)
testAPI.sendMessageToQueue(queue);
testAPI.startConsuming(testAPI.getMessage)
if testAPI.Result['Result'] != "PROBLEMA NOVO ITEM PEDIDO":
    print(f"FALHA TESTE {teste}")
    pp.pprint(Param)
    pp.pprint(testAPI.Result)
    sys.exit(0)
else:
    N += 1
    print(f"TESTE {N} {teste}: OK")
    Log(testAPI.Result)

# INSERIR UM ITEM AUSENTE NO ESTOQUE_VENDA
teste   = "INSERIR UM ITEM EM QTD A MENOR NO ESTOQUE_VENDA"
Param   = {"Pedido" : Pedido, "Artigo": art_3, "Quantidade": 3}
Api     = {"Name": "pedido.NovoItem", "Param": Param}
testAPI.Message["Api"] =  Api
Log(teste)
testAPI.sendMessageToQueue(queue);
testAPI.startConsuming(testAPI.getMessage)
if testAPI.Result['Result'] != "PROBLEMA NOVO ITEM PEDIDO":
    print(f"FALHA TESTE {teste}")
    pp.pprint(Param)
    pp.pprint(testAPI.Result)
    sys.exit(0)
else:
    N += 1
    print(f"TESTE {N} {teste}: OK")
    Log(testAPI.Result)


# INSERIR UM ITEM COMPOSTO (VENDA PRODUTO) PRESENTE NO ESTOQUE_VENDA
teste   =  "INSERIR UM ITEM COMPOSTO (VENDA PRODUTO) PRESENTE NO ESTOQUE_VENDA"
Param   = {"Pedido" : Pedido, "Artigo": 62, "Quantidade": 1}
Api     = {"Name": "pedido.NovoItem", "Param": Param}
testAPI.Message["Api"] =  Api
Log(teste)
testAPI.sendMessageToQueue(queue);
testAPI.startConsuming(testAPI.getMessage)
if testAPI.Result['Result'] != "OK":
    print(f"FALHA TESTE {teste}")
    pp.pprint(Param)
    pp.pprint(testAPI.Result)
    sys.exit(0)
else:
    N += 1
    print(f"TESTE {N} {teste}: OK")
    Log(testAPI.Result)


# INSERIR UM DESCONTO NEGATIVO NO PEDIDO
teste   =  "INSERIR UM DESCONTO NEGATIVO NO PEDIDO"
Param   = {"Pedido" : Pedido, "Desconto": -4.6}
Api     = {"Name": "pedido.DescontoPedido", "Param": Param}
testAPI.Message["Api"] =  Api
Log(teste)
testAPI.sendMessageToQueue(queue);
testAPI.startConsuming(testAPI.getMessage)
if testAPI.Result['Result'] != "ERROR PARAM VALUE":
    print(f"FALHA TESTE {teste}")
    pp.pprint(Param)
    pp.pprint(testAPI.Result)
    sys.exit(0)
else:
    N += 1
    print(f"TESTE {N} {teste}: OK")
    Log(testAPI.Result)

# INSERIR UM DESCONTO PROB PARAMETROS
teste   =  "INSERIR UM DESCONTO PROB PARAMETROS 1"
Param   = {"Desconto": 4.6}
Api     = {"Name": "pedido.DescontoPedido", "Param": Param}
testAPI.Message["Api"] =  Api
Log(teste)
testAPI.sendMessageToQueue(queue);
testAPI.startConsuming(testAPI.getMessage)
if testAPI.Result['Result'] != "ERROR PARAM NOT FOUND":
    print(f"FALHA TESTE {teste}")
    pp.pprint(Param)
    pp.pprint(testAPI.Result)
    sys.exit(0)
else:
    N += 1
    print(f"TESTE {N} {teste}: OK")
    Log(testAPI.Result)

# INSERIR UM DESCONTO PROB PARAMETROS 2
teste   =  "INSERIR UM DESCONTO PROB PARAMETROS 2"
Param   = {"Pedido": 4.6}
Api     = {"Name": "pedido.DescontoPedido", "Param": Param}
testAPI.Message["Api"] =  Api
Log(teste)
testAPI.sendMessageToQueue(queue);
testAPI.startConsuming(testAPI.getMessage)
if testAPI.Result['Result'] != "ERROR PARAM NOT FOUND":
    print(f"FALHA TESTE {teste}")
    pp.pprint(Param)
    pp.pprint(testAPI.Result)
    sys.exit(0)
else:
    N += 1
    print(f"TESTE {N} {teste}: OK")
    Log(testAPI.Result)

# INSERIR UM DESCONTO PROB PARAMETROS 3
teste   =  "INSERIR UM DESCONTO PROB PARAMETROS 3"
Param   = {"Pedido": 4.6, "Desconto": "a1"}
Api     = {"Name": "pedido.DescontoPedido", "Param": Param}
testAPI.Message["Api"] =  Api
Log(teste)
testAPI.sendMessageToQueue(queue);
testAPI.startConsuming(testAPI.getMessage)
if testAPI.Result['Result'] != "ERROR PARAM QUALITY":
    print(f"FALHA TESTE {teste}")
    pp.pprint(Param)
    pp.pprint(testAPI.Result)
    sys.exit(0)
else:
    N += 1
    print(f"TESTE {N} {teste}: OK")
    Log(testAPI.Result)

# INSERIR UM DESCONTO PARA UM PEDIDO INEXISTENTE
teste   =  "INSERIR UM DESCONTO PROB PARAMETROS 3"
Param   = {"Pedido": 1, "Desconto": "0.50"}
Api     = {"Name": "pedido.DescontoPedido", "Param": Param}
testAPI.Message["Api"] =  Api
Log(teste)
testAPI.sendMessageToQueue(queue);
testAPI.startConsuming(testAPI.getMessage)
result = testAPI.Result['Result']
error  = testAPI.Result['Error']
if   result != "PROBLEMA DESCONTO PEDIDO" and  error != "PEDIDO INEXISTENTE":
    print(f"FALHA TESTE {teste}")
    pp.pprint(Param)
    pp.pprint(testAPI.Result)
    sys.exit(0)
else:
    N += 1
    print(f"TESTE {N} {teste}: OK")
    Log(testAPI.Result)


# INSERIR DESCONTO PEDIDO
teste   =  f"INSERIR DESCONTO PEDIDO {Pedido}"
Param   = {"Pedido": Pedido, "Desconto": "0.50"}
Api     = {"Name": "pedido.DescontoPedido", "Param": Param}
testAPI.Message["Api"] =  Api
Log(teste)
testAPI.sendMessageToQueue(queue);
testAPI.startConsuming(testAPI.getMessage)
if   testAPI.Result['Result'] != "OK":
    print(f"FALHA TESTE {teste}")
    pp.pprint(Param)
    pp.pprint(testAPI.Result)
    sys.exit(0)
else:
    N += 1
    print(f"TESTE {N} {teste}: OK")
    Log(testAPI.Result)

# INSERIR ENTREGA PEDIDO
teste   =  f"INSERIR ENTREGA PEDIDO {Pedido}"
Param   = {"Pedido": Pedido, "Entrega": "2.70"}
Api     = {"Name": "pedido.ValorEntrega", "Param": Param}
testAPI.Message["Api"] =  Api
Log(teste)
testAPI.sendMessageToQueue(queue);
testAPI.startConsuming(testAPI.getMessage)
if   testAPI.Result['Result'] != "OK":
    print(f"FALHA TESTE {teste}")
    pp.pprint(Param)
    pp.pprint(testAPI.Result)
    sys.exit(0)
else:
    N += 1
    print(f"TESTE {N} {teste}: OK")
    Log(testAPI.Result)

# INSERIR ENTREGADOR PARA UM PEDIDO EXISTENTE
teste   =  f"INSERIR ENTREGADOR PEDIDO {Pedido}"
Param   = {"Pedido": Pedido, "Entregador": "10"}
Api     = {"Name": "pedido.EntregadorPedido", "Param": Param}
testAPI.Message["Api"] =  Api
Log(teste)
testAPI.sendMessageToQueue(queue);
testAPI.startConsuming(testAPI.getMessage)
if   testAPI.Result['Result'] != "OK":
    print(f"FALHA TESTE {teste}")
    pp.pprint(Param)
    pp.pprint(testAPI.Result)
    sys.exit(0)
else:
    N += 1
    print(f"TESTE {N} {teste}: OK")
    Log(testAPI.Result)

# ACRESCENTAR UMA OBSERVACAO DE ENTREGA
teste   =  f"ACRESCENTAR OBSERVACAO ENTREGA PEDIDO {Pedido}"
Param   = {"Pedido": Pedido, "Observacao": "CASA AMARELA, PORTAO MARROM, SEM CAMPANHINHA"}
Api     = {"Name": "pedido.ObservacaoEntrega", "Param": Param}
testAPI.Message["Api"] =  Api
Log(teste)
testAPI.sendMessageToQueue(queue);
testAPI.startConsuming(testAPI.getMessage)
if   testAPI.Result['Result'] != "OK":
    print(f"FALHA TESTE {teste}")
    pp.pprint(Param)
    pp.pprint(testAPI.Result)
    sys.exit(0)
else:
    N += 1
    print(f"TESTE {N} {teste}: OK")
    Log(testAPI.Result)

# APRESENTA PEDIDO
teste   =  f"APRESENTA PEDIDO {Pedido}"
Param   = {"Pedido": Pedido}
Api     = {"Name": "pedido.MostraPedido", "Param": Param}
testAPI.Message["Api"] =  Api
Log(teste)
testAPI.sendMessageToQueue(queue);
testAPI.startConsuming(testAPI.getMessage)
if   testAPI.Result['Result'] != "OK":
    print(f"FALHA TESTE {teste}")
    pp.pprint(Param)
    pp.pprint(testAPI.Result)
    sys.exit(0)
else:
    N += 1
    print(f"TESTE {N} {teste}: OK")
    Log(testAPI.Result)

# LISTA PEDIDOS EM ABERTO
teste   =  "LISTA PEDIDOS EM ABERTO"
Param   = {}
Api     = {"Name": "pedido.ApresentaPedidos", "Param": Param}
testAPI.Message["Api"] =  Api
Log(teste)
testAPI.sendMessageToQueue(queue);
testAPI.startConsuming(testAPI.getMessage)
if   testAPI.Result['Result'] != "OK":
    print(f"FALHA TESTE {teste}")
    pp.pprint(Param)
    pp.pprint(testAPI.Result)
    sys.exit(0)
else:
    N += 1
    print(f"TESTE {N} {teste}: OK")
    Log(testAPI.Result)

# ACEITA PEDIDO E COLOCA EM PRODUCAO
teste   =  "ACEITA PEDIDO E COLOCA EM PRODUCAO"
Param   = {"Pedido": Pedido}
Api     = {"Name": "pedido.AceitaPedido", "Param": Param}
testAPI.Message["Api"] =  Api
Log(teste)
testAPI.sendMessageToQueue(queue);
testAPI.startConsuming(testAPI.getMessage)
if   testAPI.Result['Result'] != "OK":
    print(f"FALHA TESTE {teste}")
    pp.pprint(Param)
    pp.pprint(testAPI.Result)
    sys.exit(0)
else:
    N += 1
    print(f"TESTE {N} {teste}: OK")
    Log(testAPI.Result)
