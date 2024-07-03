from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'Usuarios'
    usuario_id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    contrasena = db.Column(db.String(255), nullable=False)
    tipo_usuario = db.Column(db.Enum('estudiante', 'personal'), nullable=False)
    nivel_acceso = db.Column(db.Integer, nullable=False)

class Libro(db.Model):
    __tablename__ = 'Libros'
    libro_id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    autor = db.Column(db.String(100), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    palabras_clave = db.Column(db.Text)
    disponibilidad = db.Column(db.Boolean, nullable=False, default=True)
    ubicacion = db.Column(db.String(100), nullable=False)
    en_reserva = db.Column(db.Boolean, nullable=False, default=False)


class Prestamo(db.Model):
    __tablename__ = 'Prestamos'
    prestamo_id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('Usuarios.usuario_id'), nullable=False)
    libro_id = db.Column(db.Integer, db.ForeignKey('Libros.libro_id'), nullable=False)
    fecha_prestamo = db.Column(db.Date, nullable=False)
    fecha_devolucion = db.Column(db.Date)
    devuelto = db.Column(db.Boolean, nullable=False, default=False)

class Reserva(db.Model):
    __tablename__ = 'Reservas'
    reserva_id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('Usuarios.usuario_id'), nullable=False)
    libro_id = db.Column(db.Integer, db.ForeignKey('Libros.libro_id'), nullable=False)
    fecha_reserva = db.Column(db.Date, nullable=False)
    estado_reserva = db.Column(db.Enum('activa', 'cancelada', 'completada'), nullable=False)

class HistorialPreferencia(db.Model):
    __tablename__ = 'Historial_Preferencias'
    preferencia_id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('Usuarios.usuario_id'), nullable=False)
    libro_id = db.Column(db.Integer, db.ForeignKey('Libros.libro_id'), nullable=False)
    fecha = db.Column(db.Date, nullable=False)

class Notificacion(db.Model):
    __tablename__ = 'Notificaciones'
    notificacion_id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('Usuarios.usuario_id'), nullable=False)
    mensaje = db.Column(db.Text, nullable=False)
    fecha = db.Column(db.Date, nullable=False)

class Recomendacion(db.Model):
    __tablename__ = 'Recomendaciones'
    recomendacion_id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('Usuarios.usuario_id'), nullable=False)
    libro_id = db.Column(db.Integer, db.ForeignKey('Libros.libro_id'), nullable=False)
    motivo = db.Column(db.Text, nullable=False)
    fecha = db.Column(db.Date, nullable=False)

class Informe(db.Model):
    __tablename__ = 'Informes'
    informe_id = db.Column(db.Integer, primary_key=True)
    tipo_informe = db.Column(db.String(50), nullable=False)
    fecha_generacion = db.Column(db.Date, nullable=False)
    datos = db.Column(db.Text, nullable=False)
