# LICENTRA — versión integrada (local)

## Ejecutar en PowerShell

2. Desde `frontend`: `python -m http.server 5500`.
3. Abrir `http://localhost:5500/panel.html`.

## Menú


Para asignar licencias, editar primero un proveedor y establecer `licenciasTotales` > 0. No es un error que se muestren 0 disponibles cuando no hay cupos contratados.

## AWS y limitaciones



**No hay autenticación real**; no publiques esta API hasta agregar login seguro, autorización, validación estricta y controles de acceso. Los datos en DynamoDB existentes no se borran. No incluyas claves en el proyecto.
