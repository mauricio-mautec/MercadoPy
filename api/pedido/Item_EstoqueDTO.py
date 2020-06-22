import datetime
import importlib
from   utility import konstantes
database_DB = konstantes('DATABASE','database_DB')
banco       = importlib.import_module (database_DB)

# RELACIONA OS ITENS QUE COMPOEM UM PEDIDO DE VENDA
class Item_EstoqueDTO():
# METODOS COMUNS
    def __init__(self):
        self.__resetData()
        self.__DataList = []
        self.db    = banco.AccessDB()

    def __resetData (self):
        # DADOS EXPOSTOS DTO
        # INFORMACAO QUE O DTO PRECISA TRABALHAR/FORNECER
        self.__Data = {
            'id'             : 0,
            'Pedido_Item'    : 0,
            'Artigo'         : 0,
            'Quantidade'     : 0 } 

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

    def getData (self, datum):
        if datum in list(self.__Data.keys()):
            return self.__Data[datum][1]
        else:
            return False

    def getData (self):
        return self.__Data

    def getDataList (self):
        return self.__DataList

# METODOS ESPECIFICOS
# ADDICIONAR ITEM NO PEDIDO
# REMOVER ITEM DO PEDIDO
# LIMPA  TODOS OS ITEM DO PEDIDO
# ATUALIZA PEDIDO
# LISTAR ITENS DO PEDIDO

    def novo (self, pedido_item, artigo, quantidade):
        self.__setData('Pedido_Item',    pedido_item)
        self.__setData('Artigo',         artigo)
        self.__setData('Quantidade',     quantidade)

        stmt = 'insert into pedido_item_estoque (pedido_item, artigo, quantidade) values (%s, %s, %s) returning id'
        Dados = self.db.execute(stmt, (pedido_item, artigo, quantidade))
        if not Dados['Result']:
            self.Error = Dados['Error']
            return False
       
        ItemEstoqueID = Dados['Data'][0][0] # { "Data": [ (ID, ), ] }
        self.__setData('id', ItemEstoqueID)

        return True

    def remove (self, pedido_item_estoque):
        self.__resetData()
        stmt = 'delete from pedido_item_estoque where id = %s'
        Dados = self.db.execute(stmt, (pedido_item_estoque,))
        if not Dados['Result']:
            self.Error = Dados['Error']
            return False
        return True
    
    def atualiza (self, pedido_item_estoque, pedido_item, artigo, quantidade):
        self.__setData('id', item)
        self.__setData('Pedido_Item',   pedido_item)
        self.__setData('Artigo',        artigo)
        self.__setData('Quantidade',    quantidade)
        stmt = 'update pedido_item_estoque (pedido_item, artigo, quantidade) values (%s, %s, %s) where id = %s'
        Dados = self.db.execute(stmt, (pedido_item, artigo, quantidade, pedido_item_estoque))
        if not Dados['Result']:
            self.__resetData()
            self.__DataList = []
            self.Error = Dados['Error']
            return False
        return True        

    def limpa (self, pedido_item):
        self.__resetData()
        stmt = 'delete from pedido_item_estoque where pedido_item = %s'
        Dados = self.db.execute(stmt, (pedido_item,))
        if not Dados['Result']:
            self.Error = Dados['Error']
            return False
        return True

    def lista (self, pedido_item):
        self.__DataList = []
        stmt = f'select {self.__columns()} from pedido_item_estoque where pedido_item = {pedido_item}'
        Dados = self.db.queryAll(stmt, None)

        if not Dados['Result']:
            self.Error = Dados['Error']
            return False

        for tupleInList in Dados['Data']:
            self.__setDataList(tupleInList)

        return True
