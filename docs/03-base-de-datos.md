# 3. Base de datos: Amazon DynamoDB

LICENTRA utiliza cuatro tablas de DynamoDB, identificadas en `backend/src/services/dynamodb.py`.

| Entidad API | Tabla DynamoDB | Clave primaria |
|---|---|---|
| `companies` | `Licentra-Companies` | `companyId` |
| `employees` | `Licentra-Employees` | `employeeId` |
| `licenses` | `Licentra-Licenses` | `licenseId` |
| `providers` | `Licentra-Providers` | `providerId` |

## Datos utilizados por la interfaz
**Empleados:** `employeeId`, `nombre`, `email`, `departamento`.

**Proveedores/software:** `providerId`, `nombre`, `descripcion`, `plan`, `costoMensual`, `periodicidad`, `proximoPago`, `licenciasTotales`, `licenciasAsignadas`, `estado`.

**Licencias:** `licenseId`, `employeeId`, `providerId`, `fechaAsignacion`, `estado`.

**Empresas:** el código CRUD identifica registros por `companyId`; no se impone un esquema adicional de atributos desde el backend.

DynamoDB es una base de datos NoSQL. Los vínculos entre empleado, proveedor y licencia se mantienen mediante identificadores, no mediante claves foráneas relacionales.

## Operaciones de datos
- `scan`: listar registros, con paginación mediante `LastEvaluatedKey`.
- `get_item`: obtener un registro por identificador.
- `put_item`: crear con condición para evitar identificadores repetidos.
- `update_item`: modificar campos sin cambiar la clave primaria.
- `delete_item`: eliminar con condición de existencia.
- `transact_write_items`: actualizar de forma conjunta el contador de cupos y el registro de asignación.

## Reglas de integridad implementadas
- No se permite reducir `licenciasTotales` por debajo de `licenciasAsignadas`.
- No se permite eliminar un empleado o proveedor con licencias asociadas sin liberarlas antes.
- La asignación comprueba que existan empleado y proveedor, que no esté duplicada y que haya cupos disponibles.
- La liberación elimina la asignación y decrementa el contador mediante una transacción.

## Consideraciones operativas
La cuenta AWS que ejecuta el backend necesita permisos de lectura/escritura sobre las tablas y `dynamodb:TransactWriteItems` para asignaciones. No se incluyen claves de acceso en esta documentación.
