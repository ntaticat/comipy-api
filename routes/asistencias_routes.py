from models.models import Asistencias
from models.models import db
from flask import Blueprint, jsonify, request
from auth.auth import verificar_jwt, solo_admin

asistencias_routes = Blueprint('asistencias_routes', __name__)

@asistencias_routes.route('/api/asistencias', methods=['POST'])
@verificar_jwt
def registrar_asistencia():

    if not request.json:
        return jsonify({'error': 'No se proporcionaron datos JSON'}), 400

    data = request.get_json()
    
    alumno_id = data.get('alumno_id')
    curso_id = data.get('curso_id')
    presento_actividad = data.get('presento_actividad')
    registrado_siri = data.get('registrado_siri')

    nuevo_alumno = Asistencias(alumno_id=alumno_id, curso_id=curso_id, presento_actividad=presento_actividad, registrado_siri=registrado_siri)
    db.session.add(nuevo_alumno)
    db.session.commit()
    return 'Asistencia creada'