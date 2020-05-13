import datetime
import importlib
from utility import konstantes
database_DB = konstantes('DATABASE','database_DB')
banco       = importlib.import_module (database_DB)

# TRABALHA OS ITENS QUE COMPOEM UM PEDIDO DE VENDA
from api.pedido.ItemDTO   import ItemDTO
from api.pedido.EventoDTO import EventoDTO

class PedidoDTO():
# METODOS COMUNS

    def __init__(self):
        self.__resetData()
        self.__DataList = []
        self.db    = banco.AccessDB()

    def __resetData (self):
        # DADOS EXPOSTOS DTO
        # INFORMACAO QUE O DTO PRECISA TRABALHAR/FORNECER
        self.__Data = {
            'id'                 : 0,
            'Cliente'            : 0,
            'Entrada'            : '',
            'Pagamento_Troco'    : '', 
            'Valor'              : 0.0, 
            'Desconto'           : 0.00,
            'Entrega'            : 0.00,
            'Total'              : 0.00,
            'Entregador'         : 0,
            'Concluido'          : False,
            'Observacao_Entrega' : '',
            'ItemList'           : [],
            'EventoList'         : [] }
         
    def __columns (self):
        strcol = ' '
        for col in self.__Data.keys():
            strcol += f"{col},"
        return strcol[0:-1]

    def __setData (self, datum, value):
        if datum in list(self.__Data.keys()):
            self.__Data[datum] = value
    
    def __setDataList (self, tupleData):
        self.__resetData()

        datacol = 0
        for field in self.__Data.keys():        
            self.__Data[field] = tupleData(datacol)
            datacol += 1
        
        self.__DataList.append(self.__Data)

    def getDataField (self, datum):
        if datum in list(self.__Data.keys()):
            return self.__Data[datum][1]
        else:
            return False

    def getData (self):
        return self.__Data

    def getDataList (self):
        return self.__DataList


