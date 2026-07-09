from flask import Flask, request, jsonify
from flask_cors import CORS
from back_devops.database import get_connection

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return jsonify({
        "mensaje": "Backend funcionando correctamente"
    })


@app.route("/productos", methods=["GET"])
def obtener_productos():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM productos ORDER BY id")
    productos = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(productos)


@app.route("/productos/<int:id>", methods=["GET"])
def obtener_producto(id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM productos WHERE id = %s", (id,))
    producto = cursor.fetchone()

    cursor.close()
    conn.close()

    if producto is None:
        return jsonify({"mensaje": "Producto no encontrado"}), 404

    return jsonify(producto)


@app.route("/productos", methods=["POST"])
def crear_producto():
    datos = request.get_json()

    nombre = datos.get("nombre")
    precio = datos.get("precio")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO productos (nombre, precio)
        VALUES (%s, %s)
        RETURNING id
        """,
        (nombre, precio)
    )

    nuevo_id = cursor.fetchone()["id"]

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({
        "mensaje": "Producto creado correctamente",
        "id": nuevo_id
    }), 201


@app.route("/productos/<int:id>", methods=["PUT"])
def actualizar_producto(id):
    datos = request.get_json()

    nombre = datos.get("nombre")
    precio = datos.get("precio")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE productos
        SET nombre = %s,
            precio = %s
        WHERE id = %s
        """,
        (nombre, precio, id)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({
        "mensaje": "Producto actualizado correctamente"
    })


@app.route("/productos/<int:id>", methods=["DELETE"])
def eliminar_producto(id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM productos WHERE id = %s",
        (id,)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({
        "mensaje": "Producto eliminado correctamente"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)