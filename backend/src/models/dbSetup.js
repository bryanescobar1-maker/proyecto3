import os
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

load_dotenv()

# Configuración de DynamoDB
dynamodb = boto3.resource(
    'dynamodb',
    region_name=os.getenv('AWS_REGION', 'us-east-1'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

TABLE_NAME = os.getenv('DYNAMODB_TABLE_NAME', 'SaasManagementTable')

def seed_database():
    try:
        tabla = dynamodb.Table(TABLE_NAME)
        
        # 1. Empresa / Organización
        tabla.put_item(
            Item={
                "PK": "ORG#ORG001",
                "SK": "METADATA",
                "nombre": "Empresa Demo",
                "plan": "Enterprise"
            }
        )

        # 2. Proveedor SaaS (CRUD: Proveedores)
        tabla.put_item(
            Item={
                "PK": "ORG#ORG001",
                "SK": "PROV#AWS",
                "nombre": "Amazon Web Services",
                "categoria": "Cloud",
                "costo_plan": "15.00"
            }
        )

        # 3. Asignación de Licencia (CRUD: Licencias)
        tabla.put_item(
            Item={
                "PK": "PROV#AWS",
                "SK": "LIC#001",
                "nombrePlan": "t3.micro Instance",
                "estado": "ACTIVA",
                "asignadoA": "EMP#101"
            }
        )

        # 4. Empleado
        tabla.put_item(
            Item={
                "PK": "ORG#ORG001",
                "SK": "EMP#101",
                "nombre": "Carlos Rivas",
                "departamento": "TI"
            }
        )

        # 5. Pagos y Facturas (CRUD: Pagos / Renovaciones)
        tabla.put_item(
            Item={
                "PK": "PROV#AWS",
                "SK": "BILL#2026-11",
                "monto": "15.00",
                "estadoFactura": "PAGADA",
                "fechaVencimiento": "2026-11-25"
            }
        )

        print("✅ Datos de prueba creados exitosamente en DynamoDB.")
        
    except ClientError as e:
        print("❌ Error al insertar datos:", e.response['Error']['Message'])

if __name__ == '__main__':
    seed_database()
