import { docClient } from "../config/dynamoClient.js";
import { PutCommand } from "@aws-sdk/lib-dynamodb";

const TABLE_NAME = process.env.DYNAMODB_TABLE_NAME || "SaasManagementTable";

export const seedDatabase = async () => {
  try {
    // 1. Empresa
    await docClient.send(new PutCommand({
      TableName: TABLE_NAME,
      Item: { PK: "ORG#ORG001", SK: "METADATA", nombre: "Empresa Demo", plan: "Enterprise" }
    }));

    // 2. Proveedor SaaS
    await docClient.send(new PutCommand({
      TableName: TABLE_NAME,
      Item: { PK: "ORG#ORG001", SK: "PROV#AWS", nombre: "Amazon Web Services", categoria: "Cloud" }
    }));

    // 3. Licencia
    await docClient.send(new PutCommand({
      TableName: TABLE_NAME,
      Item: { PK: "PROV#AWS", SK: "LIC#001", nombrePlan: "t3.micro Instance", costoMensual: 15.00, estado: "ACTIVA" }
    }));

    // 4. Empleado
    await docClient.send(new PutCommand({
      TableName: TABLE_NAME,
      Item: { PK: "ORG#ORG001", SK: "EMP#101", nombre: "Carlos Rivas", departamento: "TI" }
    }));

    console.log("✅ Datos relacionales creados exitosamente en DynamoDB.");
  } catch (error) {
    console.error("❌ Error al insertar datos:", error);
  }
};
