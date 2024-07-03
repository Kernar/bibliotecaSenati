from app import app, db, bcrypt
from models import Usuario

with app.app_context():
    users = Usuario.query.all()
    
    for user in users:
        if not user.contrasena.startswith('$2b$'):
            user.contrasena = bcrypt.generate_password_hash(user.contrasena).decode('utf-8')
            db.session.add(user)
    
    db.session.commit()

print("Contraseñas cifradas y actualizadas con éxito.")
