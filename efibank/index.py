# encoding: utf-8
from efipay import EfiPay
import json
import requests
import time

# Carregar configurações
try:
    with open("config.json") as db:
        database = json.load(db)
except FileNotFoundError:
    print("Arquivo config.json não encontrado. Verifique o caminho e tente novamente.")
    exit(1)

# Configurar EfiPay
try:
    efi = EfiPay({
        'client_id': database["efibank"]["clientID"],
        'client_secret': database["efibank"]["clientSECRET"],
        'sandbox': False,
        'certificate': './database/certificado-combinado.pem'
    })
except Exception as e:
    print(f"Erro ao configurar o SDK da EfiPay: {e}")
    exit(1)

# Função para criar cobrança PIX
def criar_cobranca_pix(valor, descricao):
    try:
        dados_cobranca = {
            'calendario': {'expiracao': 3600},  # Expiração em 1 hora
            'valor': {'original': f'{valor:.2f}'},
            'chave': database["efibank"]["chavePIX"],
            'solicitacaoPagador': descricao
        }
        resposta = efi.pix_create_immediate_charge(body=dados_cobranca)
        print(f"Cobrança criada: {resposta}")

        txid = resposta.get('txid')
        copia_cola = resposta.get('pixCopiaECola')
        location = resposta.get('loc', {}).get('location')

        if not txid or not copia_cola or not location:
            print("Erro ao criar a cobrança Pix. Resposta incompleta.")
            return None, None, None

        return txid, copia_cola, location
    except Exception as e:
        print(f"Erro ao criar a cobrança Pix: {e}")
        return None, None, None

# Função para gerar QR Code
def gerar_qr_code(qr_code_data):
    url = "https://api.qrcode-monkey.com/qr/custom"
    payload = {
        "data": qr_code_data,
        "config": {
            "body": "round",
            "eye": "frame2",
            "eyeBall": "ball14",
            "bodyColor": "#5865F2",
            "bgColor": "#FFFFFF",
            "eye1Color": "#5865F2",
            "eye2Color": "#5865F2",
            "eye3Color": "#5865F2",
            "eyeBall1Color": "#5865F2",
            "eyeBall2Color": "#5865F2",
            "eyeBall3Color": "#5865F2",
            "gradientOnEyes": "true",
            "logo": None,
            "logoMode": "default"
        },
        "size": 2000,
        "download": "imageUrl",
        "file": "png"
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        qr_code_response = response.json().get('imageUrl')

        if not qr_code_response:
            raise ValueError("Erro: URL do QR Code não foi retornada.")
        return qr_code_response
    except Exception as e:
        print(f"Erro ao gerar o QR Code: {e}")
        return None

# Função para verificar status do pagamento
def verificar_status_pagamento(txid, tentativas=120, intervalo=5):
    for tentativa in range(1, tentativas + 1):
        try:
            resposta = efi.pix_detail_charge(params={"txid": txid})
            status = resposta.get('status')

            print(f"Tentativa {tentativa}: Status do pagamento para TXID {txid}: {status}")

            if status in ["CONCLUIDA", "CANCELADA"]:
                return status

        except Exception as e:
            print(f"Erro ao verificar o status do pagamento na tentativa {tentativa}: {e}")

        time.sleep(intervalo)

    print("Limite de tentativas atingido. Não foi possível confirmar o pagamento.")
    return None

# Exemplo de uso
if __name__ == "__main__":
    valor = 1.00
    descricao = "Pagamento de teste"

    txid, copia_cola, location = criar_cobranca_pix(valor, descricao)
    if not txid or not copia_cola:
        print("Erro ao criar cobrança. Encerrando.")
        exit(1)

    qr_code_url = gerar_qr_code(copia_cola)
    if not qr_code_url:
        print("Erro ao gerar QR Code. Encerrando.")
        exit(1)

    print(f"QR Code gerado com sucesso: {qr_code_url}")
    print(f"Pix Copia e Cola: {copia_cola}")

    status = verificar_status_pagamento(txid)
    if status:
        print(f"Status final do pagamento: {status}")
    else:
        print("Pagamento não foi confirmado dentro do tempo limite.")
