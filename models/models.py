from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone

db = SQLAlchemy()

class Turnos(db.Model):
    __tablename__ = 'turnos'
    turno_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    identificador = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(100), nullable=True)
    alumnos = db.relationship("Alumnos", backref="turnos", lazy=True)
    
    def __repr__(self):
        return '<Turno %r>' % self.identificador
    
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class AlumnosCursos(db.Model):
    __tablename__ = 'alumnos_cursos'
    alumno_id = db.Column(db.Integer, db.ForeignKey('alumnos.alumno_id'), primary_key=True)
    curso_id = db.Column(db.Integer, db.ForeignKey('cursos.curso_id'), primary_key=True)
    activo = db.Column(db.Boolean, default=True)
    fecha = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), server_default=func.now(), nullable=False)

    alumno = db.relationship('Alumnos', backref=db.backref('alumnos_cursos'))
    curso = db.relationship('Cursos', backref=db.backref('alumnos_cursos'))

    def __repr__(self):
        return f'<AlumnosCursos {self.alumno_id} - {self.curso_id}>'
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Docentes(db.Model):
    __tablename__ = 'docentes'
    docente_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_completo = db.Column(db.String(200), nullable=False)
    nombres = db.Column(db.String(200), nullable=True)
    primer_apellido = db.Column(db.String(200), nullable=True)
    segundo_apellido = db.Column(db.String(200), nullable=True)
    usuario = db.Column(db.String(200), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    activo = db.Column(db.Boolean, default=True, nullable=False)
    rol = db.Column(db.String(255), nullable=False, default='normal')

    def __repr__(self):
        return '<Docente %r>' % self.nombre_completo
    
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Alumnos(db.Model):
    __tablename__ = 'alumnos'
    alumno_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_completo = db.Column(db.String(200), nullable=False)
    nombres = db.Column(db.String(200), nullable=True)
    primer_apellido = db.Column(db.String(200), nullable=True)
    segundo_apellido = db.Column(db.String(200), nullable=True)
    turno_id = db.Column(db.Integer, db.ForeignKey('turnos.turno_id'), nullable=True)
    activo = db.Column(db.Boolean, default=True)
    folio = db.Column(db.String(200), nullable=False)
    cursos = db.relationship('Cursos', secondary='alumnos_cursos', backref=db.backref('alumnos', lazy='dynamic'))

    def __repr__(self):
        return '<Alumno %r>' % self.nombre_completo
    
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
class Cursos(db.Model):
    __tablename__ = 'cursos'
    curso_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    identificador = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return '<Turno %r>' % self.identificador
    
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Asistencias(db.Model):
    __tablename__ = 'asistencias'
    asistencia_id = db.Column(db.Integer, primary_key=True)
    alumno_id = db.Column(db.Integer, nullable=False)
    curso_id = db.Column(db.Integer, nullable=False)
    fecha = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), server_default=func.now(), nullable=False)
    presento_actividad = db.Column(db.Boolean, nullable=False, default=False)
    registrado_siri = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f'<Asistencia {self.asistencia_id} - Alumno: {self.alumno_id} - Curso: {self.curso_id}>'
    
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
