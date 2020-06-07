from   itsdangerous.serializer import Serializer
from   itsdangerous            import TimestampSigner
from   itsdangerous.exc        import BadSignature, BadData
from   api.produto.ProdutoDTO  import ProdutoDTO
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
class NovoProduto:
    def __init__(self, Param):
        self.Param  = Param

    def Execute (self):
        produto = ProdutoDTO()
        ident  = "pedido.NovoProduto"

        # AUTORIZATION
        data = {}
        data["Api"] = ident
        if  not tokenIsValid(ident, self.Param):
            data["Result"] = "TOKEN NOT VALID"
            Log(data["Result"], ident)
            return json.dumps(data)

        # VERIFICACAO PARAMETROS
        paramKeys = self.Param.keys()
        if 'Artigo' not in paramKeys:
            data["Result"] = "ERROR PARAM NOT FOUND"
            Log(data['Result'], ident)
            return json.dumps(data)

        try: 
            Artigo = int(self.Param['Artigo'])
        except:
            data["Result"] = "ERROR PARAM QUALITY"
            Log(data['Result'], ident)
            return json.dumps(data)
            
        if Artigo <= 0:
            data["Result"] = "ERROR PARAM VALUE"
            Log(data['Result'], ident)
            return json.dumps(data)

        # 2 CRIA O PRODUTO
        if not produto.novo(Artigo):
            data["Result"] = 'PROBLEMA NOVO PEDIDO'
            data["Error"]  = pedido.Error
            Log(data['Error'], ident)
            return json.dumps(data)
       
        produto = pedido.getDataField('id')
        data["Produto"] = produto
        data["Result"]  = "OK"

        return json.dumps(data)


class RemoveProduto:
    def __init__(self, Param):
        self.Param  = Param

    def Execute (self):
        produto = ProdutoDTO()
        ident  = "pedido.RemoveProduto"

        # AUTORIZATION
        data = {}
        data["Api"] = ident
        if  not tokenIsValid(ident, self.Param):
            data["Result"] = "TOKEN NOT VALID"
            Log(data["Result"], ident)
            return json.dumps(data)

        # VERIFICACAO PARAMETROS
        paramKeys = self.Param.keys()
        if 'Produto' not in paramKeys:
            data["Result"] = "ERROR PARAM NOT FOUND"
            Log(data['Result'], ident)
            return json.dumps(data)

        try: 
            Produto = int(self.Param['Produto'])
        except:
            data["Result"] = "ERROR PARAM QUALITY"
            Log(data['Result'], ident)
            return json.dumps(data)
            
        if Produto <= 0:
            data["Result"] = "ERROR PARAM VALUE"
            Log(data['Result'], ident)
            return json.dumps(data)

        # 2 REMOVE O PRODUTO
        if not produto.remove(Produto):
            data["Result"] = 'PROBLEMA REMOVE PEDIDO'
            data["Error"]  = produto.Error
            Log(data['Error'], ident)
            return json.dumps(data)
       
        data["Result"] = "OK"

        return json.dumps(data)

