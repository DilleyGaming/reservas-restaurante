from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)
DB = 'reservas.db'

# Función para comprobar mesas disponibles
def mesas_disponibles(fecha, hora_inicio, num_personas):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT id_mesa, capacidad FROM mesa WHERE capacidad >= ?", (num_personas,))
    mesas = c.fetchall()
    disponibles = []
    for mesa_id, capacidad in mesas:
        c.execute("""
        SELECT * FROM reserva
        WHERE id_mesa = ? AND fecha = ? AND (
            (hora_inicio <= ? AND hora_fin > ?) OR
            (hora_inicio < ? AND hora_fin >= ?)
        )
        """, (mesa_id, fecha, hora_inicio, hora_inicio, hora_inicio, hora_inicio))
        if not c.fetchall():
            disponibles.append({'id_mesa': mesa_id, 'capacidad': capacidad})
    conn.close()
    return disponibles

# Página cliente
@app.route('/')
def index():
    return render_template('index.html')

# Página admin / tablet
@app.route('/admin')
def admin():
    return render_template('admin.html')

# API: mesas disponibles
@app.route('/api/disponibles', methods=['POST'])
def api_disponibles():
    data = request.json
    fecha = data['fecha']
    hora = data['hora']
    num_personas = int(data['num_personas'])
    disponibles = mesas_disponibles(fecha, hora, num_personas)
    return jsonify(disponibles)

# API: crear reserva
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

    # Calcular hora_fin según duración del restaurante
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT duracion_reserva FROM restaurante WHERE id_restaurante = 1")
    duracion = c.fetchone()[0]
    hora_inicio_dt = datetime.strptime(hora, "%H:%M")
    hora_fin_dt = hora_inicio_dt + timedelta(minutes=duracion)
    hora_fin = hora_fin_dt.strftime("%H:%M")

    c.execute("""
    INSERT INTO reserva (id_restaurante, id_mesa, nombre_cliente, telefono, fecha, hora_inicio, hora_fin, num_personas)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (1, mesa_id, nombre, telefono, fecha, hora, hora_fin, num_personas))

    conn.commit()
    conn.close()
    return jsonify({'status': 'ok', 'mesa': mesa_id, 'hora_fin': hora_fin})

# API: listar reservas para admin (con id_reserva)
@app.route('/api/reservas')
def api_reservas():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT id_reserva, nombre_cliente, telefono, fecha, hora_inicio, hora_fin, num_personas, id_mesa FROM reserva")
    reservas = c.fetchall()
    conn.close()
    return jsonify([{
        'id': r[0],
        'nombre': r[1],
        'telefono': r[2],
        'fecha': r[3],
        'hora_inicio': r[4],
        'hora_fin': r[5],
        'num_personas': r[6],
        'mesa': r[7]
    } for r in reservas])

# API: borrar reserva
@app.route('/api/reserva/<int:id_reserva>', methods=['DELETE'])
def api_borrar_reserva(id_reserva):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("DELETE FROM reserva WHERE id_reserva = ?", (id_reserva,))
    conn.commit()
    conn.close()
    return jsonify({'status': 'ok', 'message': 'Reserva borrada'})

if __name__ == '__main__':
    app.run(debug=True)
