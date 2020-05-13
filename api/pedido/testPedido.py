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

# ENVIO DO LOGIN/PASSWORD E RECOLHA DO TOKEN PARA FUTUROS ACESSOS E CONFIGURACAO CANAL RSP
Appid   = {"Name" : "Python cmd line", "Version" : "3.6", "Appsys": "Arm Raspbian" }
Param   = {"Login": "sergio.moreira@gmail.com","Password": "veiM4biu","Sistema" : 2, "Appid": Appid }
Api     = {"Name": "autenticador.Token", "Param": Param}
testAPI = TestAPI() 
testAPI.Message["Api"] =  Api
print("MENSAGEM DE LOGIN:")
testAPI.sendMessageToQueue(queue);
testAPI.startConsuming(testAPI.getMessage)
testAPI.showMessage(testAPI.Result)
if 'Token' in testAPI.Result.keys():
    testAPI.setAuthorizationWith(testAPI.Result['Token'], testAPI.Result['Validade'])
else:
    print("TOKEN NAO RECEBIDO")
    sys.exit(0)

# TESTE DO ENVIO DO TOKEN PARA VALIDACAO
Param   = {"Cliente": 1}
Api     = {"Name": "pedido.NovoPedido", "Param": Param}
testAPI.Message["Api"] =  Api
print(f"\n\nMENSAGEM ENVIADA AUTORIZACAO VALIDA:")
testAPI.sendMessageToQueue(queue);
testAPI.startConsuming(testAPI.getMessage)
testAPI.showMessage(testAPI.Result)

sys.exit(0)
# TESTE DO ENVIO DO TOKEN PARA VALIDACAO TOKEN EXPIRADO
import time
#time.sleep(20)
Param   = {"Cliente": 1}
Api     = {"Name": "pedido.NovoPedido", "Param": Param}
testAPI.Message["Api"] =  Api
print(f"\n\nMENSAGEM ENVIADA AUTORIZACAO TOKEN EXPIRADO:")
testAPI.sendMessageToQueue(queue);
testAPI.startConsuming(testAPI.getMessage)
testAPI.showMessage(testAPI.Result)

# TESTE CRIACAO DE UM NOVO PEDIDO PROB PARAMETROS
Param   = {"Cliente": 1}
Api     = {"Name": "pedido.NovoPedido", "Param": Param}
print(f"\n\nCRIAR NOVO PEDIDO")
testAPI.sendMessageToQueue(queue);
testAPI.startConsuming(testAPI.getMessage)
testAPI.showMessage(testAPI.Result)

