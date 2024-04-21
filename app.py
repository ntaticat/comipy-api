from flask import Flask, jsonify
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configuración de la base de datos
db = mysql.connector.connect(
    host='24.199.104.126',
    user='comipy',
    password='Panque123!',
    database='dbcomipems'
)

# Ruta para obtener todos los alumnos
@app.route('/api/alumnos', methods=['GET'])
def obtener_alumnos():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM alumnos")
    alumnos = cursor.fetchall()
    cursor.close()

    # Lista para almacenar los datos con las claves modificadas
    alumnos_con_claves = []

    # Recorremos cada fila de la tabla de alumnos
    for alumno in alumnos:
        # Creamos un diccionario para almacenar los datos de este alumno
        alumno_con_claves = {}
        # Recorremos cada columna en la tabla
        for idx, columna in enumerate(cursor.description):
            # Asignamos el valor de la columna al diccionario usando el nombre de la columna como clave
            alumno_con_claves[columna[0]] = alumno[idx]
        # Agregamos el diccionario del alumno a la lista
        alumnos_con_claves.append(alumno_con_claves)

    # Devolvemos la lista de alumnos con las claves modificadas
    return jsonify(alumnos_con_claves)

if __name__ == '__main__':
    app.run(debug=True)