from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "message": "Licentra API funcionando"
    })
m
if __name__ == "__main__":
    app.run()
