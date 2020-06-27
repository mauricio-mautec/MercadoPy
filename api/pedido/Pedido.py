from   itsdangerous.serializer import Serializer
from   itsdangerous            import TimestampSigner
from   itsdangerous.exc        import BadSignature, BadData
from   api.pedido.PedidoDTO    import PedidoDTO
from   api.autenticador.Autenticador import TokenValidate
from   utility                 import *
import uuid
import json

hugekey   = konstantes('TOKEN','hugekey')
timekey   = konstantes('TOKEN','timekey')
maxage    = int (konstantes('TOKEN','maxage'))

def Log(ident, message):
    sendLog(ident, message)

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
        validate    = TokenValidate(self.Param)    # UPDATE LAST CHECK TIME OF THE TOKEN
        rslt        = validate.Execute()
        jslt        = json.loads(rslt)

        if  jslt['Result'] != 'OK':
            data["Result"] = "TOKEN NOT VALID"
            data['Error']  = jslt['Result']
            Log(ident, jslt["Result"])
            return json.dumps(data)

        if 'Token'    in jslt.keys():
            data['Token']    = jslt['Token']
        if 'Validade' in jslt.keys():
            data['Validade'] = jslt['Validade']

        # VERIFICACAO PARAMETROS
        paramKeys = self.Param.keys()
        Loja      = jslt['Loja']
        
        if 'Cliente' not in paramKeys:
            data["Result"] = "ERROR PARAM NOT FOUND"
            Log(ident, data['Result'])
            return json.dumps(data)

        try: 
            Cliente = int(self.Param['Cliente'])
        except:
            data["Result"] = "ERROR PARAM QUALITY"
            Log(ident, data['Result'])
            return json.dumps(data)
            
        if Cliente <= 0:
            data["Result"] = "ERROR PARAM VALUE"
            Log(ident, data['Result'])
            return json.dumps(data)

        # 2 CRIA O PEDIDO
        client = self.Param['Cliente']
        if not pedido.novo(client, Loja):
            data["Result"] = 'PROBLEMA NOVO PEDIDO'
            data["Error"]  = pedido.Error
            Log(ident, data['Error'])
            return json.dumps(data)
       
        pedido = pedido.getDataField('id')
        data["Pedido"] = pedido
        data["Result"] = "OK"

        return json.dumps(data)

class RemovePedido:
    def __init__(self, Param):
        self.Param  = Param

    def Execute (self):
        pedido = PedidoDTO()
        ident  = "pedido.RemovePedido"

        # AUTORIZATION
        data = {}
        data["Api"] = ident
        validate = TokenValidate(self.Param)    # UPDATE LAST CHECK TIME OF THE TOKEN
        rslt     = validate.Execute()
        jslt     = json.loads(rslt)

        if  jslt['Result'] != 'OK':
            data["Result"] = "TOKEN NOT VALID"
            data['Error']  = jslt['Result']
            Log(ident, jslt["Result"])
            return json.dumps(data)

        if 'Token'    in jslt.keys():
            data['Token']    = jslt['Token']
        if 'Validade' in jslt.keys():
            data['Validade'] = jslt['Validade']
            
        # VERIFICACAO PARAMETROS
        paramKeys = self.Param.keys()
        if 'Pedido' not in paramKeys:
            data["Result"] = "ERROR PARAM NOT FOUND"
            Log(ident, data['Result'])
            return json.dumps(data)

        try: 
            Pedido = int(self.Param['Pedido'])
        except:
            data["Result"] = "ERROR PARAM QUALITY"
            Log(ident, data['Result'])
            return json.dumps(data)
            
        if Pedido <= 0:
            data["Result"] = "ERROR PARAM VALUE"
            Log(ident, data['Result'])
            return json.dumps(data)

        # 2 REMOVE O PEDIDO
        if not pedido.remove(Pedido):
            data["Result"] = 'PROBLEMA REMOVE PEDIDO'
            data["Error"]  = pedido.Error
            Log(ident, data['Error'])
            return json.dumps(data)
       
        data["Result"] = "OK"

        return json.dumps(data)

