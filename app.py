from flask import Flask, render_template, request, redirect, url_for, flash
from config import Config
from models import db, Usuario, Libro, Prestamo, Reserva  # Asegúrate de importar Prestamo
import datetime

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    user = Usuario.query.filter_by(email=email).first()
    
    
    if user and user.contrasena == password:  # Comparación de contraseñas en texto plano
        return redirect(url_for('libreria'))
    else:
        flash('Invalid email or password', 'error')
        return redirect(url_for('index'))
    

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
        contrasena = request.form['contrasena']
        tipo_usuario = request.form['tipo_usuario']
        nivel_acceso = request.form['nivel_acceso']
        
        nuevo_usuario = Usuario(
            nombre=nombre,
            apellido=apellido,
            email=email,
            contrasena=contrasena,  # Si decides encriptar la contraseña, usa generate_password_hash(contrasena)
            tipo_usuario=tipo_usuario,
            nivel_acceso=nivel_acceso
        )
        
        db.session.add(nuevo_usuario)
        db.session.commit()
        
        flash('Usuario registrado con éxito', 'success')
        return redirect(url_for('login'))
    
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
        usuario_id=1,  # Esto debería ser el ID del usuario actualmente autenticado
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
    fecha_fin_reserva = fecha_reserva + datetime.timedelta(days=14)  # Reserva por 14 días (puedes ajustar el número de días)

    return render_template('reservar.html', libro=libro, fecha_reserva=fecha_reserva, fecha_fin_reserva=fecha_fin_reserva)



@app.route('/reservar_libro/<int:libro_id>', methods=['POST'])
def reservar_libro(libro_id):
    libro = Libro.query.get_or_404(libro_id)
    fecha_reserva = datetime.datetime.now().date()

    reserva = Reserva(
        usuario_id=1,  # Esto debería ser el ID del usuario actualmente autenticado
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
        usuario_id=1,  # Debería ser el ID del usuario actualmente autenticado
        libro_id=libro_id,
        fecha_reserva=fecha_reserva,
        estado_reserva='activa'
    )
    
    db.session.add(reserva)
    db.session.commit()
    
    flash('Reserva realizada con éxito', 'success')
    return redirect(url_for('libreria'))



if __name__ == '__main__':
    app.run(debug=True)
