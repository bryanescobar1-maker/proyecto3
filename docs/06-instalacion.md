# 6. Instalación y ejecución local

## Requisitos
- Windows con PowerShell.
- Python 3 y `pip`.
- Acceso a AWS configurado en un perfil autorizado.
- Tablas DynamoDB de LICENTRA accesibles en la región configurada.

## 1. Preparar el backend
Desde la carpeta raíz del proyecto:
```powershell
cd backend\src
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```
El archivo `.env.example` contiene variables no secretas de ejemplo:
```dotenv
AWS_REGION=us-east-1
FRONTEND_ORIGIN=http://localhost:5500,http://127.0.0.1:5500
FLASK_DEBUG=0
```
No introduzcas claves de acceso AWS en archivos que se subirán a GitHub.

## 2. Configurar el perfil AWS
En la terminal que ejecutará Flask, selecciona un perfil ya configurado y autorizado:
```powershell
$env:AWS_PROFILE="licentra-dev"
```
El nombre del perfil es un ejemplo del entorno de desarrollo utilizado; debe existir en la computadora.

## 3. Iniciar Flask
```powershell
python app.py
```
Verifica `http://127.0.0.1:5000/health`. Debe responder con JSON indicando el servicio activo.

## 4. Iniciar el frontend
Abre otra terminal desde la raíz de LICENTRA:
```powershell
cd frontend
python -m http.server 5500
```
Visita `http://localhost:5500/panel.html` o `http://localhost:5500/proveedores.html`.

## 5. Comprobación funcional
Consulta el panel, verifica el listado de proveedores y prueba operaciones con registros de prueba autorizados. La API requiere acceso real a DynamoDB para cargar los datos.

## Solución de problemas frecuentes
- **Error de conexión:** verifica que Flask esté ejecutándose en el puerto 5000.
- **Error AWS:** verifica el perfil, la región y los permisos IAM.
- **Error de CORS:** revisa `FRONTEND_ORIGIN` y el origen del servidor web.
- **Error en asignación:** comprueba cupos disponibles y permisos de transacciones DynamoDB.
