import os
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:5000")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/productos", methods=["GET"])
def listar_productos():
    response = requests.get(f"{BACKEND_URL}/productos", timeout=10)
    return jsonify(response.json()), response.status_code


@app.route("/api/productos", methods=["POST"])
def crear_producto():
    response = requests.post(
        f"{BACKEND_URL}/productos",
        json=request.get_json(),
        timeout=10
    )
    return jsonify(response.json()), response.status_code


@app.route("/api/productos/<int:id>", methods=["PUT"])
def actualizar_producto(id):
    response = requests.put(
        f"{BACKEND_URL}/productos/{id}",
        json=request.get_json(),
        timeout=10
    )
    return jsonify(response.json()), response.status_code


@app.route("/api/productos/<int:id>", methods=["DELETE"])
def eliminar_producto(id):
    response = requests.delete(
        f"{BACKEND_URL}/productos/{id}",
        timeout=10
    )

    if response.text:
        return jsonify(response.json()), response.status_code

    return jsonify({"mensaje": "Producto eliminado"}), response.status_code


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)