from   itsdangerous.serializer import Serializer
from   itsdangerous            import TimestampSigner
from   itsdangerous.exc        import BadSignature, BadData
from   api.produto.ProdutoDTO  import ProdutoDTO
from   api.autenticador.AutenticadorDTO import AutenticadorDTO
from   utility                 import *
import uuid
import json
import inspect

hugekey   = konstantes('TOKEN','hugekey')
timekey   = konstantes('TOKEN','timekey')
maxage    = int (konstantes('TOKEN','maxage'))

def Log(ident, message):
    sendLog(f'produto.{ident}', message)


def tokenIsValid(ident, param):
    Result, msg, AuthID, Loja = testToken(param)
    if not Result:
        Log(ident, msg)
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
        ident   = self.__class__.__name__

        # AUTORIZATION
        data = {}
        data["Api"] = ident
        if  not tokenIsValid(ident, self.Param):
            data["Result"] = "TOKEN NOT VALID"
            Log(ident, data["Result"])
            return json.dumps(data)

        # VERIFICACAO PARAMETROS
        paramKeys = self.Param.keys()
        if 'Artigo' not in paramKeys:
            data["Result"] = "ERROR PARAM NOT FOUND"
            Log(ident, data['Result'])
            return json.dumps(data)

        try: 
            Artigo = int(self.Param['Artigo'])
        except:
            data["Result"] = "ERROR PARAM QUALITY"
            Log(ident, data['Result'])
            return json.dumps(data)
            
        if Artigo <= 0:
            data["Result"] = "ERROR PARAM VALUE"
            Log(ident, data['Result'])
            return json.dumps(data)

        # 2 CRIA O PRODUTO
        if not produto.novo(Artigo):
            data["Result"] = 'PROBLEMA NOVO PEDIDO'
            data["Error"]  = produto.Error
            Log(ident, data['Error'])
            return json.dumps(data)
       
        produto = produto.getDataField('id')
        data["Produto"] = produto
        data["Result"]  = "OK"

        return json.dumps(data)


class RemoveProduto:
    def __init__(self, Param):
        self.Param  = Param

    def Execute (self):
        produto = ProdutoDTO()
        ident   = self.__class__.__name__

        # AUTORIZATION
        data = {}
        data["Api"] = ident
        if  not tokenIsValid(ident, self.Param):
            data["Result"] = "TOKEN NOT VALID"
            Log(ident, data["Result"])
            return json.dumps(data)

        # VERIFICACAO PARAMETROS
        paramKeys = self.Param.keys()
        if 'Produto' not in paramKeys:
            data["Result"] = "ERROR PARAM NOT FOUND"
            Log(ident, data['Result'])
            return json.dumps(data)

        try: 
            Produto = int(self.Param['Produto'])
        except:
            data["Result"] = "ERROR PARAM QUALITY"
            Log(ident, data['Result'])
            return json.dumps(data)
            
        if Produto <= 0:
            data["Result"] = "ERROR PARAM VALUE"
            Log(ident, data['Result'])
            return json.dumps(data)

        # 2 REMOVE O PRODUTO
        if not produto.remove(Produto):
            data["Result"] = 'PROBLEMA REMOVE PEDIDO'
            data["Error"]  = produto.Error
            Log(ident, data['Error'])
            return json.dumps(data)
       
        data["Result"] = "OK"

        return json.dumps(data)

class NovoArtigoProduto:
    def __init__(self, Param):
        self.Param  = Param

    def Execute (self):
        produto = ProdutoDTO()
        ident   = self.__class__.__name__

        # AUTORIZATION
        data = {}
        data["Api"] = ident
        if  not tokenIsValid(ident, self.Param):
            data["Result"] = "TOKEN NOT VALID"
            Log(ident, data["Result"])
            return json.dumps(data)

        # VERIFICACAO PARAMETROS
        paramKeys  = self.Param.keys()
        parametros = ('Artigo','Produto','Quantidade','Essencial', 'Visivel')
        for param in parametros:
            if param not in paramKeys:
                data["Result"] = "ERROR PARAM NOT FOUND"
                Log(idente, data['Result'])
                return json.dumps(data)

        try: 
            Artigo     = int(self.Param['Artigo'])
            Produto    = int(self.Param['Pedido'])
            Quantidade = int(self.Param['Quantidade'])
            Essencial  = bool(self.Param['Essencial'])
            Visivel    = bool(self.Param['Visivel'])

        except:
            data["Result"] = "ERROR PARAM QUALITY"
            Log(ident, data['Result'])
            return json.dumps(data)
            
        if Artigo * Pedido * Qtd <= 0:
            data["Result"] = "ERROR PARAM VALUE"
            Log(ident, data['Result'])
            return json.dumps(data)

        #  SOLICITA CRIACAO DO NOVO ITEM
        if not produto.novoArtigo(Pedido, Artigo, Qtd):
            data["Result"] = 'PROBLEMA NOVO ARTIGO PEDIDO'
            data["Error"]  = produto.Error
            Log(ident, data['Error'])
            return json.dumps(data)
       
        data["Result"] = "OK"
        data["Data"]   = produto.getArtigoData()

        return json.dumps(data)


class MostraProduto:
    def __init__(self, Param):
        self.Param  = Param

    def Execute (self):
        produto = ProdutoDTO()
        ident  = self.__class__.__name__

        # AUTORIZATION
        data = {}
        data["Api"] = ident
        if  not tokenIsValid(ident, self.Param):
            data["Result"] = "TOKEN NOT VALID"
            Log(ident, data["Result"])
            return json.dumps(data)

        # VERIFICACAO PARAMETROS
        paramKeys = self.Param.keys()
        if 'Produto' not in paramKeys:
            data["Result"] = "ERROR PARAM NOT FOUND"
            Log(ident, data['Result'])
            return json.dumps(data)

        try: 
            Produto = int(self.Param['Produto'])
        except:
            data["Result"] = "ERROR PARAM QUALITY"
            Log(ident, data['Result'])
            return json.dumps(data)
            
        if Produto <= 0:
            data["Result"] = "ERROR PARAM VALUE"
            Log(data['Result'], ident)
            return json.dumps(data)

        # 2 APRESENTA O PEDIDO
        if not produto.mostra(Produto):
            data["Result"] = 'PROBLEMA MOSTRA PEDIDO'
            data["Error"]  = produto.Error
            Log(ident, data['Error'])
            return json.dumps(data)
       
        data["Result"] = "OK"
        data["Data"]   = produto.getData()

        return json.dumps(data)

