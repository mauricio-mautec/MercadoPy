from datetime import date, datetime
import importlib
from utility import konstantes
database_DB = konstantes('DATABASE','database_DB')
banco       = importlib.import_module (database_DB)

# TRABALHA OS ITENS QUE COMPOEM UM PEDIDO DE VENDA
from api.pedido.ItemDTO           import ItemDTO
from api.pedido.Item_EstoqueDTO   import Item_EstoqueDTO
from api.pedido.EventoDTO         import EventoDTO
from api.artigo.ArtigoDTO         import ArtigoDTO
from api.produto.ProdutoDTO       import ProdutoDTO

class PedidoDTO():
# METODOS COMUNS

    def __init__(self):
        self.__resetData()
        self.__DataList = []
        self.Error        = ''
        self.db           = banco.AccessDB()
        self.item         = ItemDTO()
        self.item_estoque = Item_EstoqueDTO()
        self.evento       = EventoDTO()
        self.artigo       = ArtigoDTO()

    def __resetData (self):
        # DADOS EXPOSTOS DTO
        # INFORMACAO QUE O DTO PRECISA TRABALHAR/FORNECER
        self.__Data = {
            'id'                 : 0,
            'Cliente'            : 0,
            'Loja'               : 0,
            'Entrada'            : '',
            'Pagamento_Troco'    : '', 
            'Valor'              : 0.0, 
            'Desconto'           : 0.00,
            'Entrega'            : 0.00,
            'Total'              : 0.00,
            'Entregador'         : 0,
            'Concluido'          : False,
            'Observacao_Entrega' : '' }

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
            if isinstance(tupleData[datacol], (date, datetime)):
                self.__Data[field] = tupleData[datacol].isoformat()
            else:    
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
    def getItemDataField (self, datum):
        return self.item.getDataField(datum)

    def getItemData (self):
        return self.item.getData()

    def getItemDataList (self):
        return self.item.getDataList()
#   
    def getEventoDataField (self, datum):
        return self.evento.getDataField(datum)

    def getEventoData (self):
        return self.evento.getData()

    def getEventoDataList (self):
        return self.evento.getDataList()
#   
    def getArtigoDataField (self, datum):
        return self.artigo.getDataField(datum)

    def getArtigoData (self):
        return self.artigo.getData()

    def getArtigoDataList (self):
        return self.artigo.getDataList()
#   
    def getItemEstoqueDataField (self, datum):
        return self.item_estoque.getDataField(datum)

    def getItemEstoqueData (self):
        return self.item_estoque.getData()

    def getItemEstoqueDataList (self):
        return self.item_estoque.getDataList()

# METODOS ESPECIFICOS
# CRIAR NOVO PEDIDO PARA O CLIENTE - PEDIDO INICIO
# REMOVER PEDIDO
# APRESENTAR ITENS A VENDA
# FECHAR PEDIDO - CONFERE DISPONIBILIDADE DOS ARTIGOS
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
        if not self.evento.lista(self.__Data['id']):
            self.Error = self.evento.Error
            return False
        return True

    def carregaItem(self):
        if not self.item.lista(self.__Data['id']):
            self.Error = self.item.Error
            return False
        return True

# EVENTOS
##################################################################################
    def enviaProducao (self):
        if not self.evento.novo("ENVIADO PRODUCAO", self.__Data['id']):
            self.Error = self.evento.Error
            return False
        return True

    def emProducao (self):
        if not self.evento.novo("EM PRODUCAO", self.__Data['id']):
            self.Error = self.evento.Error
            return False
        return True

    def finalizaProducao (self):
        if not self.evento.novo("FINALIZADO PRODUCAO", self.__Data['id']):
            self.Error = self.evento.Error
            return False
        return True

    def enviaEntrega (self):
        if not self.evento.novo("ENVIADO ENTREGA", self.__Data['id']):
            self.Error = self.evento.Error
            return False
        return True

    def finalizaEntrega (self):
        if not self.evento.novo("FINALIZA ENTREGA", self.__Data['id']):
            self.Error = self.evento.Error
            return False
        return True

    def encerra (self):
        stmt   = 'update pedido set concluido = True where id = %s'
        pedido = self.__Data['id']
        Dados  = self.db.execute(stmt, (pedido,))
        if not Dados['Result']:
            self.Error = Dados['Error']
            return False

        if not self.evento.novo("PEDIDO CONCLUIDO", self.__Data['id']):
            self.Error = self.evento.Error
            return False

        return True

    def atualizaValor (self):
        pedido = self.__Data['id']
        stmt = 'select sum(valor) from pedido_item where pedido = %s'
        Dados  = self.db.execute(stmt, (pedido, ))
        if not Dados['Result']:
            self.Error = Dados['Error']
            return False
        valor = Dados['Data'][0][0]
        stmt = 'update pedido set valor = %s, total = (%s - desconto + entrega) where id = %s and concluido =  FALSE returning ' + self.__columns()
        Dados  = self.db.execute(stmt, (valor, valor, pedido))
        if not Dados['Result']:
            self.Error = Dados['Error']
            return False
        
        column = 0
        for dtfield in self.__Data.keys():
            self.__setData(dtfield, Dados['Data'][0][column])
            column += 1

        return True

