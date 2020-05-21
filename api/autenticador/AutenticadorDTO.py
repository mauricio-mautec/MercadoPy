import datetime
import importlib
from utility import *

database_DB = konstantes('DATABASE','database_DB')
banco = importlib.import_module (database_DB)
  
class AutenticadorDTO():
# METODOS COMUNS

    def __init__(self):
        self.__resetData()
        self.db    = banco.AccessDB()
        self.Error = ''

    def __resetData (self):
        # DADOS EXPOSTOS DTO
        # INFORMACAO QUE O DTO PRECISA TRABALHAR/FORNECER
        self.__Data = {
            'AuthID'             : 0,
            'UserID'             : 0,
            'Nome'               : '',
            'Numero_Acessos'     : 0, 
            'Ultimo_Acesso'      : '',
            'Sistemas_Atendidos' : {} }

    def __setData (self, datum, value):
        if datum in list(self.__Data.keys()):
            self.__Data[datum] = value

    def getDataField (self, datum):
        if datum in list(self.__Data.keys()):
            return self.__Data[datum][1]
        else:
            return False

    def getData (self):
        return self.__Data

# METODOS ESPECIFICOS
    def getUserInfo (self, Login, Password):
        stmt = 'SELECT id, nome, email, qtd_acesso, ultimo_acesso FROM usuario WHERE email = %s AND senha = %s'
        Dados = self.db.queryOne(stmt, (Login, Password))
        if not Dados['Result']:
            return False

        if Dados['Data'] != None:   
            self.__Data['UserID']         = Dados['Data'][0]
            self.__Data['Nome']           = Dados['Data'][1]
            self.__Data['email']          = Dados['Data'][2]
            self.__Data['Numero_Acessos'] = Dados['Data'][3]
            self.__Data['Ultimo_Acesso']  = Dados['Data'][4]
        else:    
            return False
        
        stmt = 'SELECT US.id, S.nome, S.url FROM sistema S JOIN usuario_sistema US ON US.sistema = S.id WHERE US.usuario = %s'
        Dados = self.db.queryAll(stmt, (self.__Data['UserID'],))
        if not Dados['Result']:
            return False

        self.__Data['Sistemas_Atendidos'] = '{}'
        if Dados['Data']:
            Relacao = { datum[0]: [datum[1], datum[2]] for datum in Dados['Data'] }
            self.__Data['Sistemas_Atendidos'] = Relacao

        return True


    def setUserAuth (self, Login, Password, Appid, Sistema, Token): 
        Result = self.getUserInfo (Login, Password)
        if not Result:
            return False
            
        if Sistema not in self.__Data['Sistemas_Atendidos']:
            return False
  
        Appids = "{}".format(Appid)
        
        stmt = 'INSERT INTO acesso(usuario_sistema, token, appid) VALUES  (%s,%s,%s) RETURNING id'
        dados = (Sistema, Token, Appids)
        Dados = self.db.queryOne (stmt, dados)

        if not Dados['Result']:
            self.Error = Dados['Error']
            return False

        if Dados['Data']:
            self.__setData('AuthID' , Dados['Data'][0])

        return True

    def updateAuth (self, authid, last_check_api):
        stmt = f'UPDATE acesso set last_check = CURRENT_TIMESTAMP, last_check_api = %s WHERE id = {authid} RETURNING last_check'
        Dados = self.db.queryOne(stmt, (last_check_api,))
        if Dados['Result']:
            self.__setData('Ultimo_Acesso', Dados['Data'])
            return True
        else:
            self.Error = Dados['Error']
            return False

# VERIFICA EXISTE UM TOKEN VALIDO COM TEMPO MENOR
# QUE MAXAGE
    def checkValidAccess (self, authid, userid, maxage):
        stmt = "select us.usuario from acesso a join usuario_sistema us on us.id = a.usuario_sistema where a.id = %s and EXTRACT (EPOCH from (current_timestamp - a.last_check)) < %s"
        Dados = self.db.queryOne(stmt, (authid, maxage))
        if not Dados['Result']:
            self.Error = Dados['Error']
            return False
        
        if Dados['Data'] and Dados['Data'][0] == userid:
            return True
        else:
            return False