class NovoItemPedido:
    def __init__(self, Param):
        self.Param  = Param

    def Execute (self):
        ident  = "pedido.NovoItemPedido"
        pedido = PedidoDTO()

        # AUTORIZATION
        data = {}
        data["Api"] = ident
        validate = TokenValidate(self.Param)    # UPDATE LAST CHECK TIME OF THE TOKEN
        rslt     = validate.Execute()
        jslt     = json.loads(rslt)
     
        if  jslt['Result'] != 'OK':
            data["Result"] = "TOKEN NOT VALID"
            data['Error']  = jslt['Result']
            Log(ident, jslt["Result"])
            return json.dumps(data)

        if 'Token'    in jslt.keys():
            data['Token']    = jslt['Token']
        if 'Validade' in jslt.keys():
            data['Validade'] = jslt['Validade']
        
        # VERIFICACAO PARAMETROS
        paramKeys = self.Param.keys()
        if 'Artigo' not in paramKeys:
            data["Result"] = "ERROR PARAM NOT FOUND"
            Log(ident, data['Result'])
            return json.dumps(data)

        if 'Pedido' not in paramKeys:
            data["Result"] = "ERROR PARAM NOT FOUND"
            Log(ident, data['Result'])
            return json.dumps(data)

        if 'Quantidade' not in paramKeys:
            data["Result"] = "ERROR PARAM NOT FOUND"
            Log(ident, data['Result'])
            return json.dumps(data)

        try: 
            Artigo = int(self.Param['Artigo'])
            Pedido = int(self.Param['Pedido'])
            Qtd    = int(self.Param['Quantidade'])

        except:
            data["Result"] = "ERROR PARAM QUALITY"
            Log(ident, data['Result'])
            return json.dumps(data)
            
        if Artigo * Pedido * Qtd <= 0:
            data["Result"] = "ERROR PARAM VALUE"
            Log(ident, data['Result'])
            return json.dumps(data)

        #  SOLICITA CRIACAO DO NOVO ITEM
        if not pedido.novoItem(Pedido, Artigo, Qtd):
            data["Result"] = 'PROBLEMA NOVO ITEM PEDIDO'
            data["Error"]  = pedido.Error
            Log(ident, data['Error'])
            return json.dumps(data)
       
        data["Result"] = "OK"
        data["Data"]   = pedido.getArtigoData()

        return json.dumps(data)

class MostraArtigoVenda:
    def __init__(self, Param):
        self.Param  = Param

    def Execute (self):
        pedido = PedidoDTO()
        ident  = "pedido.MostraArtigoVenda"

        # AUTORIZATION
        data = {}
        data["Api"] = ident
        validate = TokenValidate(self.Param)    # UPDATE LAST CHECK TIME OF THE TOKEN
        rslt     = validate.Execute()
        jslt     = json.loads(rslt)

        if  jslt['Result'] != 'OK':
            data["Result"] = "TOKEN NOT VALID"
            Log(ident, jslt["Result"])
            return json.dumps(data)

        if 'Token'    in jslt.keys():
            data['Token']    = jslt['Token']
        if 'Validade' in jslt.keys():
            data['Validade'] = jslt['Validade']

        # VERIFICACAO PARAMETROS

        # 2 SOLICITA ITENS A VENDA
        if not pedido.mostraArtigoVenda():
            data["Result"] = 'PROBLEMA MOSTRA ARTIGOS VENDA'
            data["Error"]  = pedido.Error
            Log(ident, data['Error'])
            return json.dumps(data)
       
        data["Result"] = "OK"
        data["Data"]   = pedido.getArtigoDataList()

        return json.dumps(data)

class MostraPedido:
    def __init__(self, Param):
        self.Param  = Param

    def Execute (self):
        pedido = PedidoDTO()
        ident  = "pedido.MostraPedido"

        # AUTORIZATION
        data = {}
        data["Api"] = ident
        validate = TokenValidate(self.Param)    # UPDATE LAST CHECK TIME OF THE TOKEN
        rslt     = validate.Execute()
        jslt     = json.loads(rslt)

        if  jslt['Result'] != 'OK':
            data["Result"] = "TOKEN NOT VALID"
            data["Error"]  = jslt["Result"]
            Log(ident, jslt["Result"])
            return json.dumps(data)

        if 'Token'    in jslt.keys():
            data['Token']    = jslt['Token']
        if 'Validade' in jslt.keys():
            data['Validade'] = jslt['Validade']

        # VERIFICACAO PARAMETROS
        paramKeys = self.Param.keys()
        if 'Pedido' not in paramKeys:
            data["Result"] = "ERROR PARAM NOT FOUND"
            Log(ident, data['Result'])
            return json.dumps(data)

        try: 
            Pedido = int(self.Param['Pedido'])
        except:
            data["Result"] = "ERROR PARAM QUALITY"
            Log(ident, data['Result'])
            return json.dumps(data)
            
        if Pedido <= 0:
            data["Result"] = "ERROR PARAM VALUE"
            Log(ident, data['Result'])
            return json.dumps(data)

        # 2 APRESENTA O PEDIDO
        if not pedido.mostra(Pedido):
            data["Result"] = 'PROBLEMA MOSTRA PEDIDO'
            data["Error"]  = pedido.Error
            Log(ident, data['Error'])
            return json.dumps(data)
       
        data["Result"] = "OK"
        data["Data"]   = pedido.getData()

        return json.dumps(data)

