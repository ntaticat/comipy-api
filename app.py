
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy.orm import relationship

import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.debug = False
CORS(app)

mysqluri = os.getenv("MYSQL_STRING")

app.config['SQLALCHEMY_DATABASE_URI'] = mysqluri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



class Turnos(db.Model):
    turno_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    identificador = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(100), nullable=True)
    alumnos = db.relationship("Alumnos", backref="turnos", lazy=True)
    
    def __repr__(self):
        return '<Turno %r>' % self.identificador
    
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Alumnos(db.Model):
    alumno_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_completo = db.Column(db.String(200), nullable=False)
    nombres = db.Column(db.String(200), nullable=True)
    primer_apellido = db.Column(db.String(200), nullable=True)
    segundo_apellido = db.Column(db.String(200), nullable=True)
    turno_id = db.Column(db.Integer, db.ForeignKey('turnos.turno_id'), nullable=True)
    activo = db.Column(db.Boolean, default=True)
    folio = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<Alumno %r>' % self.nombre_completo
    
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

# Ruta para obtener todos los alumnos
@app.route('/api/alumnos', methods=['POST'])
def crear_alumno():
    if not request.json:
        return jsonify({'error': 'No se proporcionaron datos JSON'}), 400

    datos_alumno = request.json
    nombre_completo=datos_alumno.get('nombre_completo')
    nombres=datos_alumno.get('nombres')
    primer_apellido=datos_alumno.get('primer_apellido')
    segundo_apellido=datos_alumno.get('segundo_apellido')
    turno_id=datos_alumno.get('turno_id')
    activo=datos_alumno.get('activo')
    folio=datos_alumno.get('folio')

    nuevo_alumno = Alumnos(nombre_completo=nombre_completo, nombres=nombres, primer_apellido=primer_apellido, segundo_apellido=segundo_apellido, turno_id=turno_id, activo=activo, folio=folio)
    db.session.add(nuevo_alumno)
    db.session.commit()
    return 'Alumno creado'

@app.route('/api/alumnos', methods=['GET'])
def obtener_alumnos():
    alumnos = Alumnos.query.all()
    alumnos_json = [alumno.as_dict() for alumno in alumnos]
    
    return jsonify(alumnos_json)

@app.route('/api/alumnos/<int:alumno_id>', methods=['PUT'])
def actualizar_alumno(alumno_id):
    if not request.json:
        return jsonify({'error': 'No se proporcionaron datos JSON'}), 400
    
    alumno = Alumnos.query.get(alumno_id)
    if not alumno:
        return 'Alumno no encontrado', 404

    datos_alumno = request.json
    nombre_completo=datos_alumno.get('nombre_completo')
    nombres=datos_alumno.get('nombres')
    primer_apellido=datos_alumno.get('primer_apellido')
    segundo_apellido=datos_alumno.get('segundo_apellido')
    turno_id=datos_alumno.get('turno_id')
    activo=datos_alumno.get('activo')
    folio=datos_alumno.get('folio')
    
    alumno.nombres = 'Nuevo nombre de Rafael'

    alumno.nombre_completo=nombre_completo
    alumno.nombres=nombres
    alumno.primer_apellido=primer_apellido
    alumno.segundo_apellido=segundo_apellido
    alumno.turno_id=turno_id
    alumno.activo=activo
    alumno.folio=folio

    db.session.commit()
    return 'Alumno actualizado'

@app.route('/api/alumnos/<int:alumno_id>', methods=['DELETE'])
def eliminar_alumno(alumno_id):
    alumno = Alumnos.query.get(alumno_id)
    if not alumno:
        return 'Alumno no encontrado', 404
    db.session.delete(alumno)
    db.session.commit()
    return 'Alumno eliminado'

@app.route('/api/turnos', methods=['POST'])
def crear_turno():
    nuevo_turno = Turnos(identificador='NUEVOIDENT', descripcion='DESC')
    db.session.add(nuevo_turno)
    db.session.commit()
    return 'Turno creado'

if __name__ == '__main__':
    app.run(host='0.0.0.0')