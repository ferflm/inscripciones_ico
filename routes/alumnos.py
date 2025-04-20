from flask import Blueprint, render_template, request, jsonify
from models.conexion import obtener_conexion

alumnos_bp = Blueprint('alumnos', __name__)

# GET: Listar todos los alumnos
@alumnos_bp.route('/alumnos', methods=['GET'])
def listar_alumnos():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM alumno")
    alumnos = cursor.fetchall()
    cursor.close()
    conexion.close()
    return render_template('alumnos/listar.html', alumnos=alumnos)

# GET: Obtener un alumno por ID
@alumnos_bp.route('/alumnos/<int:id_alumno>', methods=['GET'])
def obtener_alumno(id_alumno):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM alumno WHERE id_alumno = %s", (id_alumno,))
    alumno = cursor.fetchone()
    cursor.close()
    conexion.close()
    if alumno:
        return jsonify(alumno)
    else:
        return jsonify({'error': 'Alumno no encontrado'}), 404

# POST: Crear un nuevo alumno
@alumnos_bp.route('/alumnos', methods=['POST'])
def crear_alumno():
    data = request.json
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute("""
            INSERT INTO alumno (numero_cuenta, nombre, a_paterno, a_materno, correo, contrasena)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (data['numero_cuenta'], data['nombre'], data['a_paterno'], data['a_materno'], data['correo'], data['contrasena']))
        conexion.commit()
        id_nuevo = cursor.lastrowid
        cursor.close()
        conexion.close()
        return jsonify({'mensaje': 'Alumno creado', 'id_alumno': id_nuevo}), 201
    except Exception as e:
        conexion.rollback()
        return jsonify({'error': str(e)}), 400

# PUT: Actualizar un alumno existente
@alumnos_bp.route('/alumnos/<int:id_alumno>', methods=['PUT'])
def actualizar_alumno(id_alumno):
    data = request.json
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute("""
            UPDATE alumno
            SET numero_cuenta = %s, nombre = %s, a_paterno = %s, a_materno = %s, correo = %s, contrasena = %s
            WHERE id_alumno = %s
        """, (data['numero_cuenta'], data['nombre'], data['a_paterno'], data['a_materno'], data['correo'], data['contrasena'], id_alumno))
        conexion.commit()
        cursor.close()
        conexion.close()
        return jsonify({'mensaje': 'Alumno actualizado'})
    except Exception as e:
        conexion.rollback()
        return jsonify({'error': str(e)}), 400

# DELETE: Eliminar un alumno
@alumnos_bp.route('/alumnos/<int:id_alumno>', methods=['DELETE'])
def eliminar_alumno(id_alumno):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute("DELETE FROM alumno WHERE id_alumno = %s", (id_alumno,))
        conexion.commit()
        cursor.close()
        conexion.close()
        return jsonify({'mensaje': 'Alumno eliminado'})
    except Exception as e:
        conexion.rollback()
        return jsonify({'error': str(e)}), 400

@alumnos_bp.route('/alumnos/<int:id_alumno>/editar', methods=['GET'])
def formulario_editar_alumno(id_alumno):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM alumno WHERE id_alumno = %s", (id_alumno,))
    alumno = cursor.fetchone()
    cursor.close()
    conexion.close()
    if alumno:
        return render_template('alumnos/editar.html', alumno=alumno)
    else:
        return "Alumno no encontrado", 404
    

@alumnos_bp.route('/alumnos/nuevo', methods=['GET'])
def formulario_crear_alumno():
    return render_template('alumnos/agregar.html')
