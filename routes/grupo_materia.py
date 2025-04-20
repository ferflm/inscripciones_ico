from flask import Blueprint, request, jsonify
from models.conexion import obtener_conexion

grupo_materia_bp = Blueprint('grupo_materia', __name__)

# Listar todos los registros
@grupo_materia_bp.route('/grupo_materia', methods=['GET'])
def listar_grupo_materia():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM grupo_materia")
    registros = cursor.fetchall()
    cursor.close()
    conexion.close()
    return jsonify(registros)

# Agregar un nuevo registro
@grupo_materia_bp.route('/grupo_materia', methods=['POST'])
def agregar_grupo_materia():
    datos = request.json
    id_grupo = datos['id_grupo']
    id_materia = datos['id_materia']
    id_profesor = datos.get('id_profesor')  # Puede ser nulo
    cupo_maximo = datos['cupo_maximo']

    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO grupo_materia (id_grupo, id_materia, id_profesor, cupo_maximo)
        VALUES (%s, %s, %s, %s)
    """, (id_grupo, id_materia, id_profesor, cupo_maximo))
    conexion.commit()
    cursor.close()
    conexion.close()
    return jsonify({'mensaje': 'Registro agregado correctamente'})

# Actualizar un registro
@grupo_materia_bp.route('/grupo_materia/<int:id>', methods=['PUT'])
def actualizar_grupo_materia(id):
    datos = request.json
    id_grupo = datos['id_grupo']
    id_materia = datos['id_materia']
    id_profesor = datos.get('id_profesor')  # Puede ser nulo
    cupo_maximo = datos['cupo_maximo']

    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        UPDATE grupo_materia
        SET id_grupo = %s, id_materia = %s, id_profesor = %s, cupo_maximo = %s
        WHERE id_grupo_materia = %s
    """, (id_grupo, id_materia, id_profesor, cupo_maximo, id))
    conexion.commit()
    cursor.close()
    conexion.close()
    return jsonify({'mensaje': 'Registro actualizado correctamente'})

# Eliminar un registro
@grupo_materia_bp.route('/grupo_materia/<int:id>', methods=['DELETE'])
def eliminar_grupo_materia(id):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM grupo_materia WHERE id_grupo_materia = %s", (id,))
    conexion.commit()
    cursor.close()
    conexion.close()
    return jsonify({'mensaje': 'Registro eliminado correctamente'})
