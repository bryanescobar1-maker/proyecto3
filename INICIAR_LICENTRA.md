# LICENTRA — Versión funcional local (sin datos de demostración)

## 1. Backend
Desde la carpeta `Licentra` en PowerShell:

```powershell
cd backend\src
Copy-Item .env.example .env
$env:AWS_PROFILE="licentra-dev"
python -m pip install -r requirements.txt
python app.py
```

## 2. Frontend (otra terminal, desde la carpeta `Licentra`)

```powershell
cd frontend
python -m http.server 5500
```

Abre `http://localhost:5500/panel.html`, `proveedores.html` o `dashboard.html`.

## Funciones implementadas
- Proveedores: crear, listar, editar (plan, costo, cupos), eliminar y buscar.
- Empleados: crear, listar, editar, eliminar, buscar, exportar CSV.
- Licencias: asignar y liberar usando operaciones transaccionales de DynamoDB. Control de cupos y contador por proveedor.
- Panel: datos consultados desde DynamoDB; sin ejemplos fijos.
- Página de acceso: solo acceso local de demostración, **sin login real**.

## Importante
- **No publiques la API en internet todavía**: no existe autenticación/autorización.
- Las operaciones de asignación requieren permiso IAM `dynamodb:TransactWriteItems` sobre las tablas Providers y Licenses, además de los permisos CRUD existentes. Si ves un error 500, revisa la terminal Flask y la política IAM.
- Los registros antiguos de DynamoDB no se borran al reemplazar el frontend. Elimina manualmente cualquier dato de prueba que tú hayas creado.
- El contador `licenciasAsignadas` de los proveedores antiguos debe corresponder con los registros reales de `Licentra-Licenses`.
- La inversión mensual estimada divide por 12 los pagos anuales.
- Rota cualquier clave AWS compartida anteriormente. No incluyas `.env` ni claves en repositorios o ZIP.
- El despliegue en Lambda, API Gateway, S3/CloudFront y el login seguro quedan pendientes de configuración en tu cuenta AWS.
