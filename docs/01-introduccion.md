# 1. Introducción a LICENTRA

## Descripción
LICENTRA es una aplicación web administrativa para gestionar software y suscripciones SaaS, proveedores, empleados y asignaciones de licencias. Su interfaz web consume una API desarrollada con Flask, la cual almacena los registros en Amazon DynamoDB.

## Problema que aborda
La administración manual de suscripciones y licencias dificulta consultar los costos, identificar cupos disponibles y conocer qué empleado tiene asignado un servicio. LICENTRA reúne estas operaciones en una interfaz administrativa.

## Objetivo general
Centralizar la gestión de proveedores SaaS, empleados y licencias mediante una aplicación web conectada a una base de datos en la nube.

## Objetivos específicos
- Registrar y administrar información de software y proveedores.
- Mantener registros de empleados.
- Asignar y liberar licencias controlando los cupos contratados.
- Mostrar indicadores administrativos obtenidos de DynamoDB.
- Facilitar la consulta de próximos pagos registrados en cada proveedor.

## Alcance documentado
La versión revisada ofrece CRUD de proveedores y empleados, endpoints CRUD genéricos para cuatro entidades, asignación y liberación de licencias, búsqueda, exportación CSV de empleados y un panel con indicadores. La pantalla de acceso de esta versión es demostrativa y no constituye autenticación real.

## Tecnologías
Python, Flask, JavaScript, HTML, CSS, Amazon DynamoDB y boto3. La integración de Flask con AWS Lambda se representa en el código mediante `apig-wsgi`.
