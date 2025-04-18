from flask import Blueprint, request, jsonify
from models.conexion import obtener_conexion

profesores_bp = Blueprint('profesores', __name__)

# Obtener todos los profesores
@profesores_bp.route('/profesores', methods=['GET'])
def listar_profesores():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM profesor")
    profesores = cursor.fetchall()
    cursor.close()
    conexion.close()
    return jsonify(profesores)

# Obtener un profesor por ID
@profesores_bp.route('/profesores/<int:id_profesor>', methods=['GET'])
def obtener_profesor(id_profesor):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM profesor WHERE id_profesor = %s", (id_profesor,))
    profesor = cursor.fetchone()
    cursor.close()
    conexion.close()
    if profesor:
        return jsonify(profesor)
    else:
        return jsonify({'mensaje': 'Profesor no encontrado'}), 404

# Crear un nuevo profesor
@profesores_bp.route('/profesores', methods=['POST'])
def crear_profesor():
    datos = request.get_json()
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO profesor (numero_trabajador, nombre, a_paterno, a_materno, correo, rfc)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        datos['numero_trabajador'], datos['nombre'], datos['a_paterno'],
        datos['a_materno'], datos['correo'], datos['rfc']
    ))
    conexion.commit()
    cursor.close()
    conexion.close()
    return jsonify({'mensaje': 'Profesor creado exitosamente'}), 201

# Actualizar un profesor
@profesores_bp.route('/profesores/<int:id_profesor>', methods=['PUT'])
def actualizar_profesor(id_profesor):
    datos = request.get_json()
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        UPDATE profesor SET numero_trabajador = %s, nombre = %s, a_paterno = %s,
        a_materno = %s, correo = %s, rfc = %s WHERE id_profesor = %s
    """, (
        datos['numero_trabajador'], datos['nombre'], datos['a_paterno'],
        datos['a_materno'], datos['correo'], datos['rfc'], id_profesor
    ))
    conexion.commit()
    cursor.close()
    conexion.close()
    return jsonify({'mensaje': 'Profesor actualizado correctamente'})

# Eliminar un profesor
@profesores_bp.route('/profesores/<int:id_profesor>', methods=['DELETE'])
def eliminar_profesor(id_profesor):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM profesor WHERE id_profesor = %s", (id_profesor,))
    conexion.commit()
    cursor.close()
    conexion.close()
    return jsonify({'mensaje': 'Profesor eliminado correctamente'})
