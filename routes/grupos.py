from flask import Blueprint, request, jsonify
from models.conexion import obtener_conexion

grupos_bp = Blueprint('grupos', __name__)

# GET: Listar todos los grupos
@grupos_bp.route('/grupos', methods=['GET'])
def listar_grupos():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM grupo")
    grupos = cursor.fetchall()
    cursor.close()
    conexion.close()
    return jsonify(grupos)

# POST: Agregar un nuevo grupo
@grupos_bp.route('/grupos', methods=['POST'])
def agregar_grupo():
    datos = request.json
    clave_grupo = datos.get('clave_grupo')
    semestre = datos.get('semestre')

    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO grupo (clave_grupo, semestre) VALUES (%s, %s)", (clave_grupo, semestre))
    conexion.commit()
    cursor.close()
    conexion.close()
    return jsonify({'mensaje': 'Grupo agregado exitosamente'}), 201

# PUT: Actualizar grupo
@grupos_bp.route('/grupos/<int:id_grupo>', methods=['PUT'])
def actualizar_grupo(id_grupo):
    datos = request.json
    clave_grupo = datos.get('clave_grupo')
    semestre = datos.get('semestre')

    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("UPDATE grupo SET clave_grupo = %s, semestre = %s WHERE id_grupo = %s", (clave_grupo, semestre, id_grupo))
    conexion.commit()
    cursor.close()
    conexion.close()
    return jsonify({'mensaje': 'Grupo actualizado correctamente'})

# DELETE: Eliminar grupo
@grupos_bp.route('/grupos/<int:id_grupo>', methods=['DELETE'])
def eliminar_grupo(id_grupo):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM grupo WHERE id_grupo = %s", (id_grupo,))
    conexion.commit()
    cursor.close()
    conexion.close()
    return jsonify({'mensaje': 'Grupo eliminado correctamente'})
