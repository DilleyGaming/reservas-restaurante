from app import db, Mesa, Reserva, app

with app.app_context():
    # Crear tablas si no existen
    db.create_all()

    # Crear mesas de ejemplo si no existen
    if Mesa.query.count() == 0:
        mesas_ejemplo = [
            Mesa(capacidad=2),
            Mesa(capacidad=2),
            Mesa(capacidad=4),
            Mesa(capacidad=4),
            Mesa(capacidad=6)
        ]
        db.session.add_all(mesas_ejemplo)
        db.session.commit()
        print("Mesas de ejemplo creadas ✅")
    else:
        print("Mesas ya existentes, no se crean nuevas.")

    # Crear reservas de prueba (opcional)
    if Reserva.query.count() == 0:
        from datetime import datetime, timedelta

        # Tomamos hora actual y añadimos reservas de prueba
        fecha = datetime.now().strftime("%Y-%m-%d")
        hora_inicio = "12:00"
        duracion = 90
        hora_fin = (datetime.strptime(hora_inicio, "%H:%M") + timedelta(minutes=duracion)).strftime("%H:%M")

        reserva_prueba = Reserva(
            nombre_cliente="Cliente Test",
            telefono="123456789",
            fecha=fecha,
            hora_inicio=hora_inicio,
            hora_fin=hora_fin,
            num_personas=2,
            mesa=1  # primera mesa
        )
        db.session.add(reserva_prueba)
        db.session.commit()
        print("Reserva de prueba creada ✅")
    else:
        print("Reservas ya existen, no se crean nuevas.")
