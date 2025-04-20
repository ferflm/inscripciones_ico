from flask import Blueprint, request, jsonify
from models.conexion import obtener_conexion

horario_bp = Blueprint('horario', __name__)

@horario_bp.route('/horarios', methods=['GET'])
def listar_horarios():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Horario")
    horarios = cursor.fetchall()
    for horario in horarios:
        horario['hora_inicio'] = str(horario['hora_inicio'])
        horario['hora_fin'] = str(horario['hora_fin'])
    cursor.close()
    conexion.close()
    return jsonify(horarios)


@horario_bp.route('/horarios', methods=['POST'])
def agregar_horario():
    datos = request.json
    id_grupo_materia = datos['id_grupo_materia']
    dia = datos['dia']
    hora_inicio = datos['hora_inicio']
    hora_fin = datos['hora_fin']
    salon = datos['salon']

    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO Horario (id_grupo_materia, dia, hora_inicio, hora_fin, salon)
        VALUES (%s, %s, %s, %s, %s)
    """, (id_grupo_materia, dia, hora_inicio, hora_fin, salon))
    conexion.commit()
    cursor.close()
    conexion.close()
    return jsonify({'mensaje': 'Horario agregado correctamente'}), 201

@horario_bp.route('/horarios/<int:id_horario>', methods=['PUT'])
def actualizar_horario(id_horario):
    datos = request.json
    id_grupo_materia = datos['id_grupo_materia']
    dia = datos['dia']
    hora_inicio = datos['hora_inicio']
    hora_fin = datos['hora_fin']
    salon = datos['salon']

    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        UPDATE Horario
        SET id_grupo_materia = %s, dia = %s, hora_inicio = %s, hora_fin = %s, salon = %s
        WHERE id_horario = %s
    """, (id_grupo_materia, dia, hora_inicio, hora_fin, salon, id_horario))
    conexion.commit()
    cursor.close()
    conexion.close()
    return jsonify({'mensaje': 'Horario actualizado correctamente'})

@horario_bp.route('/horarios/<int:id_horario>', methods=['DELETE'])
def eliminar_horario(id_horario):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM Horario WHERE id_horario = %s", (id_horario,))
    conexion.commit()
    cursor.close()
    conexion.close()
    return jsonify({'mensaje': 'Horario eliminado correctamente'})
