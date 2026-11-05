from flask import Flask, jsonify
import boto3
import os
from dotenv import load_dotenv

# Cargar las variables del archivo .env
load_dotenv()

app = Flask(__name__)

# Configuración del recurso de DynamoDB utilizando boto3
dynamodb = boto3.resource(
    'dynamodb',
    region_name=os.getenv('AWS_REGION', 'us-east-1'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

TABLE_NAME = os.getenv('DYNAMODB_TABLE_NAME', 'SaasManagementTable')

@app.route('/')
def home():
    return jsonify({
        "status": "success",
        "message": "API Backend de Licentra (Gestión de Licencias SaaS) funcionando correctamente 🚀"
    })

# Ruta de prueba para verificar la conexión con DynamoDB
@app.route('/api/test-db', methods=['GET'])
def test_db():
    try:
        table = dynamodb.Table(TABLE_NAME)
        response = table.scan(Limit=5)
        return jsonify({
            "status": "success",
            "message": "Conexión exitosa con DynamoDB",
            "items": response.get('Items', [])
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)