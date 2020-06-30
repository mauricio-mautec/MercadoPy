import psycopg2
import psycopg2.extras
from   utility import konstantes

# CLASSE PARA REPRESENTAR A TECNOLOGIA DE ARMAZENAMENTO UTILIZADO
# CAMADA MAIS ABAIXO DO DTO QUE TEM HAVER COM O DADOS E SEU ARMAZENAMENTO
class AccessDB():
    # DADOS REPRESENTADOS
    def __init__(self):
        self.database  = konstantes('POSTGRES', 'database')
        psycopg2.extras.register_uuid()
        self.Dados = {}
        try:
            self.conn = psycopg2.connect (self.database)
            self.connected = True 

        except (Exception, psycopg2.Error) as error:
            self.Dados['Error']  = error
            self.Dados['Result'] = False
            raise Exception(error)
        
        self.conn.close()

    def queryOne(self, stmt, data):
        try:
            conn = psycopg2.connect (self.database) 
            curs = conn.cursor()
            if data == None:
                curs.execute(stmt)
            else:
                curs.execute (stmt, data)
            self.Dados['Data'] = curs.fetchone()
            conn.commit()
            Result = True

        except psycopg2.Error as error:
            self.Dados['Error'] = error.pgerror
            Result = False

        conn.close()
        self.Dados['Result'] = Result
        return self.Dados


    def queryAll(self, stmt, data):
        try:
            conn = psycopg2.connect (self.database)
            curs = conn.cursor()
            if data == None:
                curs.execute(stmt)
            else:
                curs.execute (stmt, data)
            data = curs.fetchall()
            self.Dados['Data'] = data
            conn.commit()
            Result = True
        
        except psycopg2.Error as error:
            self.Dados['Error'] = error.pgerror
            Result = False
        
        conn.close()
        self.Dados['Result'] = Result
        return self.Dados
    
    def execute(self, stmt, data):
        try:
            conn = psycopg2.connect (self.database)
            curs = conn.cursor()
            if data == None:
                curs.execute(stmt)
            else:
                curs.execute (stmt, data)

            hasData = curs.description != None
            if hasData and (curs.rowcount > 0):
                self.Dados['Data'] = curs.fetchall()
            else:
                self.Dados['Data'] = None

            conn.commit()
            Result = True
        
        except psycopg2.Error as error:
            self.Dados['Error'] = error.pgerror
            Result = False
        
        conn.close()
        self.Dados['Result'] = Result
        return self.Dados
    
    def executeManyStart(self):
        try:
            self.conn = psycopg2.connect (self.database)
            self.curs = self.conn.cursor()
            self.Dados['Result'] = True
        
        except psycopg2.Error as error:
            self.Dados['Error']  = error.pgerror
            self.Dados['Result'] = False
        
        return self.Dados
    
    def executeManyCommit(self):
        try:
            self.conn.commit()
            self.conn.close()
            self.Dados['Result'] = True

        except psycopg2.Error as error:
            self.Dados['Error']  = error.pgerror
            self.Dados['Result'] = False
        
        return self.Dados
    
    def executeMany(self, stmt, data):
        try:
            if data == None:
                self.curs.execute(stmt)
            else:
                self.curs.execute (stmt, data)
            hasData = self.curs.description != None
            if hasData and (self.curs.rowcount > 0):
                self.Dados['Data'] = self.curs.fetchall()
            else:
                self.Dados['Data'] = None
            self.Dados['Result'] = True

        except psycopg2.Error as error:
            self.Dados['Error']  = error.pgerror
            self.Dados['Result'] = False
    
        return self.Dados
