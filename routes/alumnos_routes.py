from flask import Blueprint, jsonify, request
from models.models import db
from models.models import Alumnos, AlumnosCursos, Asistencias
from auth.auth import verificar_jwt, solo_admin

alumnos_routes = Blueprint('alumnos_routes', __name__)

@alumnos_routes.route('/api/alumnos', methods=['POST'])
@verificar_jwt
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

@alumnos_routes.route('/api/alumnos', methods=['GET'])
@verificar_jwt
def obtener_alumnos():
    alumnos = Alumnos.query.all()
    alumnos_json = [alumno.as_dict() for alumno in alumnos]
    
    return jsonify(alumnos_json)

@alumnos_routes.route('/api/alumnos/<int:alumno_id>', methods=['GET'])
@verificar_jwt
def obtener_alumno(alumno_id):
    alumno = Alumnos.query.get(alumno_id)
    
    if not alumno:
        return 'Alumno no encontrado', 404
    
    cursos = [curso.as_dict() for curso in alumno.cursos]

    alumno_dict = alumno.as_dict()
    alumno_dict['cursos'] = cursos
    
    return jsonify(alumno_dict)

@alumnos_routes.route('/api/alumnos/<int:alumno_id>/asistencias', methods=['GET'])
@verificar_jwt
def obtener_alumno_asistencias(alumno_id):
    alumnoscursos = AlumnosCursos.query.filter_by(alumno_id=alumno_id).all()
    cursos_ids = [alumnocurso.curso_id for alumnocurso in alumnoscursos]

    asistencias_alumno = Asistencias.query.filter(Asistencias.curso_id.in_(cursos_ids)).all()
    
    asistencias_json = [asistencia_alumno.as_dict() for asistencia_alumno in asistencias_alumno]
    
    return jsonify(asistencias_json), 200

@alumnos_routes.route('/api/alumnos/<int:alumno_id>', methods=['PUT'])
@solo_admin
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

    alumno.nombre_completo=nombre_completo
    alumno.nombres=nombres
    alumno.primer_apellido=primer_apellido
    alumno.segundo_apellido=segundo_apellido
    alumno.turno_id=turno_id
    alumno.activo=activo
    alumno.folio=folio

    db.session.commit()
    return 'Alumno actualizado'

@alumnos_routes.route('/api/alumnos/<int:alumno_id>', methods=['DELETE'])
@solo_admin
def eliminar_alumno(alumno_id):
    alumno = Alumnos.query.get(alumno_id)
    if not alumno:
        return 'Alumno no encontrado', 404
    db.session.delete(alumno)
    db.session.commit()
    return 'Alumno eliminado'
