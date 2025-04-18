from flask import Flask, render_template
from routes.alumnos import alumnos_bp

app = Flask(__name__)
app.secret_key = "clave_secreta"  # Necesario para sesiones o flashes

@app.route('/')
def index():
    return render_template('index.html')


app.register_blueprint(alumnos_bp)

if __name__ == '__main__':
    app.run(debug=True)