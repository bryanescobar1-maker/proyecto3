# 5. Frontend y navegación

## Estructura
El frontend utiliza HTML, CSS y JavaScript sin necesidad de un framework de interfaz. El archivo `frontend/js/api.js` centraliza las llamadas HTTP a Flask mediante `fetch`.

## Pantallas principales
| Archivo | Uso |
|---|---|
| `index.html` | Pantalla de acceso de demostración |
| `panel.html` | Resumen administrativo y métricas |
| `proveedores.html` | Listado, búsqueda, edición y eliminación de proveedores |
| `registrar-software.html` | Formulario de registro de software |
| `dashboard.html` | Gestión de empleados y asignaciones de licencias |

## Panel de control
`panel.js` consulta proveedores, empleados y licencias. Calcula costo mensual estimado, cantidad de proveedores, empleados, licencias asignadas y disponibles, además de próximos pagos dentro de 30 días. Para proveedores con periodicidad anual, el importe se divide entre 12 al estimar el costo mensual.

## Gestión de proveedores
`proveedores.js` obtiene registros de DynamoDB por medio de la API, permite filtrar por nombre, editar plan/costo/cupos y solicitar eliminación con confirmación.

## Empleados y licencias
`gestion.js` presenta registros de empleados y sus asignaciones, permite crear/editar/eliminar empleados, buscar por nombre o correo, exportar CSV y asignar/liberar licencias. La interfaz muestra los cupos disponibles por software.

## Comunicación con backend
`api.js` utiliza por defecto `http://127.0.0.1:5000`. Cada operación envía o recibe JSON y muestra mensajes cuando la API responde con error.

## Recomendación de ejecución
Abrir el frontend mediante un servidor HTTP local, no directamente con `file://`, para mantener el comportamiento esperado de la aplicación.
