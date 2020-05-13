import sqlite3
from   utility import konstantes

# CLASSE PARA REPRESENTAR A TECNOLOGIA DE ARMAZENAMENTO UTILIZADO
# CAMADA MAIS ABAIXO DO DTO QUE TEM HAVER COM O DADOS E SEU ARMAZENAMENTO
class AccessDB():
    # DADOS REPRESENTADOS
    #database = "C:\\Users\\mauvi\\python\\mercado\\data\\API.db"
    database = konstantes('SQLITE3', 'database')
    lastrowid = 0
    
    def __init__(self):
        self.Result = False

    def queryOne(self, statement, data):
        Dados = {}
        try:
            Result = True
            conn = sqlite3.connect (self.database)
            curs = conn.cursor()
            stmt = statement
            curs.execute (stmt, data)
            Data = curs.fetchone()
            Dados['Data'] = Data
            conn.commit()
        except:
            Result = False
        
        conn.close()
        Dados['Result'] = Result
        return Dados
        
    def queryAll(self, statement, data):
        Dados = {}
        try:
            Result = True
            conn = sqlite3.connect (self.database)
            curs = conn.cursor()
            stmt = statement
            curs.execute (stmt, data)
            Data = curs.fetchall()
            Dados['Data'] = Data
            conn.commit()
        except:
            Result = False

        conn.close()
        Dados['Result'] = Result
        return Dados   
        
      
    def execute(self, statement, data):
        Dados = {}
        try:
            Result = True
            conn = sqlite3.connect (self.database)
            curs = conn.cursor()
            stmt = statement
            curs.execute (stmt, data)
            self.lastrowid = curs.lastrowid
            conn.commit()

        except sqlite3.Error as error:
            Error  = error.args[0]
            Dados['Error'] = Error
            Result = False
            
        conn.close()           
        Dados['Result'] = Result
        return Dados

'''
            PRAGMA foreign_keys=OFF;
            BEGIN TRANSACTION;
            CREATE TABLE sistema (sUser integer, sTier integer, sSistema text, sURL text);
            CREATE TABLE user (uLogin text, uPassword text, uName text, uAcesso integer);
            CREATE TABLE user_auth (auSistema text,auUser integer,auName text,auAppid text, auToken, auInDate datetime, auCkdate datetime);
            COMMIT;


        
        user_auth = {
            'rowid'       : 0,
            'auSistema'   : '',        # sistema em operacao
            'auUser'      : 0,         # rowid user
            'auName'      : '',        # user.uName
            'auAppid'     : '',        # informacao do cliente acessando a API
            'auToken'     : 0,         # token gerado pelo Login
            'auIndate'    : 0,         # momento da criacao da entrada
            'auCkdate'    : 0 }        # momento do ultimo acesso valido, API vai atualizando essa info

        self.user = {
            'rowid'       : 0,         # codigo user
            'uLogin'      : '',        # Login para acesso
            'uPassword'   : '',        # Password para acesso
            'uName'       : '',        # Nome completo do user
            'uAcesso'     : 0 }        # Contabiliza quantidade de acessos validos
        
        self.sistema = {
            'rowid'       : 0,         # codigo sistema 
            'sUser'       : 0,         # codigo user
            'sTier'       : 1,         # nivel contabil do sistema
            'sSistema'    : '',        # Nome identificado para o sistema
            'sURL'        : '' }       # URL da pagina de venda        
 '''
