import datetime
import importlib
from   utility import konstantes
database_DB = konstantes('DATABASE','database_DB')
banco       = importlib.import_module (database_DB)

# TRABALHA OS ITENS QUE COMPOEM UM PEDIDO DE VENDA
class ArtigoDTO():
# METODOS COMUNS
    def __init__(self):
        self.__resetData()
        self.__DataList = []
        self.db    = banco.AccessDB()

    def __resetData (self):
        # DADOS EXPOSTOS DTO
        # INFORMACAO QUE O DTO PRECISA TRABALHAR/FORNECER
        self.__Data = {
            'id'          : 0,
            'Nome'        : '',
            'Grupo'       : '',
            'Funcao'      : '',
            'Valor_Venda' : ''  }

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

    def getDataField (self, datum):
        if datum in list(self.__Data.keys()):
            return self.__Data[datum]
        else:
            return None

    def getData (self):
        return self.__Data

    def getDataList (self):
        return self.__DataList

# METODOS ESPECIFICOS
# ADDICIONAR  ARTIGO
# REMOVER ARTIGO
# LIMPA  TODOS OS ARTIGOS
# ATUALIZA ARTIGO

    def novo (self, nome, grupo, funcao):
        self.__setData('Nome',      nome)
        self.__setData('Grupo',     grupo)
        self.__setData('Funcao',    funcao)

        stmt = 'insert into artigo (nome, grupo, funcao) values (%s, %s, %s) returning id'

        Dados = self.db.execute(stmt, (nome, grupo, funcao))
        if not Dados['Result']:
            self.Error = Dados['Error']
            return False

        artigoId = Dados['Data'][0][0] # {'Data' : [(id,)]}
        self.__setData('id', artigoId)

        return True

    def remove (self, artigo):
        self.__resetData()
        stmt = 'delete from artigo where id = %s'
        Dados = self.db.execute(stmt, (artigo,))
        if not Dados['Result']:
            self.Error = Dados['Error']
            return False
        return True
    
    def atualiza (self, artigo, nome, grupo, funcao):
        self.__setData('id',       artigo)
        self.__setData('Nome',     nome)
        self.__setData('Grupo',    grupo)
        self.__setData('Funcao',    funcao)
        stmt = 'update artigo (nome, grupo, funcao) values (%s, %s, %s) where id = %s'
        Dados = self.db.execute(stmt, (nome, grupo, funcao, artigo))
        if not Dados['Result']:
            self.__resetData()
            self.__DataList = []
            self.Error = Dados['Error']
            return False
        return True        

    def mostra (self, artigo):
        self.__resetData()
        stmt = f'select {self.__columns()} from artigo where id = {artigo}' 
        Dados = self.db.queryOne(stmt, None)
        if not Dados['Result']:
            self.Error = Dados['Error']
            return False
        

        col = 0
        for key in self.__Data.keys():
            self.__setData(key, Dados['Data'][col])
            col += 1

        return True

    def lista (self, pedido):
        self.__DataList = []
        stmt = f'select {self.__columns()} from artigo'
        Dados = self.db.queryAll(stmt, None)

        if not Dados['Result']:
            self.Error = Dados['Error']
            return False

        for tupleInList in Dados['Data']:
            self.__setDataList(tupleInList)

        return True
    
    def listaFuncao (self, funcao):
        self.__DataList = []
        stmt = f"select {self.__columns()} from artigo where funcao like '%{funcao}%' order by id" 
        Dados = self.db.queryAll(stmt, None)

        if not Dados['Result']:
            self.Error = Dados['Error']
            return False

        for tupleInList in Dados['Data']:
            self.__setDataList(tupleInList)

        return True
    
    def listaGrupo (self, grupo):
        self.__DataList = []
        stmt = f"select {self.__columns()} from artigo where grupo like '%{grupo}%'" 
        Dados = self.db.queryAll(stmt, None)

        if not Dados['Result']:
            self.Error = Dados['Error']
            return False

        for tupleInList in Dados['Data']:
            self.__setDataList(tupleInList)

        return True

    def disponivelEstoque(self, loja, artigo):
        hoje = datetime.date.today().isoformat()
        stmt = f"select sum(disponivel) from estoque_venda where loja = {loja} and artigo = {artigo} and validade >= '{hoje}' and disponivel > 0"
        Dados = self.db.queryAll(stmt, None)

        if not Dados['Result']:
            self.Error = Dados['Error']
            return (False, 0)

        qtd = Dados['Data'][0][0]
        if qtd == None: qtd = 0
        
        result = (True, qtd)

        return result
