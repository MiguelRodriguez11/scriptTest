#!/bin/bash

if [ -f .env ]; then
  export $(cat ../../.env | grep -v '#' | awk '/=/ {print $1}')
fi

echo $MAILJET_KEY
echo $MAILJET_SECRETKEY

URL="https://migueldev-web.vercel.appasdasdasdasd"

HTTP_RESPONSE=$(curl --write-out "%{http_code}" --silent --output /dev/null "$URL")

if [ "$HTTP_RESPONSE" -eq 200 ]; then
    echo "El servidor web esta funcionando correctamente. Codigo de respuesta: $HTTP_RESPONSE"
else
    echo "El servidor web no esta disponible. Codigo de respuesta: $HTTP_RESPONSE"

    # Enviar notificación por correo 
    curl -s \
    -X POST \
    --user "1b5df97716d10b35d1844697bfaf95dd:1b20d46f29a70c1949e07621de6fbf28" \
    https://api.mailjet.com/v3.1/send \
    -H 'Content-Type: application/json' \
    -d '{
      "Messages":[
        {
          "From": {
            "Email": "11.mrodriguez.21@gmail.com",
            "Name": "Miguel Angel"
          },
          "To": [
            {
              "Email": "miguelsaray05@gmail.com",
              "Name": "Miguel Angel"
            }
          ],
          "Subject": "Alerta: Servidor Web No Disponible",
          "TextPart": "El servidor web https://migueldev-web.vercel.app no está disponible. Código de respuesta: '"$HTTP_RESPONSE"'",
          "HTMLPart": "<h3>Alerta: Servidor Web No Disponible</h3><p>El servidor web <a href=\"https://migueldev-web.vercel.app\">https://migueldev-web.vercel.app</a> no está disponible. Código de respuesta: '"$HTTP_RESPONSE"'</p>",
          "CustomID": "ServerStatusAlert"
        }
      ]
    }'
    
    exit 1
fi
