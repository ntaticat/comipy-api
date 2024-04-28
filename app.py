from models.models import db
from flask import Flask
from flask_cors import CORS
from routes.alumnos_routes import alumnos_routes
from routes.turnos_routes import turnos_routes
from routes.cursos_routes import cursos_routes
from routes.docentes_routes import docentes_routes
from routes.auth_routes import auth_routes
from routes.alumnoscursos_routes import alumnoscursos_routes
from routes.asistencias_routes import asistencias_routes
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.debug = False
CORS(app)

mysqluri = os.getenv("MYSQL_STRING")

app.config['SQLALCHEMY_DATABASE_URI'] = mysqluri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.register_blueprint(alumnos_routes)
app.register_blueprint(turnos_routes)
app.register_blueprint(cursos_routes)
app.register_blueprint(auth_routes)
app.register_blueprint(docentes_routes)
app.register_blueprint(alumnoscursos_routes)
app.register_blueprint(asistencias_routes)

if __name__ == '__main__':
    app.run(host='0.0.0.0') 