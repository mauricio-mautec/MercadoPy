from   itsdangerous.serializer import Serializer
from   itsdangerous            import TimestampSigner
from   itsdangerous.exc        import BadSignature, BadData
from   api.pedido.PedidoDTO    import PedidoDTO
from   api.autenticador.AutenticadorDTO import AutenticadorDTO
from   utility                 import *
import uuid
import json

hugekey   = konstantes('TOKEN','hugekey')
timekey   = konstantes('TOKEN','timekey')
maxage    = int (konstantes('TOKEN','maxage'))


# RETORNA CASO LOGIN / PASSWORD CONFERIR
# JSON COM SISTEMAS QUE PODEM SER ATENDIDOS
class NovoPedido:
    def __init__(self, Param):
        self.Param  = Param

    def Execute (self):
        pedido       = PedidoDTO()

        # 1 AUTORIZATION
        data = {}
        data["Api"]    = "pedido.NovoPedido"
        if  not self.tokenIsValid():
            data["Result"] = "TOKEN NOT VALID"
            self.Log(data["Result"])
            return json.dumps(data)

        paramKeys = self.Param.keys()
        if 'Cliente' not in paramKeys:
            data["Result"] = "ERROR PARAM"
            self.Log(data['Result'])
            return json.dumps(data)

        # 2 VERIFICA CLIENTE OK

        # 3 CRIA O PEDIDO
        client = 1
        if not pedido.novo(client):
            data["Result"] = 'PROBLEMA NOVO PEDIDO'
            data["Error"]  = pedido.Error
            self.Log(data['Error'])
            return json.dumps(data)
        
        data["Result"] = "TOKEN OK"
        self.Log(data['Result'])
        return json.dumps(data)
        
    def Log(self, message):
        sendLog('pedido.NovoPedido', message)
    

    def tokenIsValid(self):
        Result, msg, AuthID = testToken(self.Param)
        if not Result:
            self.Log(msg)
            return False
        else:
            dto = AutenticadorDTO()
            dto.checkAuth(AuthID)    # UPDATE LAST CHECK TIME OF THE TOKEN
            return True 
