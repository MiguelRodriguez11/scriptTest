import requests
import os
import subprocess
import json

# URL del servidor web que quieres verificar
URL = "https://migueldev-web.vercel.appasdasd"

# Configuración de Mailjet
MAILJET_API_KEY = os.getenv("MAILJET_KEY")
MAILJET_API_SECRET = os.getenv("MAILJET_SECRETKEY")

FROM_EMAIL = "11.mrodriguez.21@gmail.com"
TO_EMAIL = "miguelsaray05@gmail.com"
FROM_NAME = "Miguel Angel"
TO_NAME = "Miguel Angel Rodriguez Saray"
SUBJECT = "Status server"
TEXT_PART = "El servidor web no está disponible. Código de respuesta: {http_response}"
HTML_PART = "<h3>Dear passenger 1, welcome to <a href='https://www.mailjet.com/'>Mailjet</a>!</h3><br />May the delivery force be with you!"
CUSTOM_ID = "AppGettingStartedTest"

try:
    # Realizar una solicitud HTTP y obtener el código de estado
    response = requests.get(URL)
    http_response = response.status_code

    # Comprobar el código de respuesta
    if http_response == 200:
        print(f"El servidor web está funcionando correctamente. Código de respuesta: {http_response}")
    else:
        print(f"El servidor web no está disponible. Código de respuesta: {http_response}")
        
        mailjet_payload = {
            "Messages": [
                {
                    "From": {
                        "Email": FROM_EMAIL,
                        "Name": FROM_NAME
                    },
                    "To": [
                        {
                            "Email": TO_EMAIL,
                            "Name": TO_NAME
                        }
                    ],
                    "Subject": SUBJECT,
                    "TextPart": TEXT_PART,
                    "HTMLPart": HTML_PART,
                    "CustomID": CUSTOM_ID
                }
            ]
        }

        # Enviar una notificación por correo electrónico utilizando Mailjet y cURL
        curl_command = [
            "curl",
            "-s",
            "-X", "POST",
            "--user", f"{MAILJET_API_KEY}:{MAILJET_API_SECRET}",
            "https://api.mailjet.com/v3.1/send",
            "-H", "Content-Type: application/json",
            "-d", json.dumps(mailjet_payload)
        ]

        try:
            result = subprocess.run(curl_command, check=True, capture_output=True, text=True)
            print(f"Notificación enviada por correo electrónico. Respuesta de Mailjet: {result.stdout}")
        except subprocess.CalledProcessError as e:
            print(f"Error al enviar el correo electrónico con Mailjet. Detalles: {e.stderr}")
        exit(1)

except requests.exceptions.RequestException as e:
    # Manejar errores en la solicitud HTTP
    print(f"Error: No se pudo conectar al servidor web. Detalles: {e}")
    exit(1)
