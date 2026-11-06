# 4. Backend y API REST

## Tecnologías y archivos
El backend está implementado con Flask. `app.py` declara las rutas; `services/dynamodb.py` implementa las operaciones sobre DynamoDB. Las dependencias declaradas en `requirements.txt` incluyen Flask, boto3, apig-wsgi, python-dotenv y flask-cors.

## Endpoints
| Método | Ruta | Función |
|---|---|---|
| GET | `/` | Estado general del backend |
| GET | `/health` | Comprobación de salud |
| GET | `/api/<entity>` | Listar registros |
| POST | `/api/<entity>` | Crear registro |
| GET | `/api/<entity>/<id>` | Consultar registro |
| PUT | `/api/<entity>/<id>` | Actualizar registro |
| DELETE | `/api/<entity>/<id>` | Eliminar registro |
| POST | `/api/assignments` | Asignar licencia |
| DELETE | `/api/assignments/<license_id>` | Liberar licencia |

`<entity>` acepta `companies`, `employees`, `licenses` o `providers`.

## Ejemplos de solicitudes
Crear un empleado:
```http
POST /api/employees
Content-Type: application/json

{"employeeId":"emp-demo-01","nombre":"Ejemplo","email":"ejemplo@dominio.test","departamento":"TI"}
```
Asignar una licencia:
```http
POST /api/assignments
Content-Type: application/json

{"employeeId":"emp-demo-01","providerId":"prov-demo-01"}
```
Los identificadores del ejemplo son ilustrativos; el proveedor y empleado deben existir para asignar.

## Respuestas y errores
La API devuelve JSON. Se utilizan, entre otros, `201` para creación, `400` para datos inválidos, `404` para recursos inexistentes, `409` para duplicados y `500` para errores internos.

## Reglas relevantes
Las operaciones genéricas requieren una clave primaria no vacía al crear. En las actualizaciones no se permite modificar el identificador. Las operaciones específicas de asignación controlan disponibilidad y contadores con transacciones.

## Seguridad de configuración
Las credenciales AWS deben obtenerse mediante un perfil o mecanismo de identidad autorizado; no se colocan en el código ni en Git. La pantalla de acceso del frontend revisado es demostrativa, por lo que no debe interpretarse como un control de autenticación de la API.
