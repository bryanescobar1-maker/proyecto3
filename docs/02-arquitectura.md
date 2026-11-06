# 2. Arquitectura del sistema

## Vista general
```text
Navegador web (HTML/CSS/JavaScript)
       | solicitudes HTTP + JSON
       v
API Flask (backend/src/app.py)
       | llamadas de servicio boto3
       v
Amazon DynamoDB
  - Licentra-Companies
  - Licentra-Employees
  - Licentra-Licenses
  - Licentra-Providers
```

## Capa de presentación
Los archivos de `frontend/` contienen las pantallas HTML, estilos CSS y scripts JavaScript. `frontend/js/api.js` centraliza las solicitudes `fetch` y el tratamiento de errores HTTP.

## Capa de aplicación
`backend/src/app.py` declara las rutas HTTP, valida el formato básico de las solicitudes, convierte números decimales y devuelve JSON con códigos de estado.

## Capa de acceso a datos
`backend/src/services/dynamodb.py` concentra la selección de tablas, operaciones CRUD y transacciones de asignación y liberación. Utiliza `boto3` y toma la región de `AWS_REGION` (predeterminada: `us-east-1`).

## Flujo de asignación
1. El usuario selecciona empleado y software.
2. El frontend envía `POST /api/assignments`.
3. El backend comprueba la existencia de los registros y una asignación duplicada.
4. Una transacción de DynamoDB incrementa el contador del proveedor y crea la licencia; se comprueba la disponibilidad de cupos.
5. La API devuelve la asignación creada.

## Integración con Lambda
`app.py` expone `lambda_handler = make_lambda_handler(app)` mediante `apig-wsgi`. Esto describe la compatibilidad del código con un entorno Lambda; no constituye evidencia de que exista un despliegue publicado.

## Configuración local
La API escucha en `127.0.0.1:5000` y el frontend puede servirse en `localhost:5500`. CORS permite los orígenes definidos en `FRONTEND_ORIGIN`.
