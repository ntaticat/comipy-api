from flask import request, jsonify
import jwt
from functools import wraps
import os
from dotenv import load_dotenv

load_dotenv()

jwtsecret = os.getenv("JWT_SECRET_KEY")

def verificar_jwt(f):
    @wraps(f)
    def decorador(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'mensaje': 'Token de autorización faltante'}), 401

        try:
            payload = jwt.decode(token, jwtsecret, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return jsonify({'mensaje': 'Token de autorización expirado'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'mensaje': 'Token de autorización inválido'}), 401

        return f(*args, **kwargs)

    return decorador