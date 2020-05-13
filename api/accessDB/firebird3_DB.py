import fdb
from utility import konstantes
# CLASSE PARA REPRESENTAR A TECNOLOGIA DE ARMAZENAMENTO UTILIZADO
# CAMADA MAIS ABAIXO DO DTO QUE TEM HAVER COM O DADOS E SEU ARMAZENAMENTO
class AccessDB(object):
    # DADOS REPRESENTADOS
    database = konstantes('FIREBIRD3', 'database')
    userDB   = konstantes('FIREBIRD3', 'userDB')
    userPW   = konstantes('FIREBIRD3', 'userPW')

    def __init__(self):

    def queryOne(self, stmt, data):
        Dados = {}
        try:
            Result = True
            conn = fdb.connect (dsn = self.database, user = self.userDB, password = self.userPW)
            curs = conn.cursor()
            conn.begin()
            curs.execute (stmt, data)
            Data = curs.fetchone()
            Dados['Data'] = Data
            conn.commit()

        except:
            Result = False

        conn.close()
        Dados['Result'] = Result
        return Dados


    def queryAll(self, stmt, data):
        Dados = {} 
        try:
            conn = fdb.connect (dsn = self.database, user = self.userDB, password = self.userPW)
            curs = conn.cursor()
            conn.begin()
            curs.execute (stmt, data)
            Data = curs.fetchall()
            conn.commit()
            Result = True;
        
        except fdb.Error as error:
            Error  = error.args[0]
            Dados['Error'] = Error
            Result = False
        
        conn.close()
        Dados['Result'] = Result
        return Dados
    
    def execute(self, stmt, data):
        Dados = {} 
        try:
            conn = fdb.connect (dsn = self.database, user = self.userDB, password = self.userPW)
            curs = conn.cursor()
            conn.begin()
            curs.execute (stmt, data)
            conn.commit()
            Result = True;
        
        except fdb.Error as error:
            Error  = error.args[0]
            Dados['Error'] = Error
            Result = False
        
        conn.close()
        Dados['Result'] = Result
        return Dados
