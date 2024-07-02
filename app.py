from flask import Flask, render_template, request, redirect, url_for, flash
from config import Config
from models import db, Usuario, Libro
from werkzeug.security import check_password_hash

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
    libros = Libro.query.all()
    return render_template('libreria.html', libros=libros)

if __name__ == '__main__':
    app.run(debug=True)
