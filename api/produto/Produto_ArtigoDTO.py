import importlib
from   utility import konstantes
database_DB = konstantes('DATABASE','database_DB')
banco       = importlib.import_module (database_DB)

'''
TRABALHA OS ITENS QUE COMPOEM UM PRODUTO DE VENDA
'''
class Produto_ArtigoDTO():
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
            'Produto'        : 0,
            'Artigo'         : 0,
            'Quantidade'     : 0, 
            'Essencial'      : True,
            'Visivel_Pedido' : False,
            'Custo'          : 0.00 }

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
            self.__Data[field] = tupleData[datacol]
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

    def novo (self, produto, artigo, quantidade):
        self.__setData('Produto',       produto)
        self.__setData('Artigo',        artigo)
        self.__setData('Quantidade',    quantidade)
        self.__setData('Custo',         custo)

        stmt = 'insert into produto_artigo (produto, artigo, quantidade) values (%s, %s, %s) returning id'
        Dados = self.db.execute(stmt, (produto, artigo, quantidade))
        if not Dados['Result']:
            self.Error = Dados['Error']
            return False
        
        self.__setData('id', Dados[0])

        return True

    def remove (self, produto, artigo):
        self.__resetData()
        stmt = 'delete from produto_artigo where produto  = %s and artigo = %s'
        Dados = self.db.execute(stmt, (pedido, item))
        if not Dados['Result']:
            self.Error = Dados['Error']
            return False
        return True
    
    def atualiza (self, produto_artigo, produto, artigo, quantidade, essencial = True, visivel_pedido = False):
        self.__setData('id',             item)
        self.__setData('Produto',        produto)
        self.__setData('Artigo',         artigo)
        self.__setData('Quantidade',     quantidade)
        self.__setData('Essencia',       essencial)
        self.__setData('Visivel_Pedido', visivel_pedido)
        stmt = 'update produto_artigo (produto, artigo, quantidade, essencia, visivel_pedido) values (%s, %s, %s, %s, %s) where id = %s'
        Dados = self.db.execute(stmt, (produto, artigo, quantidade, essencial, visivel_pedido, produto_artigo))
        if not Dados['Result']:
            self.__resetData()
            self.__DataList = []
            self.Error = Dados['Error']
            return False
        return True        

    def limpa (self, produto):
        self.__resetData()
        stmt = 'delete from produto_artigo where produto = %s'
        Dados = self.db.execute(stmt, (pedido, item))
        if not Dados['Result']:
            self.Error = Dados['Error']
            return False
        return True

    def lista (self, produto):
        self.__DataList = []
        stmt = f'select {self.__columns()} from produto_artigo where produto = {produto}'
        Dados = self.db.queryAll(stmt, None)

        if not Dados['Result']:
            self.Error = Dados['Error']
            return False

        for tupleInList in Dados['Data']:
            self.__setDataList(tupleInList)

        return True
