from flask import Blueprint, request, jsonify
from models.conexion import obtener_conexion

inscripciones_bp = Blueprint('inscripciones', __name__)

# Obtener todas las inscripciones
@inscripciones_bp.route('/inscripciones', methods=['GET'])
def listar_inscripciones():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("""
        SELECT i.id_inscripcion, a.nombre AS alumno, m.nombre AS materia, g.clave_grupo, i.fecha_inscripcion
        FROM inscripcion i
        JOIN alumno a ON i.id_alumno = a.id_alumno
        JOIN grupo_materia gm ON i.id_grupo_materia = gm.id_grupo_materia
        JOIN grupo g ON gm.id_grupo = g.id_grupo
        JOIN materia m ON gm.id_materia = m.id_materia
    """)
    inscripciones = cursor.fetchall()
    cursor.close()
    conexion.close()

    # Convertir datetime a string
    for i in inscripciones:
        i['fecha_inscripcion'] = i['fecha_inscripcion'].strftime("%Y-%m-%d %H:%M:%S")

    return jsonify(inscripciones)

# Agregar inscripción
@inscripciones_bp.route('/inscripciones', methods=['POST'])
def agregar_inscripcion():
    datos = request.get_json()
    id_alumno = datos['id_alumno']
    id_grupo_materia = datos['id_grupo_materia']

    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute("INSERT INTO inscripcion (id_alumno, id_grupo_materia) VALUES (%s, %s)",
                       (id_alumno, id_grupo_materia))
        conexion.commit()
        mensaje = {'mensaje': 'Inscripción registrada correctamente'}
    except Exception as e:
        mensaje = {'error': str(e)}
    finally:
        cursor.close()
        conexion.close()
    return jsonify(mensaje)

# Eliminar inscripción
@inscripciones_bp.route('/inscripciones/<int:id_inscripcion>', methods=['DELETE'])
def eliminar_inscripcion(id_inscripcion):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM inscripcion WHERE id_inscripcion = %s", (id_inscripcion,))
    conexion.commit()
    cursor.close()
    conexion.close()
    return jsonify({'mensaje': 'Inscripción eliminada correctamente'})
