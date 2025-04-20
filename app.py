from flask import Flask, render_template
from routes.alumnos import alumnos_bp
from routes.profesores import profesores_bp
from routes.materias import materias_bp
from routes.grupos import grupos_bp
from routes.grupo_materia import grupo_materia_bp
from routes.horario import horario_bp
from routes.inscripciones import inscripciones_bp

app = Flask(__name__)
app.secret_key = "clave_secreta"  # Necesario para sesiones o flashes

@app.route('/')
def index():
    return render_template('index.html')


app.register_blueprint(alumnos_bp)
app.register_blueprint(profesores_bp)
app.register_blueprint(materias_bp)
app.register_blueprint(grupos_bp)
app.register_blueprint(grupo_materia_bp)
app.register_blueprint(horario_bp)
app.register_blueprint(inscripciones_bp)

if __name__ == '__main__':
    app.run(debug=True)