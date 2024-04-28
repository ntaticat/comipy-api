from flask import Blueprint, jsonify, request
from models.models import db
from models.models import Cursos, AlumnosCursos, Asistencias
from auth.auth import verificar_jwt

cursos_routes = Blueprint('cursos_routes', __name__)

@cursos_routes.route('/api/cursos', methods=['POST'])
@verificar_jwt
def crear_curso():
    if not request.json:
        return jsonify({'error': 'No se proporcionaron datos JSON'}), 400

    datos_curso = request.json

    identificador=datos_curso.get('identificador')
    descripcion=datos_curso.get('descripcion')

    nuevo_curso = Cursos(identificador=identificador, descripcion=descripcion)
    db.session.add(nuevo_curso)
    db.session.commit()
    return 'Curso creado'

# Ruta para obtener todos los cursos
@cursos_routes.route('/api/cursos', methods=['GET'])
@verificar_jwt
def obtener_cursos():
    cursos = Cursos.query.all()
    cursos_json = [curso.as_dict() for curso in cursos]
    
    return jsonify(cursos_json)

@cursos_routes.route('/api/cursos/<int:curso_id>', methods=['GET'])
@verificar_jwt
def obtener_curso(curso_id):
    curso = Cursos.query.get(curso_id)
    
    if not curso:
        return 'Curso no encontrado', 404
    
    alumnos = [alumno.as_dict() for alumno in curso.alumnos]

    curso_alumnos = {
        'curso_id': curso.curso_id,
        'identificador': curso.identificador,
        'descripcion': curso.descripcion,
        'alumnos': alumnos
    }
    
    return jsonify(curso_alumnos)

@cursos_routes.route('/api/cursos/<int:curso_id>/asistencias', methods=['GET'])
@verificar_jwt
def obtener_curso_asistencias(curso_id):
    alumnoscursos = AlumnosCursos.query.filter_by(curso_id=curso_id).all()
    alumnos_ids = [alumnocurso.alumno_id for alumnocurso in alumnoscursos]

    asistencias_curso = Asistencias.query.filter(Asistencias.alumno_id.in_(alumnos_ids)).all()
    
    asistencias_json = [asistencia_curso.as_dict() for asistencia_curso in asistencias_curso]
    
    return jsonify(asistencias_json), 200

@cursos_routes.route('/api/cursos/<int:curso_id>', methods=['PUT'])
@verificar_jwt
def actualizar_curso(curso_id):
    if not request.json:
        return jsonify({'error': 'No se proporcionaron datos JSON'}), 400
    
    curso = Cursos.query.get(curso_id)
    if not curso:
        return 'Curso no encontrado', 404

    datos_curso = request.json
    nombre_completo=datos_curso.get('nombre_completo')
    nombres=datos_curso.get('nombres')
    primer_apellido=datos_curso.get('primer_apellido')
    segundo_apellido=datos_curso.get('segundo_apellido')
    turno_id=datos_curso.get('turno_id')
    activo=datos_curso.get('activo')
    folio=datos_curso.get('folio')
    
    curso.nombres = 'Nuevo nombre de Rafael'

    curso.nombre_completo=nombre_completo
    curso.nombres=nombres
    curso.primer_apellido=primer_apellido
    curso.segundo_apellido=segundo_apellido
    curso.turno_id=turno_id
    curso.activo=activo
    curso.folio=folio

    db.session.commit()
    return 'Curso actualizado'

@cursos_routes.route('/api/cursos/<int:curso_id>', methods=['DELETE'])
@verificar_jwt
def eliminar_curso(curso_id):
    curso = Cursos.query.get(curso_id)
    if not curso:
        return 'Curso no encontrado', 404
    db.session.delete(curso)
    db.session.commit()
    return 'Curso eliminado'