class EntregadorPedido:
    def __init__(self, Param):
        self.Param  = Param

    def Execute (self):
        pedido = PedidoDTO()
        ident  = "pedido.EntregadorPedido"

        # AUTORIZATION
        data = {}
        data["Api"] = ident
        validate = TokenValidate(self.Param)    # UPDATE LAST CHECK TIME OF THE TOKEN
        rslt     = validate.Execute()
        jslt     = json.loads(rslt)

        if  jslt['Result'] != 'OK':
            data["Result"] = "TOKEN NOT VALID"
            date["Error"]  = jslt["Result"]
            Log(ident, jslt["Result"])
            return json.dumps(data)

        if 'Token'    in jslt.keys():
            data['Token']    = jslt['Token']
        if 'Validade' in jslt.keys():
            data['Validade'] = jslt['Validade']

        # VERIFICACAO PARAMETROS
        paramKeys = self.Param.keys()
        if 'Entregador' not in paramKeys:
            data["Result"] = "ERROR PARAM NOT FOUND"
            Log(ident, data['Result'])
            return json.dumps(data)

        if 'Pedido' not in paramKeys:
            data["Result"] = "ERROR PARAM NOT FOUND"
            Log(ident, data['Result'])
            return json.dumps(data)

        try: 
            Entregador = int(self.Param['Entregador'])
            Pedido     = int(self.Param['Pedido'])
        except:
            data["Result"] = "ERROR PARAM QUALITY"
            Log(ident, data['Result'])
            return json.dumps(data)
            
        if Entregador <= 0 or Pedido <= 0:
            data["Result"] = "ERROR PARAM VALUE"
            Log(ident, data['Result'])
            return json.dumps(data)

        # 2 ACRESCENTA O ENTREGADOR
        if not pedido.entregador(Entregador, Pedido):
            data["Result"] = 'PROBLEMA ENTREGADOR PEDIDO'
            data["Error"]  = pedido.Error
            Log(ident, data['Error'])
            return json.dumps(data)
       
        data["Result"] = "OK"
        data["Data"]   = pedido.getData()

        return json.dumps(data)

class DescontoPedido:
    def __init__(self, Param):
        self.Param  = Param

    def Execute (self):
        pedido = PedidoDTO()
        ident  = "pedido.DescontoPedido"

        # AUTORIZATION
        data = {}
        data["Api"] = ident
        validate = TokenValidate(self.Param)    # UPDATE LAST CHECK TIME OF THE TOKEN
        rslt     = validate.Execute()
        jslt     = json.loads(rslt)

        if  jslt['Result'] != 'OK':
            data["Result"] = "TOKEN NOT VALID"
            data["Error"]  = jslt["Result"]
            Log(ident, jslt["Result"])
            return json.dumps(data)

        if 'Token'    in jslt.keys():
            data['Token']    = jslt['Token']
        if 'Validade' in jslt.keys():
            data['Validade'] = jslt['Validade']

        # VERIFICACAO PARAMETROS
        paramKeys = self.Param.keys()
        if 'Desconto' not in paramKeys:
            data["Result"] = "ERROR PARAM NOT FOUND"
            Log(ident, data['Result'])
            return json.dumps(data)

        if 'Pedido' not in paramKeys:
            data["Result"] = "ERROR PARAM NOT FOUND"
            Log(ident, data['Result'])
            return json.dumps(data)

        try: 
            Desconto = float(self.Param['Desconto'])
            Pedido   = int(self.Param['Pedido'])
        except:
            data["Result"] = "ERROR PARAM QUALITY"
            Log(ident, data['Result'])
            return json.dumps(data)
            
        if Desconto <= 0.00 or Pedido <= 0:
            data["Result"] = "ERROR PARAM VALUE"
            Log(ident, data['Result'])
            return json.dumps(data)

        # 2 ACRESCENTA O ENTREGADOR
        if not pedido.desconto(Desconto, Pedido):
            data["Result"] = 'PROBLEMA DESCONTO PEDIDO'
            data["Error"]  = pedido.Error
            Log(ident, data['Error'])
            return json.dumps(data)
       
        data["Result"] = "OK"
        data["Data"]   = pedido.getData()

        return json.dumps(data)
