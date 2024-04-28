from models.models import Docentes
from models.models import db
from flask import Blueprint, Flask, jsonify, request
import jwt
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv

load_dotenv()

jwtsecret = os.getenv("JWT_SECRET_KEY")
auth_routes = Blueprint('auth_routes', __name__)

@auth_routes.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'email y password son requeridos'}), 400

    docente = Docentes.query.filter_by(email=email).first()

    if not docente or not docente.check_password(password):
        return jsonify({'error': 'Email o contraseña incorrectos'}), 401

    token = jwt.encode({'docente_id': docente.docente_id, 'rol': docente.rol, 'exp': datetime.now(timezone.utc) + timedelta(hours=1)}, jwtsecret, algorithm='HS256')

    return jsonify({'token': token}), 200