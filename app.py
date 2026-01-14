from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import os

app = Flask(__name__)

# Conexión a PostgreSQL usando variable de entorno
DATABASE_URL = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Tablas
class Mesa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    capacidad = db.Column(db.Integer, nullable=False)

class Reserva(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_cliente = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(50), nullable=False)
    fecha = db.Column(db.String(20), nullable=False)
    hora_inicio = db.Column(db.String(10), nullable=False)
    hora_fin = db.Column(db.String(10), nullable=False)
    num_personas = db.Column(db.Integer, nullable=False)
    mesa = db.Column(db.Integer, db.ForeignKey('mesa.id'), nullable=False)

with app.app_context():
    db.create_all()

# Función para comprobar mesas disponibles
def mesas_disponibles(fecha, hora, num_personas):
    reservas = Reserva.query.filter_by(fecha=fecha).all()
    mesas = Mesa.query.filter(Mesa.capacidad >= num_personas).all()
    disponibles = []

    hora_dt = datetime.strptime(hora, "%H:%M")

    for mesa in mesas:
        ocupada = False
        for r in reservas:
            if r.mesa == mesa.id:
                r_inicio = datetime.strptime(r.hora_inicio, "%H:%M")
                r_fin = datetime.strptime(r.hora_fin, "%H:%M")
                if (hora_dt >= r_inicio and hora_dt < r_fin):
                    ocupada = True
                    break
        if not ocupada:
            disponibles.append({'id_mesa': mesa.id})
    return disponibles

# Crear reserva
@app.route('/api/reserva', methods=['POST'])
def api_reserva():
    data = request.json
    fecha = data['fecha']
    hora = data['hora']
    num_personas = int(data['num_personas'])
    nombre = data['nombre']
    telefono = data['telefono']

    disponibles = mesas_disponibles(fecha, hora, num_personas)
    if not disponibles:
        return jsonify({'status': 'error', 'message': 'No hay mesas disponibles'}), 400

    mesa_id = disponibles[0]['id_mesa']

    # Suponemos duración de reserva: 90 minutos
    duracion = 90
    hora_inicio_dt = datetime.strptime(hora, "%H:%M")
    hora_fin_dt = hora_inicio_dt + timedelta(minutes=duracion)
    hora_fin = hora_fin_dt.strftime("%H:%M")

    reserva = Reserva(
        nombre_cliente=nombre,
        telefono=telefono,
        fecha=fecha,
        hora_inicio=hora,
        hora_fin=hora_fin,
        num_personas=num_personas,
        mesa=mesa_id
    )
    db.session.add(reserva)
    db.session.commit()

    return jsonify({'status': 'ok', 'mesa': mesa_id, 'hora_fin': hora_fin})

# Listar reservas
@app.route('/api/reservas', methods=['GET'])
def api_reservas():
    reservas = Reserva.query.all()
    resultado = []
    for r in reservas:
        resultado.append({
            'nombre': r.nombre_cliente,
            'telefono': r.telefono,
            'fecha': r.fecha,
            'hora_inicio': r.hora_inicio,
            'hora_fin': r.hora_fin,
            'num_personas': r.num_personas,
            'mesa': r.mesa
        })
    return jsonify(resultado)

# Borrar reserva por ID
@app.route('/api/reserva/<int:id>', methods=['DELETE'])
def borrar_reserva(id):
    reserva = Reserva.query.get(id)
    if not reserva:
        return jsonify({'status': 'error', 'message': 'Reserva no encontrada'}), 404
    db.session.delete(reserva)
    db.session.commit()
    return jsonify({'status': 'ok', 'message': 'Reserva eliminada'})

@app.route('/')
def index():
    return "API de reservas funcionando ✅"

if __name__ == '__main__':
    app.run(debug=True)
