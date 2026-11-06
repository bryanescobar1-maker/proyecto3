# 7. Integración del proyecto con AWS

## Servicio de datos: DynamoDB
El backend consulta las tablas `Licentra-Companies`, `Licentra-Employees`, `Licentra-Licenses` y `Licentra-Providers` mediante `boto3`. La región predeterminada configurada en código es `us-east-1`.

## Credenciales y permisos
En desarrollo local se utiliza el mecanismo estándar de credenciales AWS, por ejemplo un perfil AWS CLI. La política IAM debe limitar el acceso a las tablas utilizadas. Las operaciones de asignación y liberación utilizan `TransactWriteItems`.

## Adaptación de Flask para Lambda
El archivo `backend/src/app.py` incluye:
```python
from apig_wsgi import make_lambda_handler
lambda_handler = make_lambda_handler(app)
```
Esto permite adaptar las solicitudes de una integración compatible con AWS Lambda a la aplicación WSGI Flask.

## Parámetros relevantes
| Parámetro | Uso |
|---|---|
| `AWS_REGION` | Región de las tablas DynamoDB |
| `FRONTEND_ORIGIN` | Orígenes autorizados por CORS |
| `FLASK_DEBUG` | Control del modo de depuración local |
| `API_URL` | URL base de la API utilizada por `frontend/js/api.js` |

## Arquitectura compatible con servicios AWS
El código contempla un backend Flask adaptable a Lambda y una interfaz web estática que consume una API HTTP. El archivo `api.js` contiene la dirección local del backend; su valor debe corresponder al entorno en que se ejecute la aplicación.

## Alcance de esta descripción
Esta sección documenta **la integración AWS visible en el código fuente revisado** y la configuración local de DynamoDB. No certifica la existencia de recursos desplegados, dominios públicos o pruebas de producción.
