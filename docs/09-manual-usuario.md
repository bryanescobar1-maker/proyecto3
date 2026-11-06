# 9. Manual de usuario de LICENTRA

## Acceso a la aplicación local
1. Inicia el backend Flask y el servidor HTTP del frontend siguiendo `06-instalacion.md`.
2. Abre `http://localhost:5500/panel.html`.
3. Utiliza la navegación disponible para acceder a proveedores o gestión de empleados y licencias.

La pantalla inicial de acceso de esta versión es demostrativa y no valida usuarios contra un sistema de autenticación.

## Consultar el panel
El panel presenta información resumida: proveedores registrados, empleados, licencias asignadas, cupos disponibles, costo mensual estimado y próximos pagos de proveedores. Los datos provienen de la API conectada a DynamoDB.

## Registrar software
1. Abre la pantalla de proveedores.
2. Selecciona la opción de registrar software.
3. Completa los campos solicitados en el formulario.
4. Guarda el registro y verifica que aparezca en el listado.

## Editar o eliminar proveedores
En el listado, utiliza **Editar** para modificar plan, costo o cantidad de licencias. Utiliza **Eliminar** para solicitar el borrado. Si el proveedor tiene licencias asignadas, la API impide eliminarlo hasta que se liberen.

## Administrar empleados
En la pantalla de gestión, selecciona **Registrar empleado** y completa nombre, correo y departamento. Puedes editar, buscar o eliminar registros. La opción de exportación genera un archivo CSV con los empleados cargados.

## Asignar una licencia
1. Asegúrate de tener empleados y software registrados.
2. Selecciona **Asignar licencia**.
3. Elige el empleado y un software con cupos disponibles.
4. Confirma la operación y revisa la tabla de asignaciones.

## Liberar una licencia
Ubica la asignación correspondiente y selecciona **Liberar**. Tras confirmar, el sistema elimina la asignación y actualiza los cupos del proveedor mediante una transacción de DynamoDB.

## Mensajes frecuentes
- **No hay licencias disponibles:** el proveedor no tiene cupos libres.
- **El empleado ya tiene asignado este software:** existe una asignación equivalente.
- **No se pudieron cargar los datos:** revisa la conexión con Flask y el acceso a DynamoDB.
- **Primero libera las licencias:** hay asignaciones que impiden eliminar el empleado o proveedor.