# SET METODOS
##################################################################################
    def entregador (self, entregador, pedido): 
        self.__setData('id', pedido)
        self.__setData('Entregador', entregador)

        stmt = 'update pedido set entregador = %s where id = %s and concluido = FALSE returning ' + self.__columns()
        Dados = self.db.execute(stmt, (entregador, pedido))
        if not Dados['Result']:
            self.Error = Dados['Error']
            return False

        if Dados['Data'] != None:
            column = 0
            for dtfield in self.__Data.keys():
                self.__setData(dtfield, Dados['Data'][0][column])
                column += 1
        else:
             self.Error = f"ENTREGADOR NAO APLICADO AO PEDIDO [{pedido}]"
             return False

        if not self.evento.novo("ACRESCENTADO ENTREGADOR", self.__Data['id']):
            self.Error = self.evento.Error
            return False

        return True

    def desconto (self, desconto, pedido):
        if not self.mostra(pedido):
            return False 

        stmt = 'update pedido set desconto = %s, total = (valor - %s + entrega) where id = %s and concluido = FALSE returning ' + self.__columns()
        Dados = self.db.execute(stmt, (desconto, desconto, pedido))
        if not Dados['Result']:
            self.Error = Dados['Error']
            return False

        if Dados['Data'] != None:
            column = 0
            for dtfield in self.__Data.keys():
                self.__setData(dtfield, Dados['Data'][0][column])
                column += 1
        else:
            self.Error = f"DESCONTO NAO APLICADO AO PEDIDO [{pedido}]"
            return False

        if not self.evento.novo("ACRESCENTADO DESCONTO", self.__Data['id']):
            self.Error = self.evento.Error
            return False

        return True
    
    def entrega (self, entrega, pedido):
        if not self.mostra(pedido):
            return False 

        stmt = 'update pedido set entrega = %s, total = (valor - desconto + %s) where id = %s and concluido = FALSE returning ' + self.__columns()
        Dados = self.db.execute(stmt, (entrega, entrega, pedido))
        if not Dados['Result']:
            self.Error = Dados['Error']
            return False

        if Dados['Data'] != None:
            column = 0
            for dtfield in self.__Data.keys():
                self.__setData(dtfield, Dados['Data'][0][column])
                column += 1
        else:
             self.Error = f"ENTREGA NAO APLICADA AO PEDIDO [{pedido}]"
             return False

        if not self.evento.novo("ACRESCENTADO VALOR ENTREGA", self.__Data['id']):
            self.Error = self.evento.Error
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
            self.__setData(dtfield, Dados['Data'][0][column])
            column += 1
        
        if not self.evento.novo("ACRESCENTADO OBSERVACAO ENTREGA", self.__Data['id']):
            self.Error = self.evento.Error
            return False

        return True

    def aceitaPedido (self, pedido):
        # CONSULTAR EM PEDIDO_ITEM_ESTOQUE A DISPONIBILIDADE
        # ATUALIZAR ESTOQUE VENDA RETIRANDO CADA ARTIGO
        # FECHAR O PEDIDO
        # ENVIAR PARA PRODUCAO
        return True
       
