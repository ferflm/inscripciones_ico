from flask import Blueprint, request, jsonify
from models.conexion import obtener_conexion

materias_bp = Blueprint('materias', __name__)

# GET: Listar todas las materias
@materias_bp.route('/materias', methods=['GET'])
def listar_materias():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM materia")
    materias = cursor.fetchall()
    cursor.close()
    conexion.close()
    return jsonify(materias)

# POST: Agregar una nueva materia
@materias_bp.route('/materias', methods=['POST'])
def agregar_materia():
    data = request.json
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO materia (clave_materia, nombre, creditos, requiere_lab, es_optativa)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        data['clave_materia'],
        data['nombre'],
        data['creditos'],
        data['requiere_lab'],
        data['es_optativa']
    ))
    conexion.commit()
    cursor.close()
    conexion.close()
    return jsonify({"mensaje": "Materia agregada correctamente"})

# PUT: Actualizar una materia existente
@materias_bp.route('/materias/<int:id>', methods=['PUT'])
def actualizar_materia(id):
    data = request.json
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        UPDATE materia
        SET clave_materia = %s, nombre = %s, creditos = %s,
            requiere_lab = %s, es_optativa = %s
        WHERE id_materia = %s
    """, (
        data['clave_materia'],
        data['nombre'],
        data['creditos'],
        data['requiere_lab'],
        data['es_optativa'],
        id
    ))
    conexion.commit()
    cursor.close()
    conexion.close()
    return jsonify({"mensaje": "Materia actualizada correctamente"})

# DELETE: Eliminar una materia
@materias_bp.route('/materias/<int:id>', methods=['DELETE'])
def eliminar_materia(id):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM materia WHERE id_materia = %s", (id,))
    conexion.commit()
    cursor.close()
    conexion.close()
    return jsonify({"mensaje": "Materia eliminada correctamente"})
