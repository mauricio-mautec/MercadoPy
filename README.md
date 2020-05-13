# mercado
Sistema para Pedidos de Venda On-Line
=====================================

## MODELO DE DESENVOLVIMENTO REST/AMQP
**UTILIZANDO REST, NGINX, FLASK, UWSGI COM API PYTHON.**

**ATUALMENTE SENDO MODIFICADO PARA TRABALHAR COM RABBITMQ**

**EM BREVE NOVO README COM AS NOVAS ORIENTACOES**

---

## RAIZ DO PROJETO:
_/srv/mautec/mercado_

## ARQUIVOS:
* config.ini     ARQUIVO DE CONFIGURACAO CENTRAL
* API.py         APLICACAO PARA EXECUCAO POR UWSGI
* nginx.conf     CONFIGURACAO DO NGINX, LINK SIMBOLICO PARA /etc/nginx/conf.d/mercado.conf
* uwsgi.conf     ESPECIFICA PARA UWSGI O NOME DA APLICACAO E OUTRAS CONFIGURACOES DE OPERACAO
* uwsgi.service  ESPECIFICA EXECUCAO DE UWSGI COMO SERVICO DE SISTEMA, COPIADO PARA /etc/systemd/system/emperor.uwsgi.service
* uwsgi.sock     ARQUIVO UTILIZADO COMO BUFFER/PIPE ENTRE UWSGI e NGINX
* on.sh/off.sh   ACIONA / DESLIGA OPERACAO DO NGINX / UWSGI. POSSIBILITA DEPURACAO python API.py
* pipReq.txt     ARQUIVO GERADO COM DEPENDENCIAS DO SISTEMA.

--- 

## DIRETORIOS:
* api            APRESENTA TODOS OS RECURSOS DISPONIBILIZADOS PELA API
* log            LOG PARA O SISTEMA, ATUALMENTE UWSGI LOG NESSE DIR
* data           DIRETORIO PARA A BASE DE DADOS
* trash          TEMPORARIO PARA ARQUIVOS NAO MAIS UTILIZADOS, NAO VERSIONADO
* static         DIRETORIO PARA CSS/JAVASCRIPT
* template       ARQUIVOS COM TEMPLATES HTML

* bin,include, lib,lib64      ARQUIVOS CRIADOS PARA O AMBIENTE VIRTUAL PYTHON

---

## CONSIDERACOES INICIAIS
TODAS AS CHAMADAS REST PARA A API ENTRAM SEMPRE NO MESMA ROTA: /api UTILIZANDO DIVERSOS METODOS (POST, PUT, GET...)
O JSON ENVIADO CONTEM INFORMACOES SOBRE O RECURSO QUE DEVERA SER DISPONIBILIZADO
O RECURSO CASO EXISTA, DISPONIBILIZA UM OBJETO INSTANCIADO COM O METODO E JSON ENVIADO
A SAIDA DO METODO EXECUTE DISPONIBILIZADO PELO OBJETO RETORNA PARA O CLIENTE COMO RAW JSON application/json no canal de resposta especificado no JSON - "Rsp"

--- 

## FUNCIONAMENTO GERAL:
1. CLIENTE REST ENVIA UMA CHAMADA REST application/json CONTENDO UM RAW JSON INFORMANDO O RECURSO QUE DESEJA EXECUTAR
2. API.py RECEBE A CHAMADA, CRIA RECURSO, EXECUTA E RETORNA RESPOSTA JSON PARA O CLIENTE NO CANAL ESPECIFICADO PELO CLIENTE


## MODELO JSON API
> ENVIANDO O LOGIN
{
    "Api": {
        "Name": "autenticador.Token",
        "Param": {
            "Login": "serjao@gmail.com",
            "Password": "ve0874biu",
            "Sistema" : 2,
            "Appid" : { "Name" : "hudflutter", "Version" : "text da versao", "Appsys": "win64, android trálálá, iphone"}
        }
    },
    "Rsp": "answerChannel"
}

- RESPOSTA:
{
    "Token": "{\"Sistema\": \"Fabrica Itaucu\", \"AuthID\": 19, \"UserID\": 1, \"__IP__\": \"19.9.19.229\", \"key\": \"774558802eef43bca1a2a8b15cddee08\"}.GaI4nNMuQ_BmLXcu3aDQN6IzX9A",
    "Validade": "'Fabrica Itaucu.XTWWVw.pxfGqDt_E_CrChBcmxOwz61gQMk'"
}

> DE POSSE DO TOKEN, PASSAMOS A ENVIA-LO NOS PROXIMOS REQUESTS PARA FINS DE AUTENTICACAO:
{
    "Api": {
           "Name": "autenticador.TokenValidate",
           "Param": {"Token": "{\"Sistema\": \"Fabrica Itaucu\", \"AuthID\": 19, \"UserID\": 1, \"__IP__\": \"19.9.19.229\", \"key\": \"774558802eef43bca1a2a8b15cddee08\"}.GaI4nNMuQ_BmLXcu3aDQN6IzX9A", "Validade": "'Fabrica Itaucu.XTWWVw.pxfGqDt_E_CrChBcmxOwz61gQMk'"} },
    "Rsp": "answerChannel"
}

- RESPOSTA
{
    "Sistema": "Fabrica Itaucu",
    "AuthID": 18,
    "UserID": 1,
    "__IP__": "19.9.19.229",
    "key": "f41c7f6f82244acab7d6ce1774b8f7e0"
}