# METODOS ESPECIFICOS
# CRIAR NOVO PEDIDO PARA O CLIENTE
# REMOVER PEDIDO
# VALOR DESCONTO
# VALOR ENTREGA
# ESCOLHE ENTREGADOR
# LISTAR PEDIDOS ABERTOS
# LISTAR PEDIDOS EM PRODUCAO
# LISTAR PEDIDOS EM ENTREGA
# LISTAGEM DE PEDIDOS
# ENVIA PARA PRODUCAO
# EM PRODUCAO
# FINALIZA PRODUCAO
# ENVIA PARA ENTREGA
# FINALIZA ENTREGA
# OBSERVACAO DE ENTREGA
# FINALIZA PEDIDO
# CARREGA EVENTOS DO PEDIDO
# CARREGA ITEMS DO PEDIDO

    def carregaEvento(self):
        dto = EventoDTO()
        if not dto.lista(self.__Data('id')):
            return False
        
        self.__setData('EventoList', dto.getDataList())
        return True

    def carregaItem(self):
        dto = ItemDTO()
        if not dto.lista(self.__Data('id')):
            return False

        self.__setData('ItemList', dto.getDataList())
        return True

    def enviaProducao (self):
        dto = EventoDTO()
        if not dto.novo("ENVIADO PRODUCAO", self.__Data('id')):
            return False
        return True

    def emProducao (self):
        dto = EventoDTO()
        if not dto.novo("EM PRODUCAO", self.__Data('id')):
            return False
        return True


    def finalizaProducao (self):
        dto = EventoDTO()
        if not dto.novo("FINALIZADO PRODUCAO", self.__Data('id')):
            return False

        return True

    def enviaEntrega (self):
        dto = EventoDTO()
        if not dto.novo("ENVIADO ENTREGA", self.__Data('id')):
            return False
        return True

    def finalizaEntrega (self):
        dto = EventoDTO()
        if not dto.novo("FINALIZA ENTREGA", self.__Data('id')):
            return False
        return True

    def encerra (self):
        stmt = 'update pedido set concluido = True where id = %s'
        Dados = self.db.execute(stmt, (entregador, pedido))
        if not Dados['Result']:
            self.Error = Dados['Error']
            return False

        dto = EventoDTO()
        if not dto.novo("PEDIDO CONCLUIDO", self.__Data('id')):
            return False
        return True

    def entregador (self, entregador, pedido): 
        self.__setData('id', pedido)
        self.__setData('Entregador', entregador)

        stmt = 'update pedido set entregador = %s where id = %s and concluido = FALSE returning ' + self.__columns()
        Dados = self.db.execute(stmt, (entregador, pedido))
        if not Dados['Result']:
            self.Error = Dados['Error']
            return False

        column = 0
        for dtfield in self.__Data.keys():
            self.__setData(dtfield, Dados['Data'][column])
            column += 1

        dto = EventoDTO()
        if not dto.novo("ACRESCENTADO ENTREGADOR", self.__Data('id')):
            return False

        return True


    def novo (self, cliente):
        stmt = 'insert into pedido (cliente) values (%s) returning id'
        Dados = self.db.execute(stmt, (cliente,))
        if not Dados['Result']:
            self.Error = Dados['Error']
            return False
        
        self.__setData('id', Dados['Data'][0])

        dto = EventoDTO()
        if not dto.novo("PEDIDO ACEITO", self.__Data['id']):
            self.Error = dto.Error
            return False

        return True

    def remove (self, pedido):
        stmt = 'delete from pedido where id = %s'
        Dados = self.db.execute(stmt, (pedido, pedido))
        if not Dados['Result']:
            self.Error = Dados['Error']
            return False

        return True

    def desconto (self, desconto, pedido):
        stmt = 'update pedido set desconto = %s, total = (valor - desconto + entrega) where id = %s and concluido = FALSE returning ' + self.__columns()
        Dados = self.db.execute(stmt, (desconto, pedido))
        if not Dados['Result']:
            self.Error = Dados['Error']
            return False

        column = 0
        for dtfield in self.__Data.keys():
            self.__setData(dtfield, Dados['Data'][column])
            column += 1

        dto = EventoDTO()
        if not dto.novo("ACRESCENTADO DESCONTO", self.__Data('id')):
            return False

        return True
    
    def entrega (self, entrega, pedido):
        stmt = 'update pedido set entrega = %s, total = (valor - desconto + entrega where id = %s and concluido = FALSE returning ' + self.__columns()
        Dados = self.db.execute(stmt, (entrega, pedido))
        if not Dados['Result']:
            self.Error = Dados['Error']
            return False

        column = 0
        for dtfield in self.__Data.keys():
            self.__setData(dtfield, Dados['Data'][column])
            column += 1
        
        dto = EventoDTO()
        if not dto.novo("ACRESCENTADO VALOR ENTREGA", self.__Data('id')):
            return False

        return True
    
    def observacaoEntrega (self, observacao, pedido):
        stmt = 'update pedido set observacao_entrega = %s where id = %s and concluido = FALSE returning ' + self.__columns()
        Dados = self.db.execute(stmt, (observacao, pedido))
        if not Dados['Result']:
            self.Error = Dados['Error']
            return False

        column = 0
        for dtfield in self.__Data.keys():
            self.__setData(dtfield, Dados['Data'][column])
            column += 1
        
        dto = EventoDTO()
        if not dto.novo("ACRESCENTADO OBSERVACAO ENTREGA", self.__Data('id')):
            return False

        return True

    def mostra (self, pedido):
        stmt = f"select {self.__columns()} from pedido where id = %s"
        Dados = self.db.queryOne(stmt, (pedido,))
        if not Dados['Result']:
            self.Error = Dados['Error']
            return False

        column = 0
        for dtfield in self.__Data.keys():
            self.__setData(dtfield, Dados['Data'][column])
            column += 1

        if not self.carregaItem():
            return False

        if not self.carregaEvento():
            return False

        return True

    def listaAberto(self):
        self.__DataList = []
        stmt = f"select {self.__columns()} from pedido where concluido = False order by id"
        Dados = self.db.queryAll(stmt, None)
        if not Dados['Result']:
            self.Error = Dados['Error']
            return False

        for tupleInList in Dados['Data']:
            self.__setDataList(tupleInList)

        return True
