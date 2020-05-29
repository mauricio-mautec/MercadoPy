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

def Log(ident, message):
    sendLog('pedido.NovoPedido', message)


def tokenIsValid(ident, param):
    Result, msg, AuthID = testToken(param)
    if not Result:
        Log(msg, ident)
        return False
    else:
        dto = AutenticadorDTO()
        dto.updateAuth(AuthID, ident)    # UPDATE LAST CHECK TIME OF THE TOKEN
        return True 

# RETORNA CASO LOGIN / PASSWORD CONFERIR
# JSON COM SISTEMAS QUE PODEM SER ATENDIDOS
class NovoPedido:
    def __init__(self, Param):
        self.Param  = Param

    def Execute (self):
        pedido = PedidoDTO()
        ident  = "pedido.NovoPedido"

        # AUTORIZATION
        data = {}
        data["Api"] = ident
        if  not tokenIsValid(ident, self.Param):
            data["Result"] = "TOKEN NOT VALID"
            Log(data["Result"], ident)
            return json.dumps(data)

        # VERIFICACAO PARAMETROS
        paramKeys = self.Param.keys()
        if 'Cliente' not in paramKeys:
            data["Result"] = "ERROR PARAM NOT FOUND"
            Log(data['Result'], ident)
            return json.dumps(data)

        try: 
            Cliente = int(self.Param['Cliente'])
        except:
            data["Result"] = "ERROR PARAM QUALITY"
            Log(data['Result'], ident)
            return json.dumps(data)
            
        if Cliente <= 0:
            data["Result"] = "ERROR PARAM VALUE"
            Log(data['Result'], ident)
            return json.dumps(data)

        # 2 CRIA O PEDIDO
        client = self.Param['Cliente']
        if not pedido.novo(client):
            data["Result"] = 'PROBLEMA NOVO PEDIDO'
            data["Error"]  = pedido.Error
            Log(data['Error'], ident)
            return json.dumps(data)
       
        pedido = pedido.getDataField('id')
        data["Pedido"] = pedido
        data["Result"] = "OK"

        return json.dumps(data)
