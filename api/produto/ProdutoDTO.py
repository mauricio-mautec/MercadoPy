from datetime import date, datetime
import importlib
from utility import konstantes
database_DB = konstantes('DATABASE','database_DB')
banco       = importlib.import_module (database_DB)

# TRABALHA OS ITENS QUE COMPOEM UM PRODUTO
from api.produto.Produto_ArtigoDTO   import Produto_ArtigoDTO

class ProdutoDTO():
# METODOS COMUNS

    def __init__(self):
        self.__resetData()
        self.__DataList     = []
        self.db             = banco.AccessDB()
        self.artigo = Produto_ArtigoDTO()

    def __resetData (self):
        # DADOS EXPOSTOS DTO
        # INFORMACAO QUE O DTO PRECISA TRABALHAR/FORNECER
        self.__Data = {
            'id'                   : 0,
            'Artigo'               : 0,
            'Custo_Final'          : 0.00, 
            'Tempo_Medio_Producao' : 0,
            'Preco_Final'          : 0.00,
            'Image'                : '',
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
            self.__Data[field] = tupleData[datacol]
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
    def getProdutoArtigoDataField (self, datum):
        return self.artigo.getDataField(datum)

    def getProdutoArtigoData (self):
        return self.artigo.getData()

    def getProdutoArtigoDataList (self):
        return self.artigo.getDataList()

# METODOS ESPECIFICOS
# CRIAR NOVO PRODUTO
# REMOVER PRODUTO
# APRESENTAR ITENS
# LISTAR PRODUTOS ATIVOS
# LISTAGEM DE PRODUTOS

    def carregaProdutoArtigo(self):
        if not self.artigo.lista(self.__Data['id']):
            self.Error = self.artigo.Error
            return False
        return True


# CREATE DESTROY METHODS
##################################################################################
    def novo (self, artigo):
        stmt = 'insert into produto (artigo) values (%s) returning id'
        Dados = self.db.execute(stmt, (cliente,))
        if not Dados['Result']:
            self.Error = Dados['Error']
            return False
        
        self.__setData('id', Dados['Data'][0][0])
        return True

    def remove (self, produto):
        stmt = 'delete from produto where id = %s'
        Dados = self.db.execute(stmt, (produto,))
        if not Dados['Result']:
            self.Error = Dados['Error']
            return False

        return True

    def novoArtigo (self, Produto, Artigo, Quantidade, Essencial, Visivel):
        if not self.mostra(Produto):
            return False

        return True


# SHOW METHODS
###############################################################################
    def mostra (self, produto):
        stmt = f"select {self.__columns()} from produto where id = %s"
        
        Dados = self.db.queryOne(stmt, (produto,))
        if not Dados['Result']:
            self.Error = Dados['Error']
            return False

        data = Dados['Data']
        if data is None:
            self.Error = "PRODUCT NOT FOUND"
            return False

        column = 0
        for dtfield in self.__Data.keys():
            self.__setData(dtfield, data[column])
            column += 1

        if not artigo.lista(produto):
            self.Error = artigo.Error
            return False

        return True
    
    def mostraArtigo (self, artigo):
        stmt = f"select {self.__columns()} from produto where artigo = %s"
       
        Dados = self.db.queryOne(stmt, (artigo,))
        if not Dados['Result']:
            self.Error = Dados['Error']
            return False

        data = Dados['Data']
        if data is None:
            self.Error = "PRODUCT NOT FOUND"
            return False

        column = 0
        for dtfield in self.__Data.keys():
            self.__setData(dtfield, data[column])
            column += 1

        produto = self.getDataField('id')
        if not self.artigo.lista(produto):
            self.Error = self.artigo.Error
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
