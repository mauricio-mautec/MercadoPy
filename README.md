# mercado
Sistema para Pedidos de Venda On-Line
=====================================

## MODELO DE DESENVOLVIMENTO PYTHON/AMQP/REACT
**UTILIZANDO  BACKEND PYTHON, MIDDLEWARE RABBITMQ, FRONTEND REACT**
---

## RAIZ DO PROJETO:

## ARQUIVOS:

--- 

## DIRETORIOS:
* api            APRESENTA TODOS OS RECURSOS DISPONIBILIZADOS PELA API
* log            LOG PARA O SISTEMA, ATUALMENTE UWSGI LOG NESSE DIR

---

## CONSIDERACOES INICIAIS
O JSON ENVIADO CONTEM INFORMACOES SOBRE O RECURSO QUE DEVERA SER DISPONIBILIZADO
O RECURSO CASO EXISTA, DISPONIBILIZA UM OBJETO INSTANCIADO COM O METODO E O JSON ENVIADO
A SAIDA DO METODO EXECUTE DISPONIBILIZADO PELO OBJETO RETORNA PARA O CLIENTE COMO RAW JSON application/json NO CANAL DE RESPOSTA ESPECIFICADO NO JSON: "Rsp"

--- 

## FUNCIONAMENTO GERAL:
1. CLIENTE REST PRODUZ UMA MENSAGEM RAW JSON PARA O CANAL DE CONSUMO DA API INFORMANDO O RECURSO QUE DESEJA EXECUTAR E TAMBÉM OS PARÂMETROS DE EXECUÇÃO
2. API PYTHON CONSOME A MENSAGEM, VALIDA O ACESSO, CRIA RECURSO PARA PROCESSAMENTO, EXECUTA E RETORNA RESPOSTA RAW JSON PARA O CLIENTE NO CANAL ESPECIFICADO PELO CLIENTE NA PRÓPRIA MENSAGEM


## MODELO JSON API
> SOLICITAÇÃO PUBLICADA EM apiFabrica PARA SOLICITAR O LOGIN

{
    "Api": {
        "Name": "autenticador.Token", # api/autenticador/Autenticador.py, contém uma classe Token e esta possuí um método Execute
        "Param": {
            "Login": "serjao@gmail.com",
            "Password": "ve0874biu",
            "Sistema" : 2,
            "Appid" : { "Name" : "hudflutter", "Version" : "text da versao", "Appsys": "win64, android trálálá, iphone"}
        }
    },
    "Rsp": "answerChannel_uuid" # NOME DO CANAL DE RESPOSTA SOLICITADO PELO CLIENTE - NORMALMENTE UM UUID
}

- RESPOSTA DA API api/autenticador/Autenticador.py, class Token PUBLICADA EM answerChannel:

{
    "Token": "{\"Sistema\": \"Fabrica Itaucu\", \"AuthID\": 19, \"UserID\": 1, \"__IP__\": \"19.9.19.229\", \"key\": \"774558802eef43bca1a2a8b15cddee08\"}.GaI4nNMuQ_BmLXcu3aDQN6IzX9A",
    "Validade": "'Fabrica Itaucu.XTWWVw.pxfGqDt_E_CrChBcmxOwz61gQMk'"
}

> DE POSSE DO TOKEN, PASSAMOS A ENVIA-LO NOS PROXIMOS REQUESTS PARA FINS DE AUTORIZAÇÃO:
{
    "Api": {
           "Name": "autenticador.TokenValidate",
           "Param": {"Token": "{\"Sistema\": \"Fabrica Itaucu\", \"AuthID\": 19, \"UserID\": 1, \"__IP__\": \"19.9.19.229\", \"key\": \"774558802eef43bca1a2a8b15cddee08\"}.GaI4nNMuQ_BmLXcu3aDQN6IzX9A", "Validade": "'Fabrica Itaucu.XTWWVw.pxfGqDt_E_CrChBcmxOwz61gQMk'"} },
    "Rsp": "answerChannel_uuid"
}

- RESPOSTA
{
    "Sistema": "Fabrica Itaucu",
    "AuthID": 19,
    "UserID": 1,
    "__IP__": "19.9.19.229",
    "key": "f41c7f6f82244acab7d6ce1774b8f7e0"
}
