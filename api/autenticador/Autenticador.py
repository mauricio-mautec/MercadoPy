import uuid
from itsdangerous.serializer import Serializer
from itsdangerous            import TimestampSigner
from itsdangerous.exc import BadSignature, BadData
import json
from api.autenticador.AutenticadorDTO import AutenticadorDTO
from utility import testToken, konstantes, sendLog

hugekey   = konstantes('TOKEN','hugekey')
timekey   = konstantes('TOKEN','timekey')
maxage    = int (konstantes('TOKEN','maxage'))


# RETORNA CASO LOGIN / PASSWORD CONFERIR
# JSON COM SISTEMAS QUE PODEM SER ATENDIDOS
class UserInfo:
    def __init__(self, Param):
        self.Param  = Param

    def Execute (self):
        Login     = self.Param['Login']
        Password  = self.Param['Password']
        dto       = AutenticadorDTO()

        if  dto.getUserInfo (Login, Password):
            data = dto.getData()
            return json.dumps(data)
            
        data = {}
        data["Api"]    = "autenticador.UserInfo"
        data["Result"] = f"Login [{Login}] Password [{Password}] NOT OK"
        self.Log(dados["Result"])

        return json.dumps(data)

    def Log(message):
        sendLog('Autenticador.UserInfo', message)
    
class Token:
    def __init__(self, Param):
        self.Param  = Param

    def Execute (self):    
        Login     = self.Param['Login']
        Password  = self.Param['Password']
        Appid     = self.Param['Appid']
        Sistema   = self.Param['Sistema']
        dto       = AutenticadorDTO()
        Token     = uuid.uuid4()

        if  dto.setUserAuth (Login, Password, Appid, Sistema, Token.hex):
            # TOKEN ASSINADO COM VALORES DE SESSAO
            data = dto.getData()
            Sessao = {}
            Sessao["Sistema"]  = f"Sistema id:{Sistema}"
            Sessao["AuthID"]   = data["AuthID"]
            Sessao["UserID"]   = data["UserID"] 
            Sessao["__IP__"]   = self.Param["__IP__"]
            Sessao["key"]      = Token.hex
            slrz               = Serializer(hugekey)
            Token              = slrz.dumps(Sessao)
            # TIMESTAMP PARA TEMPO DE VALIDADE
            st                 = TimestampSigner (timekey)
            validade           = st.sign(Sessao["Sistema"]).decode('UTF-8')
            dados              = {}
            dados["Token"]     = Token
            dados["Validade"]  = validade
            return json.dumps(dados) # PYTHON DATA TO ENCODED JSON STRING

        dados = {}
        dados["Api"]    = "autenticador.Token"
        dados["Result"] = f"Login [{Login}] Password [{Password}] NOT OK"
        self.Log(dados["Result"])

        return json.dumps(dados)
    
    def Log(message):
        sendLog('Autenticador.Token', message)

class TokenValidate:
    def __init__(self, Param):
        self.Param  = Param

    def Execute (self):
        data = {}
        data["Api"]    = "autenticador.TokenValidade"
        Result, msg, AuthID = testToken(self.Param)
        if not Result:
            data["Result"] = msg
            sendLog('Autenticador.TokenValidate', msg)
        else:
            data["Result"] = "OK"
            dto = AutenticadorDTO()
            dto.checkAuth(AuthID)    # UPDATE LAST CHECK TIME OF THE TOKEN
        
        return json.dumps(data)