# CREATE DESTROY METHODS
##################################################################################
    def novo (self, cliente, loja):
        stmt = 'insert into pedido (cliente, loja) values (%s, %s) returning id'
        Dados = self.db.execute(stmt, (cliente, loja))
        if not Dados['Result']:
            self.Error = Dados['Error']
            return False
        
        self.__setData('id', Dados['Data'][0][0])

        if not self.evento.novo("PEDIDO INICIADO", self.__Data['id']):
            self.Error = self.evento.Error
            return False

        return True

    def remove (self, pedido):
        if not self.evento.novo("PEDIDO REMOVIDO", pedido):
            self.Error = self.evento.Error + " MAS OQUE ISSO"
            return False

        stmt = 'insert into pedido_historico (pedido, data, evento) select pedido, data, evento from pedido_evento where pedido = %s'
        Dados = self.db.execute(stmt, (pedido,))
        if not Dados['Result']:
            self.Error = Dados['Error']
            return False

        stmt = 'delete from pedido where id = %s'
        Dados = self.db.execute(stmt, (pedido,))
        if not Dados['Result']:
            self.Error = Dados['Error']
            return False

        self.__resetData()
        self.__DataList = []
        return True

    def novoItem (self, Pedido, Artigo, Quantidade):
        if not self.mostra(Pedido):
            return False

        if not self.artigo.mostra(Artigo):
            return False
        
        funcao = self.artigo.getDataField('Funcao')
        if funcao is None:
            self.Error = "ARTIGO SEM FUNCAO"
            return False
        
        Loja  = self.getDataField('Loja')
        Valor = float(self.artigo.getDataField('Valor_Venda'))
        if Valor <= 0:
            self.Error = "ARTIGO SEM VALOR DE VENDA"
            return False

        if funcao == 'VENDA':
            disponivel, qtd = self.artigo.disponivelEstoque(Loja, Artigo)

            if not disponivel:
                self.Error = f"ARTIGO {Artigo} INDISPONIVEL"
                self.Error = self.artigo.Error
                return False

            if qtd is None or qtd < Quantidade:
                self.Error = f"LOJA {Loja} ARTIGO {Artigo} QTD {qtd} INSUFICIENTE"
                return False

                
            if not self.item.novo(Pedido, Artigo, Quantidade, Valor):
                self.Error = self.item.Error
                return False
            
            pedidoItem = self.item.getDataField('id')
            if not self.item_estoque.novo(pedidoItem, Artigo, Quantidade):
                self.Error = self.item_estoque.Error
                return False

            if not self.atualizaValor():
                return False

            if not self.evento.novo("ACRESCENTADO ITEM VENDA", self.__Data['id']):
                self.Error = self.evento.Error
                return False

            return True

        if funcao == 'VENDA PRODUTO':
            produto = ProdutoDTO()
            if not produto.mostraArtigo (Artigo):
                self.Error = produto.Error
                return False

            if not self.item.novo(Pedido, Artigo, Quantidade, Valor):
                return False
            
            pedidoItem     = self.item.getDataField('id')
            produtoArtigos = produto.getProdutoArtigoDataList()

            for produtoArtigo in produtoArtigos:
                disponivel, qtd = self.artigo.disponivelEstoque(Loja, produtoArtigo['Artigo'])
                if not disponivel or qtd < produtoArtigo['Quantidade']:
                    self.Error = f"ESTOQUE VENDA SEM ARTIGO [{produtoArtigo['Artigo']}]"
                    self.item.remove (Pedido, pedidoItem)
                    return False

                if not self.item_estoque.novo(pedidoItem, produtoArtigo['Artigo'], produtoArtigo['Quantidade']):
                    self.Error = self.item_estoque.Error
                    self.item.remove (Pedido, pedidoItem)
                    return False

            if not self.atualizaValor():
                return False

            if not self.evento.novo("ACRESCENTADO ITEM ARTIGO PRODUTO", Pedido):
                self.Error = self.evento.Error
                return False

            return True    

        # teste para o caso de produtos funcao VENDA PRODUTO

        return True

# SHOW METHODS
###############################################################################
    def mostraArtigoVenda(self):
        if not self.artigo.listaFuncao('VENDA'):
            self.Error = self.artigo.Error
            return False
        
        return True

    def mostra (self, pedido):
        self.__resetData()
        stmt = f"select {self.__columns()} from pedido where id = %s"
        Dados = self.db.queryOne(stmt, (pedido,))
        if not Dados['Result']:
            self.Error = Dados['Error']
            return False

        if Dados['Data'] != None:
            column = 0
            for dtfield in self.__Data.keys():
                self.__setData(dtfield, Dados['Data'][column])
                column += 1
        else:
            self.Error = "PEDIDO INEXISTENTE"
            return False

        if not self.carregaItem():
            self.Error = "carregaItem"
            return False

        if not self.carregaEvento():
            self.Error = 'carregaEvento'
            return False

        return True

    def listaAberto(self):
        stmt = f"select {self.__columns()} from pedido where concluido = False order by id"
        Dados = self.db.queryAll(stmt, None)
        if not Dados['Result']:
            self.Error = Dados['Error']
            return False

        self.__DataList = []
        for tupleInList in Dados['Data']:
            self.__setDataList(tupleInList)

        return True
