from models.models import AlumnosCursos
from models.models import db
from flask import Blueprint, jsonify, request

alumnoscursos_routes = Blueprint('alumnoscursos_routes', __name__)

@alumnoscursos_routes.route('/api/alumnoscursos', methods=['POST'])
def asignar_alumno_a_curso():
    data = request.get_json()
    alumno_id = data.get('alumno_id')
    curso_id = data.get('curso_id')

    nueva_relacion = AlumnosCursos(alumno_id=alumno_id, curso_id=curso_id)

    db.session.add(nueva_relacion)
    db.session.commit()

    return jsonify({'message': 'Relación Alumno-Curso creada correctamente'}), 200