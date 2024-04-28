# Toca hacer ruta para crear docente y para eliminar

from flask import Blueprint, jsonify, request
from models.models import db
from models.models import Docentes
from auth.auth import verificar_jwt, solo_admin

docentes_routes = Blueprint('docentes_routes', __name__)

@docentes_routes.route('/api/docentes', methods=['POST'])
@solo_admin
def crear_docente():
    if not request.json:
        return jsonify({'error': 'No se proporcionaron datos JSON'}), 400

    datos_docente = request.json
    email=datos_docente.get('email')

    if Docentes.query.filter_by(email=email).first():
        return jsonify({'error': 'El email ya está registrado'}), 400

    nombre_completo=datos_docente.get('nombre_completo')
    nombres=datos_docente.get('nombres')
    primer_apellido=datos_docente.get('primer_apellido')
    segundo_apellido=datos_docente.get('segundo_apellido')
    usuario=datos_docente.get('usuario')
    
    password=datos_docente.get('password')
    activo=datos_docente.get('activo')

    nuevo_docente = Docentes(nombre_completo=nombre_completo, nombres=nombres, primer_apellido=primer_apellido, segundo_apellido=segundo_apellido, usuario=usuario, email=email, activo=activo)
    nuevo_docente.set_password(password)

    db.session.add(nuevo_docente)
    db.session.commit()
    return 'Docente creado'

@docentes_routes.route('/api/docentes/<int:docente_id>', methods=['GET'])
@verificar_jwt
def obtener_docente(docente_id):
    docente = Docentes.query.get(docente_id)
    
    if not docente:
        return 'Docente no encontrado', 404
    
    return jsonify(docente.as_dict())

@docentes_routes.route('/api/docentes/<int:docente_id>', methods=['DELETE'])
@solo_admin
def eliminar_alumno(docente_id):
    docente = Docentes.query.get(docente_id)
    if not docente:
        return 'Docente no encontrado', 404
    db.session.delete(docente)
    db.session.commit()
    return 'Docente eliminado'