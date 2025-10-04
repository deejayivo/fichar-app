from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

# Configuración de la base de datos
DATABASE_URL = os.environ.get("DATABASE_URL")  # Render te da esta URL
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Modelo de fichaje
class Fichaje(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(100), nullable=False)
    accion = db.Column(db.String(10), nullable=False)  # "entrada" o "salida"
    hora = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "usuario": self.usuario,
            "accion": self.accion,
            "hora": self.hora.isoformat()
        }

@app.before_first_request
def crear_tablas():
    db.create_all()

@app.route("/")
def home():
    return "Hola 👋, tu aplicación de fichaje está funcionando"

@app.route("/fichar", methods=["POST"])
def fichar():
    data = request.get_json()
    if not data or "usuario" not in data or "accion" not in data:
        return jsonify({"error": "Faltan datos"}), 400

    usuario = data["usuario"]
    accion = data["accion"].lower()
    if accion not in ["entrada", "salida"]:
        return jsonify({"error": "Acción inválida"}), 400

    fichaje = Fichaje(usuario=usuario, accion=accion)
    db.session.add(fichaje)
    db.session.commit()

    return jsonify({"mensaje": "Fichaje registrado", "fichaje": fichaje.to_dict()})

@app.route("/historial/<usuario>", methods=["GET"])
def historial(usuario):
    fichajes_usuario = Fichaje.query.filter_by(usuario=usuario).all()
    return jsonify({"usuario": usuario, "historial": [f.to_dict() for f in fichajes_usuario]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
