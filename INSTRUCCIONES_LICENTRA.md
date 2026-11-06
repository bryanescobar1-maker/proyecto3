# LICENTRA — proyecto integrado (versión de desarrollo)

Se conservan los HTML y el CSS originales. Se añade backend Flask con cuatro entidades DynamoDB y JS para consultar/crear/editar/eliminar proveedores.

## Inicio local en Windows

1. En `backend/src`, crea un entorno virtual con `python -m venv .venv` si aún no tienes uno.
2. Actívalo con `.venv\Scripts\Activate.ps1` y ejecuta `python -m pip install -r requirements.txt`.
3. Copia `.env.example` a `.env`. No agregues credenciales al repositorio.
4. Configura acceso AWS local mediante AWS CLI `aws configure sso` o un perfil autorizado, con permisos limitados a las cuatro tablas en `us-east-1`.
5. Ejecuta `python app.py` y abre `http://127.0.0.1:5000/health`.
6. En otra terminal, dentro de `frontend`, ejecuta `python -m http.server 5500` y abre `http://localhost:5500/proveedores.html`.

## AWS Lambda

Handler: `app.lambda_handler` si `app.py` está en la raíz del ZIP desplegado. Empaqueta Flask, boto3, apig-wsgi y dependencias compatibles con el runtime Linux elegido. Crea rol IAM con permisos limitados a DynamoDB (GetItem, Scan, PutItem, UpdateItem, DeleteItem). Conecta API Gateway y configura CORS para tu dominio CloudFront. Cambia `API_URL` en `frontend/js/api.js` por la URL real de API Gateway.

## Advertencias

- La pantalla de login original es solo demostrativa: NO autentica. No uses contraseñas reales ni publiques los CRUD sin Cognito u otra autenticación y autorización por empresa.
- La vista de empleados y la vista de panel conservan datos de ejemplo. `panel.js` calcula métricas en consola, pero no reemplaza todavía las tarjetas visuales.
- El frontend no debe abrirse como `file://`; sírvelo por HTTP.
- Se han excluido `.git`, `venv` y secretos del ZIP entregado. Conserva tu repositorio Git original en tu computadora.
- Los archivos JS antiguos del backend (`config/dynamoClient.js` y `models/dbSetup.js`) son legado y no participan en el backend Python.
