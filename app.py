from flask import Flask, render_template, request, redirect, url_for, flash, session
from config import Config
from flask_bcrypt import Bcrypt
from models import db, Usuario, Libro, Prestamo, Reserva  # Asegúrate de importar Prestamo
import datetime

# Inicializar Flask
app = Flask(__name__)
app.config.from_object(Config)

# Inicializar extensiones
db.init_app(app)
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Buscar al usuario por email
        user = Usuario.query.filter_by(email=email).first()
        
        # Verificar la contraseña
        if user and bcrypt.check_password_hash(user.contrasena, password):
            # Almacenar información del usuario en la sesión
            session['user_id'] = user.usuario_id
            session['nivel_acceso'] = user.nivel_acceso
            session['tipo_usuario'] = user.tipo_usuario
            
            # Redirigir según el tipo de usuario
            if user.tipo_usuario == 'personal':
                return redirect(url_for('gestionar_libros'))
            elif user.tipo_usuario == 'estudiante':
                return redirect(url_for('libreria'))
        
        # Mostrar mensaje de error si el inicio de sesión falla
        flash('Correo electrónico o contraseña incorrectos', 'danger')
    
    return render_template('login.html')

@app.route('/libreria')
def libreria():
    libros = Libro.query.all()  # Obtener todos los libros, tanto disponibles como no disponibles
    return render_template('libreria.html', libros=libros)

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
        password = request.form['password']

        if Usuario.query.filter_by(email=email).first():
            flash('Email ya registrado', 'danger')
            return redirect(url_for('registro'))

        nuevo_usuario = Usuario(
            nombre=nombre,
            apellido=apellido,
            email=email,
            contrasena=bcrypt.generate_password_hash(password).decode('utf-8'),
            tipo_usuario='estudiante',
            nivel_acceso=1
        )
        db.session.add(nuevo_usuario)
        db.session.commit()

        flash('Usuario registrado con éxito', 'success')
        return redirect(url_for('index'))
    
    return render_template('registro.html')

@app.route('/prestamo/<int:libro_id>')
def prestamo(libro_id):
    libro = Libro.query.get_or_404(libro_id)
    fecha_prestamo = datetime.datetime.now().date()
    return render_template('prestamo.html', libro=libro, fecha_prestamo=fecha_prestamo)

@app.route('/realizar_prestamo/<int:libro_id>', methods=['POST'])
def realizar_prestamo(libro_id):
    libro = Libro.query.get_or_404(libro_id)
    fecha_devolucion = request.form['fecha_devolucion']
    fecha_prestamo = datetime.datetime.now().date()

    prestamo = Prestamo(
        usuario_id=session['user_id'],  # ID del usuario actualmente autenticado
        libro_id=libro_id,
        fecha_prestamo=fecha_prestamo,
        fecha_devolucion=fecha_devolucion,
        devuelto=False
    )
    
    libro.disponibilidad = False  # Cambiar la disponibilidad del libro a False
    
    db.session.add(prestamo)
    db.session.commit()

    flash('Préstamo realizado con éxito', 'success')
    return redirect(url_for('libreria'))

@app.route('/devolver_prestamo/<int:prestamo_id>', methods=['POST'])
def devolver_prestamo(prestamo_id):
    prestamo = Prestamo.query.get_or_404(prestamo_id)
    prestamo.devuelto = True
    
    libro = Libro.query.get(prestamo.libro_id)
    libro.disponibilidad = True  # Cambiar la disponibilidad del libro a True
    
    db.session.commit()

    flash('Libro devuelto con éxito', 'success')
    return redirect(url_for('libreria'))

@app.route('/reservar/<int:libro_id>')
def reservar(libro_id):
    libro = Libro.query.get_or_404(libro_id)
    fecha_reserva = datetime.datetime.now().date() + datetime.timedelta(days=1)  # Día siguiente
    fecha_fin_reserva = fecha_reserva + datetime.timedelta(days=14)  # Reserva por 14 días

    return render_template('reservar.html', libro=libro, fecha_reserva=fecha_reserva, fecha_fin_reserva=fecha_fin_reserva)

@app.route('/reservar_libro/<int:libro_id>', methods=['POST'])
def reservar_libro(libro_id):
    libro = Libro.query.get_or_404(libro_id)
    fecha_reserva = datetime.datetime.now().date()

    reserva = Reserva(
        usuario_id=session['user_id'],  # ID del usuario actualmente autenticado
        libro_id=libro_id,
        fecha_reserva=fecha_reserva,
        estado_reserva='activa'
    )
    
    db.session.add(reserva)
    db.session.commit()

    flash('Reserva realizada con éxito', 'success')
    return redirect(url_for('libreria'))

@app.route('/confirmar_reserva/<int:libro_id>', methods=['POST'])
def confirmar_reserva(libro_id):
    libro = Libro.query.get_or_404(libro_id)
    fecha_reserva = datetime.datetime.now().date() + datetime.timedelta(days=1)
    
    reserva = Reserva(
        usuario_id=session['user_id'],  # Debería ser el ID del usuario actualmente autenticado
        libro_id=libro_id,
        fecha_reserva=fecha_reserva,
        estado_reserva='activa'
    )
    
    db.session.add(reserva)
    db.session.commit()
    
    flash('Reserva realizada con éxito', 'success')
    return redirect(url_for('libreria'))

@app.route('/gestionar_libros')
def gestionar_libros():
    # Verificar si el usuario ha iniciado sesión y tiene nivel de acceso 2 y es personal
    if not session.get('user_id') or session.get('nivel_acceso') != 2 or session.get('tipo_usuario') != 'personal':
        return redirect(url_for('index'))
    
    libros = Libro.query.all()
    return render_template('gestionar_libros.html', libros=libros)

@app.route('/modificar_libro/<int:libro_id>')
def modificar_libro(libro_id):
    # Verificar si el usuario ha iniciado sesión y tiene nivel de acceso 2 y es personal
    if not session.get('user_id') or session.get('nivel_acceso') != 2 or session.get('tipo_usuario') != 'personal':
        return redirect(url_for('index'))
    
    libro = Libro.query.get_or_404(libro_id)
    return render_template('modificar_libro.html', libro=libro)

@app.route('/actualizar_libro/<int:libro_id>', methods=['POST'])
def actualizar_libro(libro_id):
    # Verificar si el usuario ha iniciado sesión y tiene nivel de acceso 2 y es personal
    if not session.get('user_id') or session.get('nivel_acceso') != 2 or session.get('tipo_usuario') != 'personal':
        return redirect(url_for('index'))
    
    libro = Libro.query.get_or_404(libro_id)
    libro.disponibilidad = request.form.get('disponibilidad') == 'true'
    libro.en_reserva = request.form.get('en_reserva') == 'true'
    db.session.commit()
    return redirect(url_for('gestionar_libros'))

if __name__ == '__main__':
    app.run(debug=True)
