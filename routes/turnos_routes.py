from flask import Blueprint, jsonify, request
from models.models import db
from models.models import Turnos
from auth.auth import verificar_jwt, solo_admin

turnos_routes = Blueprint('turnos_routes', __name__)

@turnos_routes.route('/api/turnos', methods=['POST'])
@verificar_jwt
def crear_turno():

    if not request.json:
        return jsonify({'error': 'No se proporcionaron datos JSON'}), 400

    datos_turno = request.json

    identificador=datos_turno.get('identificador')
    descripcion=datos_turno.get('descripcion')

    nuevo_turno = Turnos(identificador=identificador, descripcion=descripcion)
    db.session.add(nuevo_turno)
    db.session.commit()
    return 'Turno creado'

@turnos_routes.route('/api/turnos/<int:turno_id>', methods=['DELETE'])
@solo_admin
def eliminar_turno(turno_id):
    turno = Turnos.query.get(turno_id)
    if not turno:
        return 'Turno no encontrado', 404
    db.session.delete(turno)
    db.session.commit()
    return 'Turno eliminado'