class NovoItemProduto:
    def __init__(self, Param):
        self.Param  = Param

    def Execute (self):
        ident  = "produto.NovoItemProduto"
        produto = ProdutoDTO()

        # AUTORIZATION
        data = {}
        data["Api"] = ident
        if  not tokenIsValid(ident, self.Param):
            data["Result"] = "TOKEN NOT VALID"
            Log(data["Result"], ident)
            return json.dumps(data)

        # VERIFICACAO PARAMETROS
        paramKeys  = self.Param.keys()
        parametros = ('Artigo','Produto','Quantidade','Essencial', 'Visivel')
        for param in parametros:
            if param not in paramKeys:
                data["Result"] = "ERROR PARAM NOT FOUND"
                Log(data['Result'], ident)
                return json.dumps(data)

        try: 
            Artigo     = int(self.Param['Artigo'])
            Produto    = int(self.Param['Pedido'])
            Quantidade = int(self.Param['Quantidade'])
            Essencial  = bool(self.Param['Essencial'])
            Visivel    = bool(self.Param['Visivel'])

        except:
            data["Result"] = "ERROR PARAM QUALITY"
            Log(data['Result'], ident)
            return json.dumps(data)
            
        if Artigo * Pedido * Qtd <= 0:
            data["Result"] = "ERROR PARAM VALUE"
            Log(data['Result'], ident)
            return json.dumps(data)

        #  SOLICITA CRIACAO DO NOVO ITEM
        if not pedido.novoItem(Pedido, Artigo, Qtd):
            data["Result"] = 'PROBLEMA NOVO ITEM PEDIDO'
            data["Error"]  = pedido.Error
            Log(data['Error'], ident)
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
        if  not tokenIsValid(ident, self.Param):
            data["Result"] = "TOKEN NOT VALID"
            Log(data["Result"], ident)
            return json.dumps(data)

        # VERIFICACAO PARAMETROS

        # 2 SOLICITA ITENS A VENDA
        if not pedido.mostraArtigoVenda():
            data["Result"] = 'PROBLEMA MOSTRA ARTIGOS VENDA'
            data["Error"]  = pedido.Error
            Log(data['Error'], ident)
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
        if  not tokenIsValid(ident, self.Param):
            data["Result"] = "TOKEN NOT VALID"
            Log(data["Result"], ident)
            return json.dumps(data)

        # VERIFICACAO PARAMETROS
        paramKeys = self.Param.keys()
        if 'Pedido' not in paramKeys:
            data["Result"] = "ERROR PARAM NOT FOUND"
            Log(data['Result'], ident)
            return json.dumps(data)

        try: 
            Pedido = int(self.Param['Pedido'])
        except:
            data["Result"] = "ERROR PARAM QUALITY"
            Log(data['Result'], ident)
            return json.dumps(data)
            
        if Pedido <= 0:
            data["Result"] = "ERROR PARAM VALUE"
            Log(data['Result'], ident)
            return json.dumps(data)

        # 2 APRESENTA O PEDIDO
        if not pedido.mostra(Pedido):
            data["Result"] = 'PROBLEMA MOSTRA PEDIDO'
            data["Error"]  = pedido.Error
            Log(data['Error'], ident)
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
        if  not tokenIsValid(ident, self.Param):
            data["Result"] = "TOKEN NOT VALID"
            Log(data["Result"], ident)
            return json.dumps(data)

        # VERIFICACAO PARAMETROS
        paramKeys = self.Param.keys()
        if 'Entregador' not in paramKeys:
            data["Result"] = "ERROR PARAM NOT FOUND"
            Log(data['Result'], ident)
            return json.dumps(data)

        if 'Pedido' not in paramKeys:
            data["Result"] = "ERROR PARAM NOT FOUND"
            Log(data['Result'], ident)
            return json.dumps(data)

        try: 
            Entregador = int(self.Param['Entregador'])
            Pedido     = int(self.Param['Pedido'])
        except:
            data["Result"] = "ERROR PARAM QUALITY"
            Log(data['Result'], ident)
            return json.dumps(data)
            
        if Entregador <= 0 or Pedido <= 0:
            data["Result"] = "ERROR PARAM VALUE"
            Log(data['Result'], ident)
            return json.dumps(data)

        # 2 ACRESCENTA O ENTREGADOR
        if not pedido.entregador(Entregador, Pedido):
            data["Result"] = 'PROBLEMA ENTREGADOR PEDIDO'
            data["Error"]  = pedido.Error
            Log(data['Error'], ident)
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
        if  not tokenIsValid(ident, self.Param):
            data["Result"] = "TOKEN NOT VALID"
            Log(data["Result"], ident)
            return json.dumps(data)

        # VERIFICACAO PARAMETROS
        paramKeys = self.Param.keys()
        if 'Desconto' not in paramKeys:
            data["Result"] = "ERROR PARAM NOT FOUND"
            Log(data['Result'], ident)
            return json.dumps(data)

        if 'Pedido' not in paramKeys:
            data["Result"] = "ERROR PARAM NOT FOUND"
            Log(data['Result'], ident)
            return json.dumps(data)

        try: 
            Desconto = float(self.Param['Desconto'])
            Pedido   = int(self.Param['Pedido'])
        except:
            data["Result"] = "ERROR PARAM QUALITY"
            Log(data['Result'], ident)
            return json.dumps(data)
            
        if Desconto <= 0.00 or Pedido <= 0:
            data["Result"] = "ERROR PARAM VALUE"
            Log(data['Result'], ident)
            return json.dumps(data)

        # 2 ACRESCENTA O ENTREGADOR
        if not pedido.desconto(Entregador, Pedido):
            data["Result"] = 'PROBLEMA DESCONTO PEDIDO'
            data["Error"]  = pedido.Error
            Log(data['Error'], ident)
            return json.dumps(data)
       
        data["Result"] = "OK"
        data["Data"]   = pedido.getData()

        return json.dumps(data)
