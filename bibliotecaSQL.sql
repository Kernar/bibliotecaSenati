CREATE DATABASE bibliotecaSenati;
use bibliotecaSenati;

CREATE TABLE Usuarios (
    usuario_id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(50),
    apellido VARCHAR(50),
    email VARCHAR(100) UNIQUE,
    contrasena VARCHAR(255),
    tipo_usuario ENUM('estudiante', 'personal'),
    nivel_acceso INT
);
select * from Usuarios;


-- Agregar usuario 1
INSERT INTO Usuarios (nombre, apellido, email, contrasena, tipo_usuario, nivel_acceso)
VALUES ('root', 'root', 'root@example.com', 'root', 'estudiante', 1);
INSERT INTO Usuarios (nombre, apellido, email, contrasena, tipo_usuario, nivel_acceso)
VALUES ('María', 'González', 'maria@example.com', 'password456', 'personal', 2);
INSERT INTO Usuarios (nombre, apellido, email, contrasena, tipo_usuario, nivel_acceso)
VALUES ('root', 'root', 'root', 'root', 'estudiante', 1);
INSERT INTO Usuarios (nombre, apellido, email, contrasena, tipo_usuario, nivel_acceso)
VALUES ('asd', 'asd', 'asd@example.com', 'asd', 'personal', 2);


CREATE TABLE Libros (
    libro_id INT PRIMARY KEY AUTO_INCREMENT,
    titulo VARCHAR(100),
    autor VARCHAR(100),
    categoria VARCHAR(50),
    palabras_clave TEXT,
    disponibilidad BOOLEAN,
    ubicacion VARCHAR(100)
);

ALTER TABLE Libros ADD en_reserva boolean;
select * from Libros;



CREATE TABLE Prestamos (
    prestamo_id INT PRIMARY KEY AUTO_INCREMENT,
    usuario_id INT,
    libro_id INT,
    fecha_prestamo DATE,
    fecha_devolucion DATE,
    devuelto BOOLEAN,
    FOREIGN KEY (usuario_id) REFERENCES Usuarios(usuario_id),
    FOREIGN KEY (libro_id) REFERENCES Libros(libro_id)
);

CREATE TABLE Reservas (
    reserva_id INT PRIMARY KEY AUTO_INCREMENT,
    usuario_id INT,
    libro_id INT,
    fecha_reserva DATE,
    estado_reserva ENUM('activa', 'cancelada', 'completada'),
    FOREIGN KEY (usuario_id) REFERENCES Usuarios(usuario_id),
    FOREIGN KEY (libro_id) REFERENCES Libros(libro_id)
);
ALTER TABLE Reservas ADD fecha_fin_reserva DATE;

CREATE TABLE Historial_Preferencias (
    preferencia_id INT PRIMARY KEY AUTO_INCREMENT,
    usuario_id INT,
    libro_id INT,
    fecha DATE,
    FOREIGN KEY (usuario_id) REFERENCES Usuarios(usuario_id),
    FOREIGN KEY (libro_id) REFERENCES Libros(libro_id)
);

CREATE TABLE Notificaciones (
    notificacion_id INT PRIMARY KEY AUTO_INCREMENT,
    usuario_id INT,
    mensaje TEXT,
    fecha DATE,
    FOREIGN KEY (usuario_id) REFERENCES Usuarios(usuario_id)
);

CREATE TABLE Recomendaciones (
    recomendacion_id INT PRIMARY KEY AUTO_INCREMENT,
    usuario_id INT,
    libro_id INT,
    motivo TEXT,
    fecha DATE,
    FOREIGN KEY (usuario_id) REFERENCES Usuarios(usuario_id),
    FOREIGN KEY (libro_id) REFERENCES Libros(libro_id)
);

CREATE TABLE Informes (
    informe_id INT PRIMARY KEY AUTO_INCREMENT,
    tipo_informe VARCHAR(50),
    fecha_generacion DATE,
    datos TEXT
);
