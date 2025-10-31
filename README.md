## ⚙️ Flujo de ejecución de la API
1. comando **docker-compose** para correr el contenedor de la Base de datos
2. docker build -t prueba_candela . # Este comando se usa para construir la imagen docker que luego se ejecutara para asi realizar el contenedor
3. docker build -t prueba_candela # Se usa para crer el contenedor de forma generica sin detalles (para esto se usa docker-compo.yml)


## ⚙️ Flujo de funcionamiento
1. **Solicitud GET**
   - Se realiza una petición a la BD local `/api/users/<id>/`.

2. **Consulta interna**
   - El sistema busca el usuario en la base de datos (`candela_soft`).

3. **Consulta externa**
   - La API realiza una petición `GET` al endpoint externo para obtener información adicional como firstname y lastname. 

4. **Combinación de datos**
   - Los datos del usuario local y los del servicio externo donde se consulta para obtener dirección y teléfono, estos se unifican en una sola respuesta JSON.

5. **Validación de estado**
   - Si el usuario tiene estado `"inactive"`, el sistema **envía (o simula)** una notificación por correo electrónico utilizando `send_mail()` (configurado con Amazon SES para el envio de los mail).

6. **Respuesta final**
   - Se devuelve un JSON con toda la información consolidada:

```json
{
    "id": 9,
    "firstname": "Yira",
    "lastname": "Quintana",
    "external_data": {
        "address": {
            "street": "Dayna Park",
            "suite": "Suite 449",
            "city": "Bartholomebury",
            "zipcode": "76495-3109",
            "geo": {
                "lat": "24.6463",
                "lng": "-168.8889"
            }
        },
        "phone": "(775)976-6794 x41206"
    },
    "created_at": "2025-10-30",
    "status": "inactive"
}

7. Se hace manejo de excepciones personalizadas para generar mensajes muy dicientes