from datetime import date, datetime
import importlib
from utility import konstantes
database_DB = konstantes('DATABASE','database_DB')
banco       = importlib.import_module (database_DB)

# TRABALHA OS ITENS QUE COMPOEM UM PRODUTO
from api.produto.ItemDTO   import ItemDTO

class ProdutoDTO():
# METODOS COMUNS

    def __init__(self):
        self.__resetData()
        self.__DataList = []
        self.db     = banco.AccessDB()
        self.item   = ItemDTO()

    def __resetData (self):
        # DADOS EXPOSTOS DTO
        # INFORMACAO QUE O DTO PRECISA TRABALHAR/FORNECER
        self.__Data = {
            'id'                   : 0,
            'Artigo'               : 0,
            'Custo_Final'          : 0.00, 
            'Tempo_Medio_Producao' : 0,
            'Preco_Final'          : 0.00,
            'Ativo'                : True }

    def __columns (self):
        strcol = ' '
        for col in self.__Data.keys():
            strcol += f"{col},"
        return strcol[0:-1]

    def __setData (self, datum, value):
        if datum in list(self.__Data.keys()):
            if isinstance(value, (date, datetime)):
                self.__Data[datum] = value.isoformat()
            else:
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
            return self.__Data[datum]
        else:
            return False

    def getData (self):
        return self.__Data

    def getDataList (self):
        return self.__DataList

    # METODOS PARA TABELAS AUXILIARES
    def getItemDataField (self, datum):
        return self.item.getDataField(datum)

    def getItemData (self):
        return self.item.getData()

    def getItemDataList (self):
        return self.item.getDataList()

# METODOS ESPECIFICOS
# CRIAR NOVO PRODUTO
# REMOVER PRODUTO
# APRESENTAR ITENS
# LISTAR PRODUTOS ATIVOS
# LISTAGEM DE PRODUTOS

    def carregaItem(self):
        if not self.item.lista(self.__Data['id']):
            self.Error = self.item.Error
            return False
        return True


# CREATE DESTROY METHODS
##################################################################################
    def novo (self, cliente):
        stmt = 'insert into pedido (cliente) values (%s) returning id'
        Dados = self.db.execute(stmt, (cliente,))
        if not Dados['Result']:
            self.Error = Dados['Error']
            return False
        
        self.__setData('id', Dados['Data'][0][0])

        if not self.evento.novo("PEDIDO INICIADO", self.__Data['id']):
            self.Error = self.evento.Error
            return False

        return True

    def remove (self, pedido):
        stmt = 'delete from pedido where id = %s'
        Dados = self.db.execute(stmt, (pedido,))
        if not Dados['Result']:
            self.Error = Dados['Error']
            return False

        return True

    def novoItem (self, Produto, Artigo, Quantidade, Essencial, Visivel):
            
        return True


# SHOW METHODS
###############################################################################
    def mostra (self, produto):
        stmt = f"select {self.__columns()} from produto where id = %s"
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

        return True

    def listaAtivo(self):
        self.__DataList = []
        stmt = f"select {self.__columns()} from produto where ativo = True order by id"
        Dados = self.db.queryAll(stmt, None)
        if not Dados['Result']:
            self.Error = Dados['Error']
            return False

        for tupleInList in Dados['Data']:
            self.__setDataList(tupleInList)

        return True
