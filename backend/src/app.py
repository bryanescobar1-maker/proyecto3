import os
from decimal import Decimal
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
from apig_wsgi import make_lambda_handler
from services.dynamodb import assign_license, release_license, validate_provider_update, validate_delete, TABLES, get_all, get_by_id, create_item, update_item, delete_item, Duplicate, NotFound, validate_provider_create

load_dotenv()
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": os.getenv("FRONTEND_ORIGIN", "http://localhost:5500").split(",")}})

def normalize(v):
    if isinstance(v, Decimal): return int(v) if v % 1 == 0 else float(v)
    if isinstance(v, list): return [normalize(x) for x in v]
    if isinstance(v, dict): return {k: normalize(x) for k, x in v.items()}
    return v

def decimalize(v):
    if isinstance(v, float): return Decimal(str(v))
    if isinstance(v, list): return [decimalize(x) for x in v]
    if isinstance(v, dict): return {k: decimalize(x) for k, x in v.items()}
    return v

@app.get("/")
def home(): return jsonify(mensaje="Backend LICENTRA", estado="funcionando")

@app.get("/health")
def health(): return jsonify(servicio="LICENTRA", estado="activo")

@app.route("/api/<entity>", methods=["GET", "POST"])
def collection(entity):
    if entity not in TABLES: return jsonify(error="Entidad no válida"), 404
    try:
        if request.method == "GET": return jsonify(normalize(get_all(entity)))
        data = request.get_json(silent=True)
        if not isinstance(data, dict): return jsonify(error="Envía un objeto JSON"), 400
        key = TABLES[entity]["key"]
        if not isinstance(data.get(key), str) or not data[key].strip(): return jsonify(error=f"{key} debe ser una cadena no vacía"), 400
        if entity=="providers": validate_provider_create(data)
        return jsonify(mensaje="Registro creado", registro=normalize(create_item(entity, decimalize(data)))), 201
    except Duplicate as e: return jsonify(error=str(e)), 409
    except (ValueError, TypeError) as e: return jsonify(error=str(e)), 400
    except Exception:
        app.logger.exception("Error en colección")
        return jsonify(error="Error de servidor"), 500

@app.route("/api/<entity>/<item_id>", methods=["GET", "PUT", "DELETE"])
def item(entity, item_id):
    if entity not in TABLES: return jsonify(error="Entidad no válida"), 404
    try:
        if request.method == "GET":
            value = get_by_id(entity, item_id)
            return (jsonify(normalize(value)), 200) if value else (jsonify(error="Registro no encontrado"), 404)
        if request.method == "DELETE":
            validate_delete(entity, item_id)
            delete_item(entity, item_id)
            return jsonify(mensaje="Registro eliminado")
        data = request.get_json(silent=True)
        if not isinstance(data, dict) or not data: return jsonify(error="Envía campos para actualizar"), 400
        validate_provider_update(entity, item_id, data)
        updated = update_item(entity, item_id, decimalize(data))
        return jsonify(mensaje="Registro actualizado", registro=normalize(updated))
    except NotFound as e: return jsonify(error=str(e)), 404
    except (ValueError, TypeError) as e: return jsonify(error=str(e)), 400
    except Exception:
        app.logger.exception("Error en registro")
        return jsonify(error="Error de servidor"), 500


@app.post("/api/assignments")
def assignment_create():
    try:
        data=request.get_json(silent=True) or {}
        record=assign_license(data.get("employeeId"),data.get("providerId"))
        return jsonify(mensaje="Licencia asignada",registro=normalize(record)),201
    except (ValueError, TypeError) as e: return jsonify(error=str(e)),400
    except NotFound as e: return jsonify(error=str(e)),404
    except Duplicate as e: return jsonify(error=str(e)),409
    except Exception:
        app.logger.exception("Error al asignar")
        return jsonify(error="Error de servidor"),500

@app.delete("/api/assignments/<license_id>")
def assignment_delete(license_id):
    try:
        release_license(license_id)
        return jsonify(mensaje="Licencia liberada")
    except NotFound as e: return jsonify(error=str(e)),404
    except (ValueError, TypeError) as e: return jsonify(error=str(e)),400
    except Exception:
        app.logger.exception("Error al liberar")
        return jsonify(error="Error de servidor"),500

lambda_handler = make_lambda_handler(app)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=os.getenv("FLASK_DEBUG") == "1")
