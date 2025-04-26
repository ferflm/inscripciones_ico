from flask import Blueprint, render_template, request, jsonify
from models.conexion import obtener_conexion

horario_bp = Blueprint('horario', __name__)

@horario_bp.route('/horarios/listar', methods=['GET'])
def vista_listar_horarios():
    return render_template('horarios/listar_horarios.html')

@horario_bp.route('/horarios/agregar')
def vista_agregar_horario():
    return render_template('horarios/agregar_horario.html')

@horario_bp.route('/horarios/editar')
def vista_editar_horario():
    return render_template('horarios/editar_horario.html')

@horario_bp.route('/horarios', methods=['GET'])
def listar_horarios():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("""
        SELECT
            h.id_horario,
            m.clave_materia,
            m.nombre AS nombre_materia,
            CONCAT(p.nombre, ' ', p.a_paterno, ' ', p.a_materno) AS profesor,
            g.clave_grupo,
            h.dia,
            h.hora_inicio,
            h.hora_fin,
            h.salon
        FROM horario h
        JOIN grupo_materia gm ON h.id_grupo_materia = gm.id_grupo_materia
        JOIN materia m ON gm.id_materia = m.id_materia
        JOIN grupo g ON gm.id_grupo = g.id_grupo
        LEFT JOIN profesor p ON gm.id_profesor = p.id_profesor
    """)
    horarios = cursor.fetchall()
    for horario in horarios:
        horario['hora_inicio'] = str(horario['hora_inicio'])
        horario['hora_fin'] = str(horario['hora_fin'])
    cursor.close()
    conexion.close()
    return jsonify(horarios)


@horario_bp.route('/horarios', methods=['POST'])
def agregar_horario():
    datos = request.get_json()
    id_grupo_materia = datos['id_grupo_materia']
    dia = datos['dia']
    hora_inicio = datos['hora_inicio']
    hora_fin = datos['hora_fin']
    salon = datos['salon']

    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO horario (id_grupo_materia, dia, hora_inicio, hora_fin, salon)
        VALUES (%s, %s, %s, %s, %s)
    """, (id_grupo_materia, dia, hora_inicio, hora_fin, salon))
    conexion.commit()
    cursor.close()
    conexion.close()

    return jsonify({'mensaje': 'Horario agregado exitosamente'}), 201


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

@horario_bp.route('/grupo_materia/opciones', methods=['GET'])
def obtener_opciones_grupo_materia():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("""
        SELECT
            gm.id_grupo_materia,
            m.nombre AS nombre_materia,
            g.clave_grupo
        FROM grupo_materia gm
        JOIN materia m ON gm.id_materia = m.id_materia
        JOIN grupo g ON gm.id_grupo = g.id_grupo
    """)
    opciones = cursor.fetchall()
    cursor.close()
    conexion.close()

    resultado = [
        {
            "id": op["id_grupo_materia"],
            "texto": f'{op["nombre_materia"]} {op["clave_grupo"]}'
        } for op in opciones
    ]
    return jsonify(resultado)

@horario_bp.route('/horarios/<int:id_horario>', methods=['GET'])
def obtener_horario(id_horario):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("""
        SELECT
            h.id_horario,
            gm.id_grupo_materia,
            h.dia,
            h.hora_inicio,
            h.hora_fin,
            h.salon
        FROM horario h
        JOIN grupo_materia gm ON h.id_grupo_materia = gm.id_grupo_materia
        WHERE h.id_horario = %s
    """, (id_horario,))
    horario = cursor.fetchone()
    cursor.close()
    conexion.close()
    if horario:
        horario['hora_inicio'] = str(horario['hora_inicio'])
        horario['hora_fin'] = str(horario['hora_fin'])
        return jsonify(horario)
    else:
        return jsonify({'error': 'Horario no encontrado'}), 404