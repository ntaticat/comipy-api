from models.models import AlumnosCursos
from models.models import db
from flask import Blueprint, jsonify, request
from auth.auth import verificar_jwt, solo_admin

alumnoscursos_routes = Blueprint('alumnoscursos_routes', __name__)

@alumnoscursos_routes.route('/api/alumnoscursos', methods=['POST'])
@verificar_jwt
def asignar_alumno_a_curso():
    data = request.get_json()
    alumno_id = data.get('alumno_id')
    curso_id = data.get('curso_id')
    activo=data.get('activo')

    nueva_relacion = AlumnosCursos(alumno_id=alumno_id, curso_id=curso_id, activo=activo)

    db.session.add(nueva_relacion)
    db.session.commit()

    return jsonify({'message': 'Relación Alumno-Curso creada correctamente'}), 200