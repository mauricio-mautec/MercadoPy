import psycopg2
import psycopg2.extras
from   utility import konstantes

# CLASSE PARA REPRESENTAR A TECNOLOGIA DE ARMAZENAMENTO UTILIZADO
# CAMADA MAIS ABAIXO DO DTO QUE TEM HAVER COM O DADOS E SEU ARMAZENAMENTO
class AccessDB():
    # DADOS REPRESENTADOS
    def __init__(self):
        self.database = konstantes('POSTGRES', 'database')
        psycopg2.extras.register_uuid()
        self.Dados = {}
    def queryOne(self, stmt, data):
        Dados = {}
        try:
            conn = psycopg2.connect (self.database)
            curs = conn.cursor()
            if data == None:
                curs.execute(stmt)
            else:
                curs.execute (stmt, data)
            Data = curs.fetchone()
            self.Dados['Data'] = Data
            conn.commit()
            Result = True

        except psycopg2.Error as error:
            conn.rollback()
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
            Data = curs.fetchall()
            self.Dados['Data'] = Data
            conn.commit()
            Result = True;
        
        except psycopg2.Error as error:
            conn.rollback()
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

            hasData = (curs.statusmessage == "INSERT 0 1"
                    or curs.statusmessage == "SELECT 1"
                    or curs.statusmessage == "UPDATE 1")

            if hasData:
                Data = curs.fetchall()
                self.Dados['Data'] = Data

            conn.commit()
            Result = True;
        
        except psycopg2.Error as error:
            conn.rollback()
            self.Dados['Error'] = error.pgerror
            Result = False
        
        conn.close()
        self.Dados['Result'] = Result
        return self.Dados
