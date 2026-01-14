import sqlite3

conn = sqlite3.connect('reservas.db')
c = conn.cursor()

# Tabla restaurante
c.execute('''
CREATE TABLE IF NOT EXISTS restaurante(
    id_restaurante INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT,
    hora_apertura TEXT,
    hora_cierre TEXT,
    duracion_reserva INTEGER,
    max_dias_reserva INTEGER
)
''')

# Tabla mesa
c.execute('''
CREATE TABLE IF NOT EXISTS mesa(
    id_mesa INTEGER PRIMARY KEY AUTOINCREMENT,
    id_restaurante INTEGER,
    capacidad INTEGER
)
''')

# Tabla reserva
c.execute('''
CREATE TABLE IF NOT EXISTS reserva(
    id_reserva INTEGER PRIMARY KEY AUTOINCREMENT,
    id_restaurante INTEGER,
    id_mesa INTEGER,
    nombre_cliente TEXT,
    telefono TEXT,
    fecha TEXT,
    hora_inicio TEXT,
    hora_fin TEXT,
    num_personas INTEGER
)
''')

# Insertar ejemplo restaurante
c.execute("INSERT INTO restaurante (nombre, hora_apertura, hora_cierre, duracion_reserva, max_dias_reserva) VALUES (?, ?, ?, ?, ?)",
          ("Restaurante Ejemplo", "12:00", "22:00", 90, 30))

# Insertar mesas ejemplo
for capacidad in [2, 4, 4, 6]:
    c.execute("INSERT INTO mesa (id_restaurante, capacidad) VALUES (?, ?)", (1, capacidad))

conn.commit()
conn.close()
print("Base de datos creada con éxito")
