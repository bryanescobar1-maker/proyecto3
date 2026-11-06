# 8. Pruebas funcionales y criterios de verificación

Este documento describe **cómo verificar** las funcionalidades identificadas en el código. No afirma que todas las pruebas se hayan ejecutado satisfactoriamente en un entorno específico.

## Comprobaciones de API
| Caso | Acción | Resultado esperado según el código |
|---|---|---|
| Salud | `GET /health` | JSON con servicio `LICENTRA` y estado `activo` |
| Listado | `GET /api/providers` | Arreglo JSON de proveedores |
| Alta | `POST /api/employees` con ID y campos válidos | HTTP 201 y registro creado |
| Duplicado | Crear un registro con el mismo ID | HTTP 409 |
| Consulta inexistente | `GET /api/employees/ID-inexistente` | HTTP 404 |
| Edición | `PUT /api/providers/ID` | Registro actualizado si existe |
| Eliminación | `DELETE /api/employees/ID` | Confirmación si el registro existe y no tiene licencias asociadas |
| Asignación | `POST /api/assignments` | HTTP 201 y licencia asignada si hay cupos |
| Liberación | `DELETE /api/assignments/ID` | Confirmación de licencia liberada |

## Verificaciones de interfaz
1. El panel presenta cantidades obtenidas de proveedores, empleados y licencias.
2. La búsqueda de proveedores filtra por nombre.
3. La gestión de empleados permite buscar por nombre/correo y exportar CSV.
4. La asignación ofrece proveedores con cupos disponibles.
5. Los errores de API se muestran al usuario.

## Prueba de integridad de licencias
Crear un empleado y un proveedor de prueba con cupos, asignar una licencia y verificar que el contador aumenta. Liberarla y verificar que el contador disminuye. Utilizar registros de prueba y confirmar los resultados en DynamoDB.

## Evidencia de ejecución
Para una presentación académica, las evidencias pueden consistir en capturas del estado HTTP, registros en DynamoDB y pantallas del frontend, siempre que provengan de pruebas realmente ejecutadas. No se adjuntan resultados inventados.
