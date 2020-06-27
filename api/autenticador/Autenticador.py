import uuid
from itsdangerous.serializer import Serializer
from itsdangerous            import TimestampSigner
from itsdangerous.exc        import BadSignature, BadData
import json
from api.autenticador.AutenticadorDTO import AutenticadorDTO
from utility import konstantes, sendLog

Hugekey  = konstantes('TOKEN', 'hugekey')
Timekey  = konstantes('TOKEN', 'timekey')
Maxage   = int (konstantes('TOKEN', 'maxage'))
MaxageDB = int (konstantes('TOKEN', 'maxagedb'))

# RETORNA CASO LOGIN / PASSWORD CONFERIR
# JSON COM SISTEMAS QUE PODEM SER ATENDIDOS
class UserInfo:
    def __init__(self, Param):
        self.Param  = Param
        self.api    = "autenticador.UserInfo"
    def Execute (self):
        Login     = self.Param['Login']
        Password  = self.Param['Password']
        dto       = AutenticadorDTO()

        if  dto.getUserInfo (Login, Password):
            data = dto.getData()
            data["Result"] = "OK"
            return json.dumps(data)
            
        data = {}
        data["Api"]    = self.api
        data["Result"] = "Login/Password NOT OK"
        self.Log(dados["Result"])
        return json.dumps(data)

    def Log(self, message):
        sendLog(self.api, message)
    
class Token:
    def __init__(self, Param):
        self.Param  = Param
        self.api    = "autenticador.Token"
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
            Sessao["Sistema"]  = f"{Sistema}"
            Sessao["AuthID"]   = data["AuthID"]
            Sessao["UserID"]   = data["UserID"] 
            Sessao["__IP__"]   = self.Param["__IP__"]
            Sessao["key"]      = Token.hex
            slrz               = Serializer(Hugekey)
            Token              = slrz.dumps(Sessao)
            # TIMESTAMP PARA TEMPO DE VALIDADE
            st                 = TimestampSigner (Timekey)
            validade           = st.sign(Sessao["Sistema"]).decode('UTF-8')
            dados              = {}
            dados["Token"]     = Token
            dados["Validade"]  = validade
            dados["Result"]    = "OK"
            return json.dumps(dados) # PYTHON DATA TO ENCODED JSON STRING

        dados = {}
        dados['Error']  = dto.Error
        dados["Api"]    = self.api
        dados["Result"] = "Login/Password NOT OK"
        self.Log(dados["Result"])
        return json.dumps(dados)
    
    def Log(self, message):
        sendLog(self.api, message)

class TokenValidate:
    def __init__(self, Param):
        self.Param  = Param
        self.dto    = AutenticadorDTO()
        self.api    = "autenticador.TokenValidate"  

    def Log(self,message):
        sendLog(self.api, message)

    def Execute (self):
        Result, msg, AuthID, Loja = self.testToken(self.Param)
        data           = {}        
        data["AuthID"] = AuthID
        data["Loja"]   = Loja
        data["Api"]    = self.api
 
        if Result:
            data["Result"] = "OK"
            self.dto = AutenticadorDTO()
            self.dto.updateAuth(AuthID, self.api)    # UPDATE LAST CHECK TIME OF THE TOKEN
            return json.dumps(data)

        if msg != 'EXPIRED':
            data["Result"] = msg
            self.Log(msg)
            return json.dumps(data)
      
        # TOKEN EXPIRADO - VERIFICA POSSIBLIDADE DE REVALIDACAO
        Result, validade = self.AtualizarToken()
        if Result:
            data['Token']    = self.Param['Token']
            data['Validade'] = validade
            msg = 'OK'
        else:
            self.Log(self.dto.Error)
            data['Error'] = self.dto.Error
            msg = 'REQUEST NEW AUTHORIZATION'

        data['Result'] = msg
        return json.dumps(data)

    def testToken(self, Param):       
        Sessao   = Param['Token']
        slrz     = Serializer(Hugekey)
        try:
            Token  = slrz.loads(Sessao)
        except BadSignature as e:
            return (False, "BAD TOKEN", 0, 0)

        st        = TimestampSigner (Timekey)
        val       = Param['Validade']
        Sistema   = val

        if not st.validate(Sistema, max_age = Maxage):
            return (False, "EXPIRED", Token['AuthID'], Token['Sistema'])

        if not Token['__IP__'] == Param['__IP__']:
            return (False, "BAD IP", Token['AuthID'], Token['Sistema'])

        return (True, "OK", Token['AuthID'], Token['Sistema'])    

    def AtualizarToken(self):
        # RECUPERAR SESSAO
        Token    = self.Param['Token']
        slrz     = Serializer(Hugekey)
        validade = ''
        try:
            Sessao = slrz.loads(Token)
        except:
            return (False, validade)
        
        # VERIFICAR TOKEN NA BASE
        AuthID = Sessao['AuthID']
        UserID = Sessao['UserID']
        maxage = int(MaxageDB)

        if not self.dto.checkValidAccess(AuthID, UserID, maxage):
            return (False, validade)

        # ATUALIZAR TOKEN NA BASE
        if not self.dto.updateAuth(AuthID, self.api):
            return (False, validade)

        # REVALIDAR TOKEN
        st        = TimestampSigner (Timekey)
        validade  = st.sign(Sessao["Sistema"]).decode('UTF-8')
        return (True, validade)
