import os
import boto3
from botocore.exceptions import ClientError

TABLES = {
    "companies": {"table": "Licentra-Companies", "key": "companyId"},
    "employees": {"table": "Licentra-Employees", "key": "employeeId"},
    "licenses": {"table": "Licentra-Licenses", "key": "licenseId"},
    "providers": {"table": "Licentra-Providers", "key": "providerId"},
}

class Duplicate(Exception): pass
class NotFound(Exception): pass

def table(entity):
    return boto3.resource("dynamodb", region_name=os.getenv("AWS_REGION", "us-east-1")).Table(TABLES[entity]["table"])

def get_all(entity):
    result = []
    options = {}
    while True:
        page = table(entity).scan(**options)
        result.extend(page.get("Items", []))
        if "LastEvaluatedKey" not in page:
            return result
        options["ExclusiveStartKey"] = page["LastEvaluatedKey"]

def get_by_id(entity, item_id):
    return table(entity).get_item(Key={TABLES[entity]["key"]: item_id}, ConsistentRead=True).get("Item")

def create_item(entity, data):
    key = TABLES[entity]["key"]
    try:
        table(entity).put_item(Item=data, ConditionExpression="attribute_not_exists(#pk)", ExpressionAttributeNames={"#pk": key})
    except ClientError as e:
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            raise Duplicate("El identificador ya existe") from e
        raise
    return data

def update_item(entity, item_id, data):
    key = TABLES[entity]["key"]
    if not data or key in data:
        raise ValueError("Envía campos para actualizar sin modificar el ID")
    names = {"#pk": key}
    values = {}
    clauses = []
    for i, (field, value) in enumerate(data.items()):
        names[f"#f{i}"] = field
        values[f":v{i}"] = value
        clauses.append(f"#f{i} = :v{i}")
    try:
        return table(entity).update_item(Key={key: item_id}, UpdateExpression="SET " + ", ".join(clauses), ConditionExpression="attribute_exists(#pk)", ExpressionAttributeNames=names, ExpressionAttributeValues=values, ReturnValues="ALL_NEW")["Attributes"]
    except ClientError as e:
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            raise NotFound("Registro no encontrado") from e
        raise

def delete_item(entity, item_id):
    key = TABLES[entity]["key"]
    try:
        table(entity).delete_item(Key={key: item_id}, ConditionExpression="attribute_exists(#pk)", ExpressionAttributeNames={"#pk": key})
    except ClientError as e:
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            raise NotFound("Registro no encontrado") from e
        raise


# Asignación transaccional: contador y registro se modifican juntos.
from datetime import datetime, timezone
from uuid import uuid4
from boto3.dynamodb.types import TypeSerializer

def _serialized(item):
    ser=TypeSerializer()
    return {k:ser.serialize(v) for k,v in item.items()}

def validate_provider_update(entity, item_id, data):
    if entity != "providers" or "licenciasTotales" not in data: return
    n=data["licenciasTotales"]
    if not isinstance(n,int) or isinstance(n,bool) or n<0: raise ValueError("Licencias totales debe ser un entero positivo o cero")
    p=get_by_id(entity,item_id)
    if not p: raise NotFound("Proveedor no encontrado")
    if n<int(p.get("licenciasAsignadas",0)): raise ValueError("No puedes reducir las licencias por debajo de las asignadas")

def validate_delete(entity, item_id):
    if entity=="providers" and any(l.get("providerId")==item_id for l in get_all("licenses")):
        raise ValueError("Primero libera las licencias asignadas a este software")
    if entity=="employees" and any(l.get("employeeId")==item_id for l in get_all("licenses")):
        raise ValueError("Primero libera las licencias de este empleado")

def assign_license(employee_id,provider_id):
    if not isinstance(employee_id,str) or not employee_id or not isinstance(provider_id,str) or not provider_id: raise ValueError("Selecciona empleado y software")
    if not get_by_id("employees",employee_id): raise NotFound("Empleado no encontrado")
    provider=get_by_id("providers",provider_id)
    if not provider: raise NotFound("Software no encontrado")
    if any(l.get("employeeId")==employee_id and l.get("providerId")==provider_id for l in get_all("licenses")):
        raise Duplicate("El empleado ya tiene asignado este software")
    license_id=str(uuid4()); record={"licenseId":license_id,"employeeId":employee_id,"providerId":provider_id,"fechaAsignacion":datetime.now(timezone.utc).date().isoformat(),"estado":"Asignada"}
    client=boto3.client("dynamodb",region_name=os.getenv("AWS_REGION","us-east-1"))
    try:
        client.transact_write_items(TransactItems=[
            {"Update":{"TableName":TABLES["providers"]["table"],"Key":_serialized({"providerId":provider_id}),"UpdateExpression":"SET #a = if_not_exists(#a, :zero) + :one","ConditionExpression":"attribute_exists(providerId) AND attribute_exists(#total) AND (attribute_not_exists(#a) OR #a < #total)","ExpressionAttributeNames":{"#a":"licenciasAsignadas","#total":"licenciasTotales"},"ExpressionAttributeValues":_serialized({":zero":0,":one":1})}},
            {"Put":{"TableName":TABLES["licenses"]["table"],"Item":_serialized(record),"ConditionExpression":"attribute_not_exists(licenseId)"}}
        ])
    except ClientError as e:
        if e.response["Error"]["Code"]=="TransactionCanceledException": raise ValueError("No hay licencias disponibles para este software") from e
        raise
    return record

def release_license(license_id):
    record=get_by_id("licenses",license_id)
    if not record: raise NotFound("Asignación no encontrada")
    provider_id=record.get("providerId")
    client=boto3.client("dynamodb",region_name=os.getenv("AWS_REGION","us-east-1"))
    client.transact_write_items(TransactItems=[
        {"Delete":{"TableName":TABLES["licenses"]["table"],"Key":_serialized({"licenseId":license_id}),"ConditionExpression":"attribute_exists(licenseId)"}},
        {"Update":{"TableName":TABLES["providers"]["table"],"Key":_serialized({"providerId":provider_id}),"UpdateExpression":"SET #a = #a - :one","ConditionExpression":"attribute_exists(providerId) AND #a >= :one","ExpressionAttributeNames":{"#a":"licenciasAsignadas"},"ExpressionAttributeValues":_serialized({":one":1})}}
    ])


def validate_provider_create(data):
    total=data.get("licenciasTotales",0)
    if not isinstance(total,int) or isinstance(total,bool) or total<0:
        raise ValueError("Las licencias contratadas deben ser un entero no negativo")
    data["licenciasTotales"]=total
    data["licenciasAsignadas"]=0
    if not str(data.get("nombre","")).strip(): raise ValueError("El software necesita un nombre")

