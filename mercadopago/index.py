import mercadopago # criar o pix utilizando o sdk disponibilizado pelo mercado pago - é necessário ter uma conta +18 no mercado pago
import qrcode # gerar o qr code do pix
import json # -> puxar dados do config.json (accesstoken)

with open("config.json") as file:
    config = json.load(file)

accesstoken = config['accesstoken']

if not accesstoken:
    print("Sua Access Token não está configurada. Por favor, configure-a em config.json. Lembre-se que é necessário ter uma conta mercado pago +18!")
    exit()

else:
    sdk = mercadopago.SDK(str(accesstoken))
    request_options = mercadopago.config.RequestOptions()


def criar_pix(amount: float):
    payment_data = {
        "transaction_amount": amount,
        "payment_method_id": "pix",
        "payer": {
            "email": "seu_email@example.com" # coloque seu email aqui
        }
    }

    payment_response = sdk.payment().create(payment_data, request_options)
    payment = payment_response["response"]

    if "point_of_interaction" in payment:
        qr_code = payment["point_of_interaction"]["transaction_data"]["qr_code"]
    else:
         print("Erro ao criar o QR Code!")

    print(f"Pix Copia e Cola: {qr_code}")
    criar_qr_code(qr_code)


def criar_qr_code(response):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(response)
        qr.make(fit=True)

        qr_code_file = f"qrcode.png"
        qr.make_image(fill_color="black", back_color="white").save(qr_code_file)
        print(f"QR Code salvo com sucesso em {qr_code_file}")

amount = 120
criar_pix(amount)
