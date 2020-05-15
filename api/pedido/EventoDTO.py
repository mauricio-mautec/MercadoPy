import datetime
import importlib
from   utility import konstantes
database_DB = konstantes('DATABASE','database_DB')
banco       = importlib.import_module (database_DB)

# TRABALHA OS ITENS QUE COMPOEM UM PEDIDO DE VENDA
class EventoDTO():
# METODOS COMUNS
    def __init__(self):
        self.__resetData()
        self.__DataList = []
        self.db    = banco.AccessDB()

    def __resetData (self):
        # DADOS EXPOSTOS DTO
        # INFORMACAO QUE O DTO PRECISA TRABALHAR/FORNECER
        self.__Data = {
            'id'       : 0,
            'Pedido'   : 0,
            'Data'     : '',
            'Evento'   : '' }

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
# ADDICIONAR NOVO EVENTO
# LISTAR EVENTOS DO PEDIDO

    def novo (self, evento, pedido):
        self.__setData('Pedido',  pedido)
        self.__setData('Evento',  evento)

        stmt = 'insert into pedido_evento (pedido, evento) values (%s, %s) returning id, data'
        Dados = self.db.execute(stmt, (pedido, evento))
        if not Dados['Result']:
            self.Error = Dados['Error']
            return False

        eventoid, data = Dados['Data'][0]
        self.__setData('id',    eventoid)
        self.__setData('Data',  data)
        return True

    def lista (self, pedido):
        self.__DataList = []
        stmt = f'select {self.__columns()} from pedido_evento where pedido = {pedido}'
        Dados = self.db.queryAll(stmt, None)

        if not Dados['Result']:
            return False

        for tupleInList in Dados['Data']:
            self.__setDataList(tupleInList)

        return True
