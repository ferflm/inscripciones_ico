from flask import Blueprint, request, jsonify, render_template
from models.conexion import obtener_conexion

grupo_materia_bp = Blueprint('grupo_materia', __name__)

# ----------------------------
# RUTAS PARA LA INTERFAZ HTML
# ----------------------------

# Mostrar formulario para crear grupo_materia
@grupo_materia_bp.route('/grupo_materia/crear', methods=['GET'])
def mostrar_formulario_grupo_materia():
    return render_template('grupo_materia/agregar_grupo_materia.html')

# Mostrar formulario para editar grupo_materia
@grupo_materia_bp.route('/grupo_materia/<int:id>/editar', methods=['GET'])
def editar_grupo_materia(id):
    return render_template('grupo_materia/editar_grupo_materia.html')

# Mostrar todos los registros en una tabla (vista HTML)
@grupo_materia_bp.route('/grupo_materia/listar', methods=['GET'])
def vista_listado_grupo_materia():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            gm.id_grupo_materia,
            g.clave_grupo,
            m.nombre AS nombre_materia,
            CONCAT(p.nombre, ' ', p.a_paterno, ' ', p.a_materno) AS nombre_profesor,
            gm.cupo_maximo
        FROM grupo_materia gm
        JOIN grupo g ON gm.id_grupo = g.id_grupo
        JOIN materia m ON gm.id_materia = m.id_materia
        LEFT JOIN profesor p ON gm.id_profesor = p.id_profesor
    """)
    registros = cursor.fetchall()
    cursor.close()
    conexion.close()
    return render_template('grupo_materia/grupo_materia.html', registros=registros)

# ----------------------------
# API JSON
# ----------------------------

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

# Obtener un registro por ID
@grupo_materia_bp.route('/grupo_materia/<int:id>', methods=['GET'])
def obtener_grupo_materia(id):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM grupo_materia WHERE id_grupo_materia = %s", (id,))
    registro = cursor.fetchone()
    cursor.close()
    conexion.close()
    return jsonify(registro)

# Obtener datos para los formularios
@grupo_materia_bp.route('/grupo_materia/datos_formulario', methods=['GET'])
def datos_para_formulario():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("SELECT id_grupo, clave_grupo FROM grupo")
    grupos = cursor.fetchall()

    cursor.execute("SELECT id_materia, nombre FROM materia")
    materias = cursor.fetchall()

    cursor.execute("SELECT id_profesor, nombre, a_paterno, a_materno FROM profesor")
    profesores = cursor.fetchall()

    cursor.close()
    conexion.close()

    # Armamos nombres completos
    for p in profesores:
        p["nombre_completo"] = f"{p['nombre']} {p['a_paterno']} {p['a_materno']}"

    return jsonify({
        "grupos": grupos,
        "materias": materias,
        "profesores": profesores
    })

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